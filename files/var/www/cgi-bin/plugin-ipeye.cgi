#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
plugin="ipeye"
page_title="$tPageTitlePluginIpeye"
%>
<%in _header.cgi %>
<%
alert "$tMsgProofOfConcept" "warning"

if [ "$(yaml-cli -g .ipeye.enabled)" = "true" ]; then
  row_ "row-cols-1 row-cols-xl-2 g-4 mb-3"
    col_ "order-2 order-xl-1"
      card_ "$tHeaderAddFeed"
        form_ "#" "post"
          field_text "ipeye_login"
          field_text "ipeye_password"
          field_text "ipeye_password"
          ipeye_camera_name="$hostname"
          field_text "ipeye_camera_name"
          field_select "ipeye_rtsp_feed"
          button_submit "$tButtonAddCameraToCloud" "primary"
        _form
      _card
    _col
    col_ "order-1 order-xl-2"
      p "$(image "/img/logo-ipeye.png" "title=\"IPEYE Logo\"")"
      p "$(link_to "www.ipeye.ru" "https://www.ipeye.ru/")"
      p "Don't have an account? $(link_to "Sign-up here" "https://www.ipeye.ru/")"
    _col
  _row
%>

<script>
function handleSubmit(event) {
  event.preventDefault();
  alert("Add registraiton request to API endpoint here.");
  // API v1 doc: http://31.131.248.100/v1/
  // API v2 doc: http://api.ipeye.ru/doc
}
function initIpEyeForm() {
  $("form").addEventListener("submit", handleSubmit);
}
window.addEventListener("load", initIpEyeForm);
</script>
<%
else
  alert_ "warning"
    h4 "$tMsgIpeyeIsDisabled"
    p "$tMsgPleaseEnableIpeye"
    form_ "/cgi-bin/majestic-settings-update.cgi" "post"
      mj_ipeye_enabled="true"
      field_hidden "mj_ipeye_enabled"
      mj_go_to="$REQUEST_URI"
      field_hidden "mj_go_to"
      button_submit "$tButtonEnableIpeye" "warning"
    _form
  _alert
fi
%>
<%in _footer.cgi %>
