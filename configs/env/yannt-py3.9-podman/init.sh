#!/usr/bin/env bash

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/init-dev.sh."
  exit 1
fi

source ${CONFIG_PATH}/config.env

python3 - "$@" <<'EOF'
#!/usr/bin/env python3

import os
import sys
import json
import subprocess

from pathlib import Path

# We don't determine proj_path ourselves because we want the user to call init-dev.sh
#proj_path=os.path.realpath(os.path.join(os.path.dirname(__file__), '../../..'))
proj_path = os.getenv('PROJ_PATH')
if proj_path is None:
    print("Please run via ./scripts/init-dev.sh.")
    exit(1)

# Safely pass the $@ to build-env.py
# '--plan', Path(os.getenv('CONFIG_PATH')) / 'plan.yaml',
cmd = [
  './scripts/_/build-env.py', '--init',
  '--config_name', os.getenv('CONFIG_NAME'),
  '--proj_path', os.getenv('PROJ_PATH'),
  '--config_path', os.getenv('CONFIG_PATH'),
]
if len(sys.argv) > 1:
  cmd.extend(['--extra', json.dumps(sys.argv[1:])])
subprocess.run(cmd)
EOF

${PROJ_PATH}/cache/builder/${CONFIG_NAME}/host/init-host.sh