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

# validate mandatory values
[ -z "$email_smtp_server"  ] && echo -e "SMTP server not found in config" && exit 2
[ -z "$email_smtp_port"    ] && echo -e "SMTP port not found in config" && exit 2
[ -z "$email_from_address" ] && echo -e "Sender's address not found in config" && exit 2
[ -z "$email_to_address"   ] && echo -e "Recipient's address not found in config" && exit 2

# assign default values if not set
[ -z "$email_from_name" ] && email_from_name="OpenIPC Camera"
[ -z "$email_to_name"   ] && email_to_name="OpenIPC Camera Admin"
[ -z "$email_subject"   ] && email_subject="Snapshot from OpenIPC Camera"
[ -z "$email_body"      ] && email_body="$(date)"

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl --url smtp://${email_smtp_server}:${email_smtp_port} --mail-from ${email_from_address} --mail-rcpt ${email_to_address} --user ${email_smtp_login}:${email_smtp_password} \
    -F '=(;type=multipart/mixed' -F "=${email_body};type=text/plain" -F "file=@${snapshot};type=image/jpeg;encoder=base64" -F '=)' \
    -H "Subject: ${email_subject}" -H "From: \"${email_from_name}\" <${email_from_address}>" -H "To: \"${email_to_name}\" <${email_to_address}>"
else
  echo "Cannot get a snapshot."
  exit 1
fi

exit 0
