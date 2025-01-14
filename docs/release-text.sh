#!/bin/sh

lines=$(grep -n -m2 -- "---" docs/changelog.txt | cut -d: -f1)

first=$(( $(echo $lines | cut -d' ' -f1) + 1 ))
last=$(( $(echo $lines | cut -d' ' -f2) - 2 ))

cat docs/changelog.txt | head -n$last | tail -n+$first

