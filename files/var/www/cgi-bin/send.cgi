#!/usr/bin/haserl
<%in p/common.cgi %>
<%
target="$GET_to"
if [ -n "$(echo "email ftp openwall telegram yadisk webhook" | sed -n "/\b${target}\b/p")" ]; then
	/usr/sbin/snapshot4cron.sh -f >/dev/null
	[ "openwall" = "$target" ] && opts="-f"
	/usr/sbin/send2${target}.sh ${opts} >/dev/null
	redirect_back "success" "Sent to ${target}."
elif [ "pastebin" = "$target" ]; then
	if [ "mjlog" = "$GET_file" ]; then
		t=$(mktemp)
		logread | grep 'user.info majestic' >$t
		url=$(/usr/sbin/send2${target}.sh $t)
		rm $t
		unset t
		redirect_to $url
	fi
else
	redirect_back "danger" "Unknown target ${target}!"
fi
%>
