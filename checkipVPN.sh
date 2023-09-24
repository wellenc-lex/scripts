#* * * * * /root/tools/checkipVPN.sh >> /root/tools/tmp/outvpn.txt
VPNip=`timeout 15 /opt/purevpn-cli/bin/purevpn-cli --info | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}"`
curl=`/usr/bin/curl -s -k --max-time 80 --connect-timeout 80 2ip.ru`

if [ "$curl" != "$VPNip" ]; 
then
    echo $VPNip
    echo $curl
    echo IP mismatch
    /usr/bin/docker pause $(/usr/bin/docker container ls -q) >/dev/null
    timeout 30 yes|/usr/bin/sudo /opt/purevpn-cli/bin/purevpn-cli -d && /usr/bin/pkill -f "openvpn"
    connect=`timeout 40 yes|/usr/bin/sudo /opt/purevpn-cli/bin/purevpn-cli -c FI`
    echo $connect
else
    #echo OK
    /usr/bin/docker unpause $(/usr/bin/docker container ls -q) >/dev/null
fi
