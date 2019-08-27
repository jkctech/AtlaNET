#!/bin/bash
rtl_fm -f 169.65M -M fm -s 22050 | multimon-ng -q -a FLEX -t raw /dev/stdin