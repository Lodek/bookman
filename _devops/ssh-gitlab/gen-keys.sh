#!/bin/sh
ssh-keygen -t rsa -N "" -b 2048 -f id_rsa
cat id_rsa | base64 --wrap=0 > id_rsa_64
