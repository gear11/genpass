#!/bin/python

# Should do same thing but with Python primitives
domain=$1
if [ "$domain" == "" ]; then
   echo "domain (e.g. google):"
   read domain
fi

echo "passphrase:"
read passphrase

echo "$passphrase $domain" | shasum -a 256 | xxd -r -p | base64

