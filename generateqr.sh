#!/bin/bash

id=0
file="outputline.txt"

# loop through all containers
while [ $id -le 10 ]
do
  id=$((id+1))
  line=$(LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 32)
  echo "Line: $line, ID=$id"
  outfile=$(echo "$line" >> outfile.txt)
  qrcode-svg -f -o $id.svg "$line" 
done