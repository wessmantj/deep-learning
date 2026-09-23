---
name: learn
description: Start (or resume) a PyTorch tutoring session. Invoke when the user types /learn, or says "let's learn", "continue learning", "teach me", or otherwise wants to begin a study session in this repo.
---

# Start a learning session

This kicks off a personal PyTorch tutoring session that runs on the Claude Code plan (no API credits). The full teaching methodology lives in the `teach` skill — invoke it and follow it exactly.

Do this now, in order:

1. **Invoke the `teach` skill** and follow its four-phase process (probe → plan → teach → update).
2. **Read the repo-root `STATE.md`** — this is Phase 1, step 0. Load where his edge sits on each strand, which misconceptions are live, what's due for spaced review, and the current goal. Flag any still-live misconception and any node whose review is due for re-check first.
3. **Open with a warm continuation, not a cold remap.** Briefly tell him where you two left off (from STATE.md) and what's on deck today, then run a short confirmation probe at his recorded edge before teaching new ground. Never march him back up to failure through material STATE.md already says he owns.
4. **At session end**, run the `teach` skill's Phase 4 — update `STATE.md` truthfully (edges moved, misconceptions dislodged/still-live, nodes taught + review dates, goal). Never skip this; next session's warm start depends on it.

If he named a specific topic when invoking (e.g. `/learn dataloaders`), aim the session there, but still read STATE.md first so you build from his real edge.
