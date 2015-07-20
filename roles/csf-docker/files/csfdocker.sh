#!/bin/sh
iptables -C ALLOWOUT -o docker0 -j ACCEPT 2> /dev/null
if [ $? = 1 ]; then
    iptables -A ALLOWOUT -o docker0 -j ACCEPT
fi

iptables -C FORWARD ! -i docker0 -j LOCALINPUT 2> /dev/null
if [ $? = 1 ]; then
    iptables -I FORWARD ! -o docker0 -p tcp -j INVALID
    iptables -I FORWARD ! -o docker0 -j LOCALOUTPUT
    iptables -I FORWARD ! -i docker0 -p tcp -j INVALID
    iptables -I FORWARD ! -i docker0 -j LOCALINPUT
fi
