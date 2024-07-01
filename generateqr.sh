#!/bin/bash

id=0
summa="10 000 рублей, если ваш отчет подлежит оплате."
count=99
file="outputline.txt"

promo="
Ваш промокод: "

text="

Найдите уязвимость и отправьте отчет в , указав промокод в описании. 

Вы получите бонус к вознаграждению в размере"

mkdir $count
while [ $id -le $count ]
do
  id=$((id+1))
  code=$(LC_ALL=C tr -dc A-Za-z0-9 </dev/urandom | head -c 32)
  echo "Line: $code, ID=$id"
  outfile=$(echo "$code" >> $count/outfile.txt)
  qrcode-svg -f -o $count/$id.svg "$promo $code $text $summa" 
done