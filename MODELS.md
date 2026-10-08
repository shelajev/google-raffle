# Model selection, verified October 8, 2026

- Gemini 3.8 Flash (`gemini-3.8-flash`) accepts images as input and produces
  text. It cannot directly render our image assets.
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-8-flash
- Nano Banana 2.1 (`gemini-nano-banana-2.1`) is the newest image model, released
  October 6, 2026. Google describes improved visual quality, prompt adherence,
  character consistency and text over Nano Banana 2 / Gemini 3.1 Flash Image.
  https://ai.google.dev/gemini-api/docs/models/gemini-nano-banana-2.1
- Nano Banana Pro (`gemini-3-pro-image`) is a separate image model, not ordinary
  Gemini Pro. Google's Cloud documentation recommends it for challenging image
  generation and multi-turn editing. Other Google pages call 2.1 their best
  current image model, so provider copy does not establish a universal winner.
  https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/3-pro-image

Both 2.1 and Pro successfully generated the same prompts/docker-whale.txt
prompt. Actual generation records are in generation/. Pro has the more
expressive whale face in this pair; this is our visual judgment from one pair,
not a general model benchmark. The initial animation uses the Pro artwork.

Google's prompting guide advises narrative scene direction, explicit
composition, reference images for consistency, and iterative edits. It also
describes Nano Banana keyframes with Veo interpolation. For our native 64×64
pixel art, deterministic layer animation provides control over integer pixel
positions and looping; this is a project decision, not a claim that Veo is
inferior in general.
https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana

The current speaker talk listings were searched. We did not locate a relevant
talk transcript establishing a different model recommendation. Do not claim
that a talk was watched or read based only on a listing or abstract.
