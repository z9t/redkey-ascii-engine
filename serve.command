#!/bin/bash
cd "$(dirname "$0")"
pgrep -f "http.server 8745" >/dev/null || (python3 -m http.server 8745 >/dev/null 2>&1 &)
sleep 1
open "http://localhost:8745/redkey-ascii-morph.html"
