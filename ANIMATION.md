# Animation plan: creative decisions first

Read [JUDGING.md](JUDGING.md) for the design targets derived from the supplied
leaderboard critique. Main target: 60 frames at 100 ms, a six-second seamless
loop, true-black negative space, bright coherent colors, and native-grid motion.

We are making animations. The static-image tools remain useful for keyframes.
Animation does not add more raffle tickets than stills; it is our creative
strategy for the visual contest. Leaderboard rank and moderation acceptance
cannot be guaranteed by a prompt or export setting.

## Two entries

1. **Ship It** — a Docker-inspired whale carrying container cargo. It bobs on
   waves, a rubber-duck captain salutes, then a container launches like a rocket
   and splashes back onto the stack. Final pose returns to the initial pose.
   Aim for a polished 4–6 second loop with an immediately readable whale.
2. **Forbidden Fruit** — a robot presents a banana to a comically serious
   scanner at a literal firewall. Scanner goes red; robot peels banana; scanner
   goes green; robot winks. The joke tests how the verifier handles mischievous
   visual context. It does not establish that any actual moderation boundary
   has been crossed. Use ordinary visible artwork, with no hidden instructions
   or claim that acceptance is assured.

## Your steps

1. Redeem the live raffle's Google Cloud credits and open its linked Studio.
2. Choose a Nano Banana image model. Use prompts/docker-whale.txt first.
3. Download the square keyframe into artwork/raw/whale-keyframe.png. Save the
   actual prompt and model name in the repo. Repeat with banana-firewall.txt
   for the second idea.
4. Let the assistant inspect the keyframes and create a motion plan/assets.
   A generated still needs additional animation work; the encoder alone does
   not animate the subject. We can animate separated layers programmatically,
   or make a consistent ordered sequence of frames. Keep all frames square,
   with a fixed camera, palette, scale, and character identity.
5. Export frames in playback order and run:

   ```sh
   ./animate artwork/raw/whale-frames/*.png --name ship-it --duration 100
   ```

   Use zero-padded frame names: 001.png, 002.png, etc. Forty frames at 100 ms
   gives a four-second loop. An existing square animated GIF also works:

   ```sh
   ./animate artwork/raw/whale.gif --name ship-it --duration 100
   ```

   For a precisely aligned 4×4 sprite sheet with equal square cells:

   ```sh
   ./animate artwork/raw/sheet.png --grid 4 --name ship-it --duration 250
   ```

   Inspect sheet boundaries before using this option: generated grids often
   need correction. Cells play left-to-right, top-to-bottom. No gutters/labels.
   The script applies a uniform frame duration, including to existing GIFs.
6. Review artwork/previews/ship-it-preview.gif and ship-it-frames.png. Check
   silhouette, joke, color stability, and the last-to-first transition. Also
   view the actual 64×64 GIF: enlarged previews can hide readability problems.
7. Fill in CREATION.md, publish our own repo with the final GIFs, prompts and
   processing code, then upload the *-64.gif files plus repo URL on the raffle
   site. Check success and the multiplier. Save room in the five daily
   submissions for revisions; do local reviews before submitting.

The encoder uses a shared 128-color palette, removes transparency onto black,
loops forever, and validates square 64×64 output, visible frame changes, and
file size below 5 MB. Up to three visual files can be submitted on the site.
There is room for a third concept after the first two are polished.
