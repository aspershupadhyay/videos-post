#!/usr/bin/env bash
# Upload files to VoiceBox Files (up to 2 GB each) without going through MCP.
# Usage: VOICEBOX_UPLOAD_TOKEN=... [VB_CAROUSEL=<group name>] tools/vb_upload.sh <folder id or path> <file>...
# With VB_CAROUSEL set, files are grouped as one carousel in the order given (position 1, 2, ...; VB_POSITION_START shifts the first).
# Prints "<name> <file_id> <ok|md5 mismatch>" per file. The token lives in the environment, never in git.
set -euo pipefail
# Falls back to a git-ignored .env at the repo root when the variable is not in the environment.
root=$(cd "$(dirname "$0")/.." && pwd)
if [ -z "${VOICEBOX_UPLOAD_TOKEN:-}" ] && [ -f "$root/.env" ]; then set -a; . "$root/.env"; set +a; fi
: "${VOICEBOX_UPLOAD_TOKEN:?set VOICEBOX_UPLOAD_TOKEN}"
API=https://voiceboxstudio.vercel.app/api/files
folder=$1; shift
pos=$(( ${VB_POSITION_START:-1} - 1 ))
for f in "$@"; do
  pos=$((pos+1))
  name=$(basename "$f")
  start=$(curl -sS -X POST "$API/upload" -H "Authorization: Bearer $VOICEBOX_UPLOAD_TOKEN" -H "Content-Type: application/json" \
    -d "$(python3 -c 'import json,sys; d={"name":sys.argv[1],"folder":sys.argv[2],"size":int(sys.argv[3])}; c=sys.argv[4]; d.update({"carousel":c,"position":int(sys.argv[5])} if c else {}); print(json.dumps(d))' "$name" "$folder" "$(stat -c %s "$f")" "${VB_CAROUSEL:-}" "$pos")")
  url=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["upload_url"])' <<<"$start") || { echo "$name start failed: $start" >&2; exit 1; }
  ticket=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["ticket"])' <<<"$start")
  curl -sS -f -T "$f" "$url" -o /dev/null
  # The carousel join can come back "busy" when calls land close together; completing again with the same ticket retries it.
  for try in 1 2 3 4 5 6; do
    done=$(curl -sS -X POST "$API/complete" -H "Authorization: Bearer $VOICEBOX_UPLOAD_TOKEN" -H "Content-Type: application/json" \
      -d "$(python3 -c 'import json,sys; print(json.dumps({"ticket":sys.argv[1]}))' "$ticket")")
    grep -q '"carousels are busy' <<<"$done" || break
    sleep $((try * 2))
  done
  echo "$name $done"
done
