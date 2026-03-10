#!/usr/bin/env bash

set -e

# Assuming in top yannt path (PROJ_PATH)

# Allow user to assign venv name and tag shell prompt
ML_VENV_NAME=${ML_VENV_NAME:-ml-venv}

export PS1_TAG=${PS1_TAG:-"(${ML_VENV_NAME}) "}
export PS1="${PS1_TAG}${PS1:-\$ }"

source ./cache/venv/${ML_VENV_NAME}/bin/activate

if [ $# -gt 0 ]; then

$@

else

echo
echo "The environment is now ready. Try 'yannt --help' for information."

# Include yannt tab completion.
TMP_RC="$(mktemp)"
cat >> "$TMP_RC" <<'EOF'
[ -f "$HOME/.bashrc" ] && source $HOME/.bashrc
source ./cache/venv/${ML_VENV_NAME}/bin/activate
eval "$(register-python-argcomplete yannt)"
EOF

exec bash --rcfile "$TMP_RC" -i

fi