#!/usr/bin/env bash

set -e

PROJ_PATH=$(realpath $(dirname $0)/..)
cd $PROJ_PATH

# Allow user to assign venv name and tag shell prompt
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}

export PS1_TAG=${PS1_TAG:-"(${ML_VENV_NAME}) "}
export PS1="${PS1_TAG}${PS1:-\$ }"

source ${PROJ_PATH}/cache/venv/${ML_VENV_NAME}/bin/activate

echo
echo "The environment is now ready. Try 'yannt --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
[ -f "~/.bashrc" ] && source ~/.bashrc
eval "$(register-python-argcomplete yannt)"
EOF

exec bash --rcfile "$TMP_RC" -i
