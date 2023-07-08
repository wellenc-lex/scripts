LINES=$(cat $1)
for LINE in $LINES
do
	VHostScan --fuzzy-logic -t "$LINE" --ssl -p 443 --rate-limit 1 >> out"$LINE".txt &
	VHostScan --fuzzy-logic -t "$LINE" -p 80 --rate-limit 1 >> out"$LINE".txt &
done
