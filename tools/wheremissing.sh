#!/bin/bash
#
# Script to find position of empty files on scene_TLs
# It requires GNU tools
 
grep -n ^$'\r' ../scene_TLs/*.txt

