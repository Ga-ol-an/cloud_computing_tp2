#!/bin/bash

git add .
git commit -m "[TP2] Measurement test script to monitor change nb of replicas"
git push


ssh gabrielandrade@cloudvm2 "bash ~/measure_scale.sh"
