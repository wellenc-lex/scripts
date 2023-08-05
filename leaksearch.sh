#go install -v github.com/tomnomnom/anew@latest && pip3 install leakcheck && go install -v github.com/BountyStrike/emissary@latest
#To run: /root/tools/scanwithleak.sh /root/tools/leakdomains.txt
# add to ~/.config/emissary.ini
#[Discord]
#webhook=https://discord.com/api/webhooks/ID
#textField=content
#* 11,21 * * * /root/tools/scanwithleak.sh /root/tools/leakdomains.txt
LINES=$(cat $1)
APIKEY=
TMP="/root/tools/tmp/"
for LINE in $LINES
do
	leakcheck --key "$APIKEY" "$LINE" --type domain_email -lo | sort -u >> "$TMP"newlines.txt
	cat "$TMP"newlines.txt | anew "$TMP"allresults.txt > "$TMP"added-lines.txt
	cat "$TMP"added-lines.txt | emissary --channel Discord -si -r 0
done