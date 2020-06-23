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
# Custom text and logos
rpl "PixPlot" "<a href='http://barrxcnn.hdplus.es/'>Barr X Inception CNN</a>" docs/index.html
rpl "https://dhlab.yale.edu" "https://iarthislab.es/" docs/index.html
cp iarthis_logo_uma.png docs/assets/images/logo.png
rpl "<img id='logo' src='assets/images/dhlab-logo.svg' alt='DHLab logo' />" "<img id='logo' src='assets/images/logo.png' alt='iArtHis_Lab' />" docs/index.html
rpl "Douglas Duhaime" "Javier de la Rosa" docs/index.html
rpl "Visualizing Image Fields" "Barr X Inception CNN" docs/index.html
