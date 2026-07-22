# Genblaze + Hugging Face generation worker

This no-cost-to-start worker uses Hugging Face Inference Providers to generate an image, writes the PNG to Backblaze B2, then uses Genblaze to create and archive a canonical provenance manifest.

## Required environment variables

- `HF_TOKEN`: Hugging Face access token with Inference Provider permission
- `B2_KEY_ID`
- `B2_APPLICATION_KEY` (the worker maps this to Genblaze/B2's `B2_APP_KEY`)
- `B2_BUCKET`
- `B2_ENDPOINT=https://s3.us-west-004.backblazeb2.com`
- `B2_REGION=us-west-004`
- Optional: `HF_IMAGE_MODEL=black-forest-labs/FLUX.1-schnell`

## Deploy

Deploy the `worker` directory as a Python web service.

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

After deployment, set `GENBLAZE_WORKER_URL` in the frontend environment to the worker URL.
