#!/usr/bin/env bash
set -euo pipefail

pyinstaller --onefile test.py
