#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info

page_title="$tPageTitleNtpSettings"
%>
<%in _header.cgi %>
<%
if [ "$(cat /etc/TZ)" != "$TZ" ]; then
  alert_ "danger"
    h6 "$tMsgTimezoneNeedsUpdating"
    p "$tMsgPleaseRestart"
    button_link_to "$tButtonRestart" "/cgi-bin/reboot.cgi" "danger"
  _alert
fi

div_ "class=\"row row-cols-1 row-cols-lg-2 g-4 mb-4\""
  echo "<datalist id=\"tz_list\"></datalist>"

  col_card_ "$tHeaderTimezone"
    form_ "/cgi-bin/network-tz-update.cgi" "post"
      field_text "tz_name" "list=\"tz_list\""
      field_text "tz_data" "readonly"
      button_submit
    _form
  _col_card

  col_card_ "TimeZone Settings"
    b "# cat /etc/TZ"
    pre "$(cat /etc/TZ)"
    b "# echo $TZ"
    pre "$TZ"
    b "# date"
    pre "$(date)"
  _col_card

  col_card_ "$tHeaderNtpServers"
    form_ "/cgi-bin/network-ntp-update.cgi" "post"
      for i in 0 1 2 3; do
        x=$(expr $i + 1)
        eval "ntp_server_${i}=$(sed -n ${x}p /etc/ntp.conf | cut -d " " -f 2)"
        field_text "ntp_server_${i}" "placeholder=\"${i}.pool.ntp.org\" data-pattern=\"host-ip\""
      done
      button_submit
    _form
  _col_card

  col_card_ "NTP Settings"
    b "# cat /etc/ntp.conf"
    pre "$(cat /etc/ntp.conf)"
    button_link_to "$tButtonResetToDefaults" "/cgi-bin/network-ntp-reset.cgi" "danger"
  _col_card
_div
%>

<script src="/js/tz.js" async></script>
<script>
function findTimezone(tz) {
  return tz.name == $("#tz_name").value;
}
function updateTimezone() {
  const tz = TZ.filter(findTimezone);
  if (tz.length == 0) {
    $("#tz_data").value = "";
  } else {
    $("#tz_data").value = tz[0].value;
  }
}
function useBrowserTimezone(event) {
  event.preventDefault();
  $("#tz_name").value = Intl.DateTimeFormat().resolvedOptions().timeZone;
  updateTimezone();
}
window.addEventListener('load', () => {
  if (navigator.userAgent.includes("Android") && navigator.userAgent.includes("Firefox")) {
    const inp = $("#tz_name");
    const sel = document.createElement("select");
    sel.classList.add("form-select");
    sel.name = "tz_name";
    sel.id = "tz_name";
    sel.options.add(new Option());
    let opt;
    TZ.forEach(function(tz) {
      opt = new Option(tz.name);
      opt.selected = (tz.name == inp.value);
      sel.options.add(opt);
    });
    inp.replaceWith(sel);
  } else {
    const el = $("#tz_list");
    el.innerHTML="";
    TZ.forEach(function(tz) {
      const o = document.createElement("option");
      o.value = tz.name;
      el.appendChild(o);
    });
  }
  $("#tz_name").addEventListener("focus", ev => ev.target.select());
  $("#tz_name").addEventListener("selectionchange", updateTimezone);
  $("#tz_name").addEventListener("change", updateTimezone);
  $("#frombrowser").addEventListener("click", useBrowserTimezone);
  updateTimezone();
});
</script>
<%in _footer.cgi %>
