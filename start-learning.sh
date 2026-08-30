#!/usr/bin/env bash
# Launch the PyTorch tutoring session.
#
# Fixes the interpreter problem: pi launched from the repo root otherwise gets
# base conda (Python 3.14, no torch). This activates the `deep-learning` env
# (Python 3.11, torch 2.x + MPS), then runs pi from the repo root inside a tmux
# session named `learn` (subagents require being inside tmux).
set -euo pipefail

SESSION="learn"
ENV_NAME="deep-learning"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Locate a conda installation that carries the profile.d hook so we can activate
# an env from a non-interactive shell.
CONDA_BASE=""
if [ -n "${CONDA_EXE:-}" ] && [ -f "$(dirname "$(dirname "$CONDA_EXE")")/etc/profile.d/conda.sh" ]; then
  CONDA_BASE="$(dirname "$(dirname "$CONDA_EXE")")"
else
  for base in "$HOME/miniconda3" "$HOME/miniforge3" "$HOME/anaconda3" "/opt/homebrew/Caskroom/miniconda/base"; do
    if [ -f "$base/etc/profile.d/conda.sh" ]; then
      CONDA_BASE="$base"
      break
    fi
  done
fi

if [ -z "$CONDA_BASE" ]; then
  echo "start-learning.sh: could not locate a conda install with etc/profile.d/conda.sh" >&2
  echo "Set CONDA_EXE or edit this script's search list." >&2
  exit 1
fi

# Command that runs inside the tmux session: activate the env, cd to the repo,
# then hand off to pi. exec so pi becomes the session's foreground process.
INNER="source '$CONDA_BASE/etc/profile.d/conda.sh' && conda activate '$ENV_NAME' && cd '$REPO_ROOT' && exec pi"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  # Session already exists — attach (or switch, if we're already inside tmux).
  if [ -n "${TMUX:-}" ]; then
    exec tmux switch-client -t "$SESSION"
  else
    exec tmux attach-session -t "$SESSION"
  fi
else
  exec tmux new-session -s "$SESSION" -c "$REPO_ROOT" "$INNER"
fi
