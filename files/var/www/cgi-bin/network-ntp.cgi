#!/usr/bin/haserl
<%
page_title="NTP Settings"
tz=$(cat /etc/TZ)
interfaces=$("/sbin/ifconfig | grep '^\w' | awk {'print $1'}")
%>
<%in _header.cgi %>
<h2>NTP Settings</h2>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
  <div class="col">
    <div class="card mb-3">
      <div class="card-body">
        <pre><% cat /etc/ntp.conf %></pre>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Timezone</h5>
      <!-- https://raw.githubusercontent.com/openwrt/luci/master/modules/luci-base/luasrc/sys/zoneinfo/tzdata.lua -->
      <div class="card-body">
        <form action="/cgi-bin/network-tz-update.cgi" method="post">
          <div class="row">
            <label class="col-md-4" for="tz_name" class="form-label">Zone name</label>
            <div class="col-md-8"><select class="form-select" name="tz_name" id="tz_name"></select></div>
          </div>
          <div class="row">
            <label class="col-md-4" for="tz_data" class="form-label">Zone string</label>
            <div class="col-md-8"><input type="text" class="form-control" name="tz_data" id="tz_data" value="<%= $tz_data %>" readonly></div>
          </div>
          <button type="submit" class="btn btn-primary">Save changes</button>
        </form>
      </div>
    </div>
  </div>

  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">NTP Servers</h5>
      <div class="card-body">
        <form action="/cgi-bin/network-ntp-update.cgi" method="post">
          <%
            for i in 0 1 2 3; do
              x=$(expr $i + 1)
              ip=$(sed -n ${x}p /etc/ntp.conf | cut -d " " -f 2)
              echo "<div class=\"row mb-1\">"
              echo "<label class=\"col-md-5 form-label\" for=\"ntp_server_${i}\">NTP Server ${x}</label>"
              echo "<div class=\"col-md-7\">"
              echo "<input class=\"form-control pat-host-ip\" type=\"text\" name=\"ntp_server[${i}]\" id=\"ntp_server_${i}\" value=\"${ip}\" placeholder=\"${i}.pool.ntp.org\">"
              echo "</div>"
              echo "</div>"
            done
          %>
          <button type="submit" class="btn btn-primary">Save changes</button>
        </form>
      </div>
    </div>
  </div>
</div>
<script src="/tz.js" async></script>
<script>
function updateTimezone() {
  $('#tz_data').value = $('#tz_name').selectedOptions[0].value
}
window.addEventListener('load', () => {
  const el = $('#tz_name');
  el.innerHTML='';
  for (i in TZ) el.options.add(new Option(TZ[i][0], TZ[i][1], true, (TZ[i][1] == "<%= $tz %>")));
  el.addEventListener('change', updateTimezone);
  updateTimezone();
});
</script>
<%in _footer.cgi %>
