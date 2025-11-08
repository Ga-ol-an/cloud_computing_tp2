#!/usr/bin/env bash

# This code measures the time taken for a specific API response to change
# It was run on my machine with the K8s cluster deployed on the server,
# with the input redirected via SSH tunnel.

# Use the following to access the service locally:
# ssh -L 50010:localhost:50010 usuario@10.43.155.95 

# The version was changed to 1.0.1 manually and github will push it

git add .
git commit -m "[TP2] Measurement test script to monitor version changes"
git push

URL="http://10.43.155.95:50010/api/recommend"
PAYLOAD='{"songs": ["Broccoli (feat. Lil Yachty)", "Bad and Boujee (feat. Lil Uzi Vert)", "Mask Off"]}'
OLD_VERSION="1.0.0"


START=$(date +%s)
while true; do
  RESPONSE=$(curl -s -X POST -H "Content-Type: application/json" -d "$PAYLOAD" "$URL" --max-time 3)
  STATUS=$?
  NOW=$(date +%s)
  ELAPSED=$((NOW - START))

  if [ $STATUS -ne 0 ] || [ -z "$RESPONSE" ]; then
    echo "${ELAPSED}s | downtime"
  else
    CURR_VERSION=$(echo "$RESPONSE" | grep -oP '"version"\s*:\s*"\K[^"]+')
    echo "${ELAPSED}s | version: ${CURR_VERSION}"
    if [ "$CURR_VERSION" != "$OLD_VERSION" ] && [ -n "$CURR_VERSION" ]; then
      echo "Version changed to ${CURR_VERSION} after ${ELAPSED}s"
      break
    fi
  fi

  sleep 1
done