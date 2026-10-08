# Creation record

Record for the first whale submission. Exact prompts are preserved in prompts/
and the generation records.

- Title: Ship It (working title)
- Creative idea: Docker-inspired whale ships a container into orbit and docks it back on its cargo stack.
- Google tool used: Google Cloud image generation API via scripts/generate_google.py
- Exact Nano Banana model used for submitted artwork: gemini-3-pro-image (Nano Banana Pro)
- Generation date: 2026-10-08
- Original downloaded filename: artwork/raw/whale-pro-keyframe.png
- Generation prompt file: prompts/docker-whale.txt (exact sent text in generation/whale-pro-keyframe.json)
- Follow-up edits/prompts: No generative edits to the selected Pro keyframe. Local layer extraction, native-grid resizing, and deterministic animation in scripts/build_whale.py.
- Chosen output filename: artwork/submission/ship-it-pro-64.gif
- Why it works on a 64×64 LED display: readable silhouette, bright connected color shapes, true-black background, stable canvas, and an infinite six-second loop.

The animation encoder records source hashes and processing settings in
artwork/submission/ship-it-pro-manifest.json. Nano Banana generated the source
artwork; local code creates the motion. Alternatives from Gemini 3.1 Flash
Image and Nano Banana 2.1 were also generated for comparison.
