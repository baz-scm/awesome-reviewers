---
title: Explicit logging for channels
description: 'When log behavior depends on configuration (e.g., `WARP_CHANNEL`) or
  when scripts auto-select an environment/tool (e.g., which Xcode app to use), make
  the behavior explicit and observable:'
repository: warpdotdev/warp
label: Logging
language: Other
comments_count: 2
repository_stars: 56893
---

When log behavior depends on configuration (e.g., `WARP_CHANNEL`) or when scripts auto-select an environment/tool (e.g., which Xcode app to use), make the behavior explicit and observable:

- Handle known values with clear conditional branches (use `elif` for each supported channel/value).
- For any unrecognized/unsupported configuration, emit a warning log so issues are diagnosable.
- Log the chosen option (selected log file, selected Xcode candidate/path, etc.) so users can verify what the script did.

Example pattern (channel-aware log file selection):
```sh
if [ "$WARP_CHANNEL" = "local" ]; then
  LOG_FILE=~/Library/Logs/warp_local.log
elif [ "$WARP_CHANNEL" = "oss" ]; then
  LOG_FILE=~/Library/Logs/warp_oss.log
else
  echo "Warning: unrecognized WARP_CHANNEL='$WARP_CHANNEL'" >&2
  LOG_FILE=~/Library/Logs/warp.log
fi

echo "Using log file: $LOG_FILE"
```