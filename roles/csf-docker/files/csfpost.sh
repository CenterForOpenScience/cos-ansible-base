#!/bin/sh
iptables -N DOCKER
iptables -A DOCKER ! -i docker0 -o docker0 -j LOCALINPUT
iptables -A DOCKER ! -i docker0 -o docker0 -p tcp -j INVALID
iptables -A DOCKER -i docker0 ! -o docker0 -j LOCALOUTPUT
iptables -A DOCKER -i docker0 ! -o docker0 -p tcp -j INVALID
