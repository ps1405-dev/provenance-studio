# Devpost submission copy

## Inspiration

Creators can generate hundreds of assets, but lose the context needed to trust, reuse, or explain them. Provenance Studio makes every generation a durable, inspectable record.

## What it does

Provenance Studio is a generation workspace and media library for AI images. A creator writes a prompt, generates an asset, and receives a stored media object together with a canonical provenance manifest containing the prompt, provider, model, timestamps, workflow, asset URL, and SHA-256 hash. The library makes that lineage visible at the point of reuse.

## How we built it

The Next.js interface provides the creator workflow and asset library. A Python Genblaze worker runs the generation pipeline through GMI Cloud and uses Genblaze's ObjectStorageSink with Backblaze B2. The generated media and its hash-verified manifest are archived together in B2. The frontend has a direct B2-compatible archive fallback for provenance records.

## Genblaze and B2

Genblaze orchestrates the media generation step, creates the canonical manifest, records the run, and verifies output integrity. Backblaze B2 is the durable, S3-compatible system of record for generated files and provenance JSON. This keeps generated media independent of a short-lived provider URL and makes a run replayable.

## Challenges we ran into

We designed the app to separate the latency-sensitive user interface from the long-running media workflow. The worker boundary allows generation retries, provider swaps, and durable B2 writes without exposing provider keys to the browser.

## What's next

Next: video and audio workflows, collection-level access controls, prompt redaction policies, and replay/remix directly from a stored manifest.

## Providers and models

- Genblaze: pipeline orchestration and provenance
- GMI Cloud: image generation (configure the selected image model in `GMI_IMAGE_MODEL`)
- Backblaze B2: media and manifest storage

## Demo script (about 3 minutes)

1. Open the Library and explain that generated media needs an auditable story.
2. Enter a prompt and click Generate.
3. Show the resulting asset in Recent assets and open its detail panel.
4. Explain the Workflow, Provider/model, B2 archive status, and prompt record.
5. Open the B2 bucket and show the stored media plus its provenance manifest.
6. Open the manifest and point out prompt, timestamps, SHA-256, and canonical hash.
7. Close with why durable assets and replayable provenance matter for real creator workflows.

