#!/usr/bin/env bash

echo RUNNING BUILD_MODE="${BUILD_MODE}" PROJ_PATH="${PROJ_PATH}" $0 $@

set -e

# --------- Guard Against Uninitialized Environments -------

if [ -z "${PROJ_PATH}" ]; then
  echo "Please run via ./scripts/run-dev.sh."
  exit 1
fi

${PROJ_PATH}/cache/builder/${CONFIG_NAME}/host/podman/run-podman.sh

#source ${CONFIG_PATH}/config.env

# python3 - "$@" <<'EOF'
# #!/usr/bin/env python3

# import os
# import sys
# import json
# import subprocess

# proj_path = os.getenv('PROJ_PATH')
# if proj_path is None:
#     print("Please run via ./scripts/run-dev.sh.")
#     exit(1)

# # Safely pass the $@ to build-env.py
# cmd = [
#   './scripts/_/build-env.py', '--run',
#   '--config_name', os.getenv('CONFIG_NAME'),
#   '--proj_path', os.getenv('PROJ_PATH'),
#   '--config_path', os.getenv('CONFIG_PATH')
# ]
# if len(sys.argv) > 1:
#   cmd.extend(['--extra', json.dumps(sys.argv[1:])])

# subprocess.run(cmd, capture_output=True, text=True)
# EOF

# Forward to generic script.
#${CONFIG_PATH}/run.py $@

