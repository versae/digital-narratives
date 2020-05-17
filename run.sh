#!/bin/bash
rm -rf images
mkdir images
python extract.py
pixplot --images "images/*.jpg" --metadata metadata.csv
# --pointgrid_fill 0.15
rm -rf docs
mv output docs
cp style.css docs/assets/css/style.css
cp CNAME docs/CNAME
rm -rf tmp/images
mv images tmp/
mv metadata.csv tmp/metadata.csv
