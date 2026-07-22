# Provenance Studio

An AI media library that preserves the story behind every asset: prompt, workflow, provider, model, timestamps, and durable B2 archive record.

## Run locally

1. `npm install`
2. Copy `.env.example` to `.env.local` and add B2 credentials and `HF_TOKEN` (optional for demo mode).
3. `npm run dev`, then open http://localhost:3000.

## B2 integration

When B2 settings are configured, each generation writes a JSON provenance manifest to `provenance/<asset-id>.json` through B2's S3-compatible API.

## Genblaze integration point

`worker/main.py` is the generation boundary. It uses Hugging Face Inference Providers for the image call, builds a Genblaze canonical provenance manifest, then archives the media and manifest together in B2. The Next.js route forwards generation requests to the deployed worker.
