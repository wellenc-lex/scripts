#* * * * * /root/tools/checkipVPN.sh > /root/tools/tmp/outvpn.txt
VPNip=`timeout 10 purevpn-cli --info | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}"`
curl=`curl -s -k --max-time 80 --connect-timeout 80 2ip.ru`
echo $curl

if [ "$curl" != "$VPNip" ]; then
    echo IP mismatch
    docker pause $(docker container ls -q)
    pkill -f "openvpn"
    purevpn-cli -c FI
fi

if [ "$curl" == "$VPNip" ]; then
    echo OK
    docker unpause $(docker container ls -q)
fi