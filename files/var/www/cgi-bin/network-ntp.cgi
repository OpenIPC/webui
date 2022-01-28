#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info

page_title="$tPageTitleNtpSettings"

check_env_tz() {
  if [ "$(cat /etc/TZ)" != "$TZ" ]; then
    echo "<div class=\"alert alert-danger\">" \
      "<p><b>$tMsgTimezoneNeedsUpdating</b> $tMsgPleaseRestart</p>" \
      "<a class=\"btn btn-danger\" href=\"/cgi-bin/reboot.cgi\">$tButtonRestart</a>" \
      "</div>"
  fi
}
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header"><%= $tHeaderTimezone %></h5>
      <div class="card-body">
        <form action="/cgi-bin/network-tz-update.cgi" method="post">
          <div class="row mb-1">
            <label class="col-md-4 form-label" for="tz_name"><%= $tLabelZoneName %></label>
            <div class="col-md-8">
              <input class="form-control" name="tz_name" id="tz_name" list="tz_list" value="<%= $tz_name %>">
              <datalist id="tz_list"></datalist>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-4 form-label" for="tz_data"><%= $tLabelZoneData %></label>
            <div class="col-md-8">
              <input type="text" class="form-control" name="tz_data" id="tz_data" value="<%= $tz_data %>" readonly>
            </div>
          </div>
          <button type="submit" class="btn btn-primary mt-2"><%= $tButtonFormSubmit %></button>
        </form>
      </div>
      <div class="card-body">
        <b># cat /etc/TZ</b>
        <pre><% cat /etc/TZ %></pre>
        <b># echo $TZ</b>
        <pre><% echo $TZ %></pre>
        <b># date</b>
        <pre><% date %></pre>
        <% check_env_tz %>
      </div>
    </div>
  </div>
  <div class="col">
    <div class="card mb-3">
      <h5 class="card-header"><%= $tHeaderNtpServers %></h5>
      <div class="card-body">
        <form action="/cgi-bin/network-ntp-update.cgi" method="post">
          <%
            for i in 0 1 2 3; do
              x=$(expr $i + 1)
              ip=$(sed -n ${x}p /etc/ntp.conf | cut -d " " -f 2)
              echo "<div class=\"row mb-1\">"
              echo "<label class=\"col-md-5 form-label\" for=\"ntp_server_${i}\">$tLabelNtpServer ${x}</label>"
              echo "<div class=\"col-md-7\">"
              echo "<input class=\"form-control pat-host-ip\" type=\"text\" name=\"ntp_server[${i}]\" id=\"ntp_server_${i}\" value=\"${ip}\" placeholder=\"${i}.pool.ntp.org\">"
              echo "</div>"
              echo "</div>"
            done
          %>
          <button type="submit" class="btn btn-primary mt-2"><%= $tButtonFormSubmit %></button>
          <a class="btn btn-danger mt-2" href="/cgi-bin/network-ntp-reset.cgi"><%= $tButtonResetToDefaults %></a>
        </form>
      </div>
      <div class="card-body">
        <b># cat /etc/ntp.conf</b>
        <pre><% cat /etc/ntp.conf %></pre>
      </div>
    </div>
  </div>
</div>
<script src="/js/tz.js" async></script>
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
  if (navigator.userAgent.includes('Android') && navigator.userAgent.includes('Firefox')) {
    const inp = $('#tz_name');
    const sel = document.createElement('select');
    sel.classList.add('form-select');
    sel.name = 'tz_name';
    sel.id = 'tz_name';
    sel.options.add(new Option());
    let opt;
    TZ.forEach(function(tz) {
      opt = new Option(tz.name);
      opt.selected = (tz.name == inp.value);
      sel.options.add(opt);
    });
    inp.replaceWith(sel);
  } else {
    const el = $('#tz_list');
    el.innerHTML='';
    TZ.forEach(function(tz) {
      const o = document.createElement('option');
      o.value = tz.name;
      el.appendChild(o);
    });
  }
  $('#tz_name').addEventListener('focus', ev => ev.target.select());
  $('#tz_name').addEventListener('selectionchange', updateTimezone);
  $('#tz_name').addEventListener('change', updateTimezone);
  updateTimezone();
});
</script>
<%in _footer.cgi %>
