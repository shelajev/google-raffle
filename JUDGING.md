# Design rules derived from the supplied leaderboard critique

Evidence: one critique supplied by Oleg, for Marc Durieux's
mdurieuxx/nano-banana-devoxx-pixels entry. This is not the complete scoring
formula. Targets below are creative/engineering choices, not known thresholds.

| Observed reward | Our production rule |
| --- | --- |
| True black integrated, 80% #000000 in the example | Use actual #000000 around the subject. Aim for roughly 65–80% black, while keeping the action readable. No mandatory 80% quota is established. |
| Clean dark clamping | Remove accidental dim near-black background noise. Export defaults to clamping pixels whose channels are all ≤12; inspect deliberate shadows and adjust if needed. |
| Bright saturation and cohesive clusters | Start with 8–14 deliberate colors, with bright blue/cyan, white, and a few warm accents. Big connected shapes, no scattered texture or dithering. |
| Crisp 1px edges and native grid | Compose final motion at 64×64; use integer positions. No subpixel camera movement, default blur, or anti-aliased outlines. Inspect the actual output. |
| Stable sprite animation | Anchor the canvas. Move whale, cargo, water and small effects as layers. Avoid whole-frame redraw jitter. |
| 60 frames and optimal cadence | Target 60 frames ×100 ms =6 seconds. Neither 60 frames nor 100 ms is proven to be a scoring threshold; this is a practical initial target. |
| Seamless ambient-pulse loop | Make all layers return to their starting positions/velocities; ensure last-to-first motion has the same cadence as other transitions. Avoid a duplicated endpoint pause. |
| Conference/ecosystem bonus +4.4 | Give the whale Google-colored cargo, and include a tasteful readable DEVOXX reference if it fits. The example explicitly named Devoxx and Google Cloud; Docker alone is not proven to earn that bonus. |
| Only 2/5 for aesthetic/originality | Add a distinctive character and a joke with a setup/payoff, rather than relying only on sponsor motifs. |

## Revised main entry: Ship It, Devoxx edition

Six-second story: a blue whale with Google-colored container cargo bobs in a
black ocean; its tiny duck captain presses a launch button; the yellow container
becomes a banana-shaped rocket; it loops around and docks back on the whale.
A small deliberately drawn DEVOXX pixel wordmark can anchor the conference
connection, if it remains readable and does not crowd the animation.

Use mostly black around a compact whale, a small wave line, and a few sparks.
The humor should read at actual LED size. First create the whale keyframe;
then separate layers and choreograph the loop at native resolution. Avoid
asking the image model to invent 60 consistent frames independently.

## Second entry: Forbidden Fruit

The robot/firewall banana joke gives us a more mischievous submission. Its
acceptance depends on the actual verifier. It is a creative context test;
we do not know their moderation rules or promise a pass. Prioritize readable
comedy over material that risks an unusable submission.

## Review before upload

Inspect the output GIF at native size and enlarged. Check black percentage in
the manifest, continuity on loop, palette stability, legibility of any words,
and distinct motion across frames. Technical validation cannot predict the
AI originality rating or final leaderboard rank. Review the real leaderboard
feedback after submission and make one targeted revision if needed.
