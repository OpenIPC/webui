#!/bin/sh

plugin="yucca"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

if [ "true" != "$yucca_enabled" ]; then
  echo "Sending to Yucca is not enabled."
  exit 10
fi

# validate mandatory values
[ -z "$yucca_host"    ] && echo -e "Yucca host not found in config" && exit 11
[ -z "$yucca_port"    ] && echo -e "Yucca port not found in config" && exit 12
[ -z "$yucca_address" ] && echo -e "Yucca address not found in config" && exit 13

echo -e "EHLO ${yucca_host}\nMAIL FROM: ${yucca_address}\nRCPT TO: ${yucca_address}\nQUIT" | nc ${yucca_host} ${yucca_port}
