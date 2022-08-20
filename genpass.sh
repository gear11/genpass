#!/bin/bash

# A simplified, bash-based version of genpass which has none of the features of the Python
# version but does demonstrate that the basic hash algorithm in Python is compatible with
# command line tools
domain=$1
if [ "$domain" == "" ]; then
   echo "domain (e.g. google):"
   read domain
fi

echo "passphrase:"
read passphrase

echo "$passphrase $domain" | shasum -a 256 | xxd -r -p | base64

