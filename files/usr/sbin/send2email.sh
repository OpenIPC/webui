#!/bin/sh

plugin="email"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

mkdir -p /tmp/webui

if [ ! -f "$config_file" ]; then
  echo "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file

if [ "true" != "$email_enabled" ]; then
  echo "Sending to email is not enabled."
  exit 10
fi

# validate mandatory values
[ -z "$email_smtp_host"    ] && echo -e "SMTP host not found in config" && exit 11
[ -z "$email_smtp_port"    ] && echo -e "SMTP port not found in config" && exit 12
[ -z "$email_from_address" ] && echo -e "Sender's address not found in config" && exit 13
[ -z "$email_to_address"   ] && echo -e "Recipient's address not found in config" && exit 14

# assign default values if not set
[ -z "$email_from_name" ] && email_from_name="OpenIPC Camera"
[ -z "$email_to_name"   ] && email_to_name="OpenIPC Camera Admin"
[ -z "$email_subject"   ] && email_subject="Snapshot from OpenIPC Camera"
[ -z "$email_body"      ] && email_body="$(date)"

curl_options="--verbose --silent --connect-timeout ${curl_timeout} --max-time ${curl_timeout}"

if [ "true" = "$email_smtp_use_ssl" ]; then
  curl_options="--ssl"
  email_smtp_protocol="smtps"
else
  email_smtp_protocol="smtp"
fi

if [ -n "$email_smtp_login" ] || [ -n "$email_smtp_password" ]; then
  curl_options="${curl_options} --user ${email_smtp_login}:${email_smtp_password}"
fi

snapshot="/tmp/${plugin}_snap.jpg"

# get image from camera
curl "http://127.0.0.1/image.jpg?t=$(date +"%s")" --output "$snapshot" --silent
if [ $? -eq 0 ]; then
  curl ${curl_options} \
    --url ${email_smtp_protocol}://${email_smtp_host}:${email_smtp_port} \
    --mail-from ${email_from_address} \
    --mail-rcpt ${email_to_address} \
    -F '=(;type=multipart/mixed' \
    -F "=${email_body};type=text/plain" \
    -F "file=@${snapshot};type=image/jpeg;encoder=base64" \
    -F '=)' \
    -H "Subject: ${email_subject}" \
    -H "From: \"${email_from_name}\" <${email_from_address}>" \
    -H "To: \"${email_to_name}\" <${email_to_address}>" \
    >/tmp/webui/${plugin}.log 2>&1
  rm -f ${snapshot}
else
  echo "Cannot get a snapshot."
  exit 2
fi

exit 0
