#!/usr/bin/haserl
<%in _common.cgi %>
<%
plugin="bigbro"
page_title="$tPageTitlePluginBigbro"
config_file="/etc/${plugin}.cfg"
[ ! -f "$config_file" ] && touch ${config_file}

if [ -n "$POST_pin" ]; then
  pin="$POST_pin"
  signature=$(echo -ne "$pin" | md5sum | awk '{print $1}')
  sed -d /^${pin}:/ ${config_file}
  echo "${pin}:${signature}" >> ${config_file}
  redirect_to "?pin=${pin}"
fi
%>
<%in _header.cgi %>
<%
alert "$tMsgProofOfConcept" "warning"

if [ -n "$GET_new" ]; then
  page_title="$tPageTitlePluginBigbroAddDevice"
  row_ "row-cols-1 row-cols-xl-2 g-4 mb-3"
    col_card_ "$tHeaderAddDevice"
      form_ "/cgi-bin/plugin-bigbro.cgi" "post" "enctype=\"multipart/form-data\""
        p "$tTextAccessPin"
        field_text "bigbro_pin" "pattern=\"[A-Za-z0-9]+\""
        button_submit "$tButtonAddDevice" "primary"
      _form
    _col_card
  _row
elif [ -n "$GET_pin" ]; then
  pin="$GET_pin"
  signature=$(grep "^${pin}" ${config_file} | cut -d: -f2)
  h3 "$pin"
  p "$signature"
  link_to "List of devices" "?"
else
  h3 "List of devices"
  link_to "add a device" "?new=device"
  dl_
    for device in $(cat ${config_file}); do
      dt "$(link_to "${device%:*}" "?pin=${device%:*}")"
      dd "${device##*:}"
    done
  _dl
fi
%>
<%in _footer.cgi %>
