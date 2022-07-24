#!/bin/sh

plugin="email"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

if [ ! -f "$config_file" ]; then
  echo -e "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl --url smtp://${email_smtp_server}:${email_smtp_port} \
    --mail-from ${email_from_address} \
    --mail-rcpt ${email_to_address} \
    --user ${email_smtp_login}:${email_smtp_password} \
    -F '=(;type=multipart/mixed'
    -F "=${email_body};type=text/plain" \
    -F "file=@${snapshot};type=image/jpeg;encoder=base64" \
    -F '=)' \
    -H "Subject: ${email_subject}" \
    -H "From: \"${email_from_name}\" <${email_from_address}>"
    -H "To: \"${email_to_name}\" <${email_to_address}>"
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
