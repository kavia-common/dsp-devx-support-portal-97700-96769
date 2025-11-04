#!/bin/bash
cd /home/kavia/workspace/code-generation/dsp-devx-support-portal-97700-96769/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

