import hashlib
import io
import os
from datetime import datetime, timezone

import boto3
from fastapi import FastAPI, HTTPException
from huggingface_hub import InferenceClient
from pydantic import BaseModel
from genblaze_core import Manifest, Modality, RunBuilder, StepBuilder, StepStatus

app = FastAPI(title="Provenance Studio Genblaze Worker")
if os.getenv("B2_APPLICATION_KEY") and not os.getenv("B2_APP_KEY"):
    os.environ["B2_APP_KEY"] = os.environ["B2_APPLICATION_KEY"]

class GenerateRequest(BaseModel):
    prompt: str

def b2_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("B2_ENDPOINT", "https://s3.us-west-004.backblazeb2.com"),
        region_name=os.getenv("B2_REGION", "us-west-004"),
        aws_access_key_id=os.environ["B2_KEY_ID"],
        aws_secret_access_key=os.environ["B2_APP_KEY"],
    )

@app.post("/generate")
def generate(body: GenerateRequest):
    if not os.getenv("HF_TOKEN") or not os.getenv("B2_KEY_ID") or not os.getenv("B2_APP_KEY"):
        raise HTTPException(503, "Set HF_TOKEN, B2_KEY_ID, and B2_APPLICATION_KEY on the worker.")
    model = os.getenv("HF_IMAGE_MODEL", "black-forest-labs/FLUX.1-schnell")
    try:
        image = InferenceClient(api_key=os.environ["HF_TOKEN"]).text_to_image(prompt=body.prompt, model=model)
    except Exception as exc:
        raise HTTPException(502, f"Hugging Face image request failed: {exc}") from exc
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    payload = image_bytes.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    run_id = f"hf-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{digest[:8]}"
    bucket = os.getenv("B2_BUCKET", "provenance-studio")
    asset_key = f"runs/{run_id}/assets/generated.png"
    asset_uri = f"s3://{bucket}/{asset_key}"

    # Genblaze creates the canonical, replayable provenance record for this provider-agnostic step.
    step = (StepBuilder("huggingface", model).prompt(body.prompt).modality(Modality.IMAGE)
            .params(format="png", sha256=digest).status(StepStatus.SUCCEEDED)
            .asset(asset_uri, "image/png").build())
    manifest = Manifest.from_run(RunBuilder("provenance-studio-hf-image").add_step(step).build())
    manifest_key = f"runs/{run_id}/manifest.json"
    try:
        client = b2_client()
        client.put_object(Bucket=bucket, Key=asset_key, Body=payload, ContentType="image/png",
                          Metadata={"sha256": digest, "genblaze-run-id": run_id})
        client.put_object(Bucket=bucket, Key=manifest_key, Body=manifest.to_canonical_json().encode(),
                          ContentType="application/json")
    except Exception as exc:
        raise HTTPException(502, f"B2 archive failed: {exc}") from exc
    return {"id": run_id, "model": f"Hugging Face / {model}", "mode": "live",
            "asset_uri": asset_uri, "manifest_uri": f"s3://{bucket}/{manifest_key}",
            "sha256": digest, "manifest_hash": manifest.canonical_hash, "verified": manifest.verify()}
