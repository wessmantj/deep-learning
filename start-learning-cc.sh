#!/usr/bin/env bash
# Launch the PyTorch tutoring session on Claude Code (runs on the plan, NOT API
# credits — unlike the old pi-based ./start-learning.sh).
#
# Fixes the interpreter problem: a shell launched from the repo root otherwise
# gets base conda (Python 3.14, no torch). This activates the `deep-learning`
# env (Python 3.11, torch 2.x + MPS), cd's to the repo, then hands off to
# `claude` so torch/MPS is importable in the interactive window during lessons.
#
# Once inside, type `/learn` to start or resume a session.
set -euo pipefail

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
  echo "start-learning-cc.sh: could not locate a conda install with etc/profile.d/conda.sh" >&2
  echo "Set CONDA_EXE or edit this script's search list." >&2
  exit 1
fi

if ! command -v claude >/dev/null 2>&1; then
  echo "start-learning-cc.sh: 'claude' CLI not found on PATH." >&2
  echo "Install Claude Code, or run 'claude' however you normally do." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "$CONDA_BASE/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"
cd "$REPO_ROOT"

echo "Env '$ENV_NAME' active. Starting Claude Code — type /learn to begin."
exec claude
