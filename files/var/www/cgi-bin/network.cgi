#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info
page_title="$tPageTitleNetworkAdministration"
dhcp=$(cat /etc/network/interfaces | grep "eth0 inet" | grep dhcp)
ipaddr=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}')
netmask=$(ifconfig eth0 | grep "inet " | cut -d: -f4)
gateway=$(ip r | grep default | cut -d' ' -f3)
dns1=$(cat /etc/resolv.conf | grep nameserver | sed -n 1p | cut -d' ' -f2)
dns2=$(cat /etc/resolv.conf | grep nameserver | sed -n 2p | cut -d' ' -f2)

checked() {
  [ -n "$dhcp" ] && echo -n " checked"
}
disabled() {
  [ -n "$dhcp" ] && echo -n " disabled"
}
%>
<%in _header.cgi %>
<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderSettings %></div>
      <div class="card-body">
        <form action="/cgi-bin/network-update.cgi" method="post">
          <input type="hidden" name="action" value="update">
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="hostname"><%= $tLabelHostname %></label>
            <div class="col-md-7 mb-1">
              <input class="form-control pat-host" type="text" name="hostname" id="hostname" value="<%= $hostname %>">
            </div>
            <i class="hint"><%= $tHintMakeHostnameUnique %> (<%= $macaddr %>).</i>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="ipaddr"><%= $tLabelIpAddress %></label>
            <div class="col-md-7">
              <div class="input-group">
                <input type="text" class="form-control" name="ipaddr" id="ipaddr" value="<%= $ipaddr %>"<% disabled %>>
                <div class="input-group-text">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" name="dhcp" id="dhcp" value="true"<% checked %>>
                    <label class="form-check-label" for="dhcp"><%= $tLabelIpDhcp %></label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="netmask"><%= $tLabelIpNetmask %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="netmask" id="netmask" value="<%= $netmask %>"<% disabled %>>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="gateway"><%= $tLabelIpGateway %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="gateway" id="gateway" value="<%= $gateway %>"<% disabled %>>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="gateway"><%= $tLabelDns1 %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="dns1" id="dns1" value="<%= $dns1 %>"<% disabled %>>
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="gateway"><%= $tLabelDns2 %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="dns2" id="dns2" value="<%= $dns2 %>"<% disabled %>>
            </div>
          </div>
          <button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
        </form>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-body">
        <b># cat /etc/network/interfaces</b>
	<pre><% cat /etc/network/interfaces %></pre>
      </div>
    </div>
  </div>

  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderNetworkAddress %></div>
      <div class="card-body">
        <b># ip address</b>
        <pre><% ip address | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g" %></pre>
      </div>
    </div>
  </div>
  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderNetworkRouting %></div>
      <div class="card-body">
        <b># ip route list</b>
        <pre><% ip route list %></pre>
      </div>
    </div>
  </div>
  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderNetworkStatus %></div>
      <div class="card-body">
        <b># netstat -tulpan</b>
        <pre><% netstat -tulpan %></pre>
      </div>
    </div>
  </div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderDnsResolver %></div>
      <div class="card-body">
        <b># cat /etc/resolv.conf</b>
        <pre><% cat /etc/resolv.conf 2>&1 %></pre>
      </div>
    </div>
  </div>
  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header"><%= $tHeaderNtpConfig %></div>
      <div class="card-body">
        <b># cat /etc/ntp.conf</b>
        <pre><% cat /etc/ntp.conf 2>&1 %></pre>
      </div>
    </div>
  </div>
</div>
<script>
$('#dhcp').addEventListener('change', (ev) => {
  $('#ipaddr').disabled = ev.target.checked
  $('#netmask').disabled = ev.target.checked
  $('#gateway').disabled = ev.target.checked
  $('#dns1').disabled = ev.target.checked
  $('#dns2').disabled = ev.target.checked
});
</script>
<%in _footer.cgi %>
