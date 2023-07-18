LINES=$(cat $1)
BASE=" "
WORDLIST=" "
id=0
if [ -n "$2" ]; then
	BASE=" -b $2"
fi

if [ -n "$3" ]; then
	WORDLIST=" -w $3"
fi

for LINE in $LINES
do
	id=$((id+1))
	VHostScan --fuzzy-logic -t "$LINE" --ssl -p 443 --rate-limit 1 $BASE $WORDLIST >> out/"$id".txt &
	VHostScan --fuzzy-logic -t "$LINE" -p 80 --rate-limit 1 $BASE $WORDLIST >> out/"$id".txt &
done