#!/bin/bash
cd "$(dirname "$0")"
SCRIPT_DIR="$( pwd )"
python3 "$SCRIPT_DIR/checkpoint.py"
