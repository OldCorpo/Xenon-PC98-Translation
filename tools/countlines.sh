#!/bin/bash
#
# Script to count the mising lines on scene translations
# It requires GNU tools
 
echo "Counting lines on the scene_TLs folder."
echo ""

grep -c ^$'\r' ../scene_TLs/*.txt

