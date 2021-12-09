#!/usr/bin/haserl
<%
page_title="NTP Settings"
tz_data=$(cat /etc/TZ)
tz_name=$(cat /etc/tzname)
interfaces=$("/sbin/ifconfig | grep '^\w' | awk {'print $1'}")
%>
<%in _header.cgi %>
<h2>NTP Settings</h2>

<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header">Timezone</h5>
      <!-- https://raw.githubusercontent.com/openwrt/luci/master/modules/luci-base/luasrc/sys/zoneinfo/tzdata.lua -->
      <div class="card-body">
        <form action="/cgi-bin/network-tz-update.cgi" method="post">
          <div class="row mb-1">
            <label class="col-md-4 form-label" for="tz_name">Zone name</label>
            <div class="col-md-8">
              <input class="form-select" name="tz_name" id="tz_name" list="tz_list" value="<%= $tz_name %>">
              <datalist id="tz_list"></datalist>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-4 form-label" for="tz_data">Zone string</label>
            <div class="col-md-8">
              <input type="text" class="form-control" name="tz_data" id="tz_data" value="<%= $tz_data %>" readonly>
            </div>
          </div>
          <button type="submit" class="btn btn-primary mt-2">Save changes</button>
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
          <button type="submit" class="btn btn-primary mt-2">Save changes</button>
        </form>
      </div>
      <div class="card-body">
        <b># cat /etc/ntp.conf</b>
        <pre><% cat /etc/ntp.conf %></pre>
      </div>
    </div>
  </div>
</div>

<script src="/tz.js" async></script>
<script>
function findTimezone(tz) {
  return tz.name == $('#tz_name').value;
}
function updateTimezone() {
  const tz = TZ.filter(findTimezone);
  if (tz.length == 0) {
    $('#tz_data').value = '';
  } else {
    $('#tz_data').value = tz[0].value;
  }
}
window.addEventListener('load', () => {
  const el = $('#tz_list');
  el.innerHTML='';
  TZ.forEach(function(tz) {
    const o = document.createElement('option');
    o.value = tz.name;
    el.appendChild(o);
  });
  $('#tz_name').addEventListener('selectionchange', updateTimezone);
  updateTimezone();
});
</script>
<%in _footer.cgi %>
