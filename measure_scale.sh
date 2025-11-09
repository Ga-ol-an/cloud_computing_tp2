#!/bin/bash
export KUBECONFIG="$HOME/.kube/config"

t0=$(date +%s)

while :; do
  avail=$(kubectl -n gabrielandrade get deploy song-recommender-goa-deployment-ds1-v1.0.2 -o jsonpath='{.status.availableReplicas}')
  [[ -z "$avail" ]] && avail=0
  echo "t=$(($(date +%s)-t0))s  available=$avail/2"
  [[ "$avail" -ge 2 ]] && break
  sleep 1
done
echo "DONE in $(($(date +%s)-t0))s"