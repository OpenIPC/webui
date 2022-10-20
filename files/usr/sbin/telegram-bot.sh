#!/bin/sh
#
plugin="telegram"
config_file="/etc/webui/${plugin}.conf"

if [ ! -f "$config_file" ]; then
  echo "Error: ${config_file} not found."
  exit 1
fi

# read variables from config
[ -f "$config_file" ] && source $config_file



#
#  VERY OLD SHIT TO RECYCLE !
#



api="https://api.telegram.org/bot$telegram_token"
offset_file=/tmp/telegram_offset

if [ "$telegram_enabled" == "false" ]; then
    echo "Launch of the Telegram_bot is not allowed." | logger -t "telegram_bot" -p daemon.info
    exit 1
fi

keyboard='{"keyboard": [["/snap \uD83D\uDCF7","/guard \uD83D\uDC6E","/relay \uD83D\uDCA1"],["/system \uD83D\uDCCA","/reboot \uD83D\uDCA9","/start \uD83D\uDD25"]],"resize_keyboard":true,"one_time_keyboard":false}'
#curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d chat_id=$telegram_channel -d parse_mode=Markdown --data-urlencode text="OpenIPC device started." >/dev/null 2>&1
#curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d chat_id=$telegram_channel -d "reply_markup=${keyboard}" -d "text=Please insert command:" >/dev/null 2>&1
curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d chat_id=$telegram_channel -d "reply_markup=${keyboard}" >/dev/null 2>&1

polling_timeout=30
offset=0
if [ -f "$offset_file" ]; then
    offset=$( cat $offset_file )
else
    echo $offset > $offset_file
fi

reply_to_msg () {
    msg_id=$1
    origin=$2
    eval toReturn="$3"
    curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d reply_to_message_id=$msg_id -d chat_id=$origin -d parse_mode=HTML --data-urlencode text="$toReturn" >/dev/null 2>&1
}

while [ true ]
do
	updates=$(curl -s -X GET ${api}/getUpdates?offset=${offset}&timeout=${polling_timeout})
	status=$(jsonfilter -s "$updates" -e $.ok)
	if [ $status = 'true' ]; then
		update_ids=$(jsonfilter -s "$updates" -e $.result[*].update_id)
		for update_id in $update_ids
		do
			offset=$((update_id+1))
			echo $offset > $offset_file
			origin=$(jsonfilter -s "$updates"  -e "$.result[@.update_id=$update_id].message.chat.id")
			msg_id=$(jsonfilter -s "$updates"  -e "$.result[@.update_id=$update_id].message.message_id")
			command=$(jsonfilter -s "$updates" -e "$.result[@.update_id=$update_id].message.text")
			is_a_cmd=$(jsonfilter -s "$updates" -e "$.result[@.update_id=$update_id].message.entities[*].type")
			query_ans=$(jsonfilter -s "$updates" -e "$.result[@.update_id=$update_id].callback_query.id")
			origin_ans=$(jsonfilter -s "$updates"  -e "$.result[@.update_id=$update_id].callback_query.message.chat.id")
			if [[ "$origin" != "$telegram_channel" && "$origin_ans" != "$telegram_channel" ]];then
				curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d reply_to_message_id=$msg_id -d chat_id=$origin -d parse_mode=Markdown --data-urlencode text="This is a Private bot." >/dev/null 2>&1
				curl -s -X POST $api/leaveChat -d chat_id=$origin >/dev/null 2>&1
			else
				if [ "$is_a_cmd" ==  "bot_command" ]; then
					cmd=$(echo $command |  awk '{print $1}')
					DATE=`date +%Y-%m-%d_%H:%M:%S`
					case "$cmd" in
						("/guard")
							echo "[ $DATE ] Run /guard command !" | logger -t "telegram_bot" -p daemon.info
							informex_guard=$("tg_guard.sh")
							reply_to_msg $msg_id $origin "\${informex_guard}"
							;;
						("/start")
							echo "[ $DATE ] Run /menu command !" | logger -t "telegram_bot" -p daemon.info
							curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d chat_id=$telegram_channel -d "reply_markup=${keyboard}" -d "text=Please insert command:" >/dev/null 2>&1
							;;
						("/reboot")
                            reboot -f
                            ;;
						("/relay")
							echo "[ $DATE ] Run /relay command !" | logger -t "telegram_bot" -p daemon.info
							informex_relay=$("tg_relay.sh")
							reply_to_msg $msg_id $origin "\${informex_relay}"
							;;
						("/snap")
                            send2telegram.sh
                            ;;
						("/system")
                            curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d chat_id=$telegram_channel -d "reply_markup=${keyboard}" -d "text=$(cat /etc/os-release)" >/dev/null 2>&1
                            ;;
						(*)
							echo "[ $DATE ] $cmd command not enabled" | logger -t "telegram_bot" -p daemon.info
							informex_unknown="This command is not enabled."
							reply_to_msg $msg_id $origin "\${informex_unknown}"
							;;
					esac
				#else
				#	curl -s -X POST -H "Charset: UTF-8" $api/sendMessage -d reply_to_message_id=$msg_id -d chat_id=$origin -d parse_mode=Markdown --data-urlencode text="Is not a command." >/dev/null 2>&1
				fi
			fi
		done
	fi
	sleep 1
done &
