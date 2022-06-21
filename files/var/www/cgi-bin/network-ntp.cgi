#!/usr/bin/haserl
<%in _common.cgi %>
<% page_title="$t_ntp_0" %>
<%in _header.cgi %>

<% if [ "$(cat /etc/TZ)" != "$TZ" ]; then %>
<div class="alert alert-danger">
  <h6><%= $t_ntp_1 %></h6>
  <p><%= $t_ntp_2 %></p>
  <% button_link_to "$t_ntp_3" "/cgi-bin/reboot.cgi" "danger" %>
</div>
<% fi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-xxl-4 g-3 mb-3">
<datalist id="tz_list"></datalist>
<% 
col_card_ "$t_ntp_4"
form_ "/cgi-bin/network-tz-update.cgi"
field_text "tz_name" "" "list=tz_list"
field_text "tz_data" "" "readonly"
button_submit "$t_btn_submit" "primary"
_form
_col_card

col_card_ "t_ntp_5"
ex "cat /etc/TZ"
ex "cat /etc/tz_name"
ex "echo \$TZ"
ex "/bin/date"
_col_card

col_card_ "$t_ntp_6"
form_ "/cgi-bin/network-ntp-update.cgi"
for i in 0 1 2 3; do
  x=$(expr $i + 1)
  eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d' ' -f2)"
  field_text "ntp_server_${i}" "placeholder=\"${i}.pool.ntp.org\" data-pattern=\"host-ip\""
done
button_submit "$t_btn_submit" "primary"
_form
_col_card

col_card_ "$t_ntp_7"
ex "cat /etc/ntp.conf"
button_link_to "$t_ntp_8" "/cgi-bin/network-ntp-reset.cgi" "danger"
_col_card
%>
</div>
<script src="/a/tz.js"></script>
<%in p/footer.cgi %>
