#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_system_info

page_title="$tPageTitleNetworkAdministration"

ipaddr_mj=$(yaml-cli -g .network.lan.ipaddr)
netmask_mj=$(yaml-cli -g .network.lan.netmask)
vpn1_mj=$(yaml-cli -g .openvpn.vpn1.remote)

ipaddr_eth0=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}')
netmask_eth0=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}')
password=$(awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf)
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
            <label class="col-md-5 form-label" for="hostname"><%= $tLabelDeviceName %></label>
            <div class="col-md-7 mb-1">
              <input class="form-control pat-host" type="text" name="hostname" id="hostname" value="<%= $hostname %>" placeholder="device-name">
            </div>
            <i class="hint"><%= $tHintMakeHostnameUnique %> (<%= $macaddr %>).</i>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="ipaddr"><%= $tLabelIpAddress %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="ipaddr" id="ipaddr" value="<%= $ipaddr_mj %>" data-real="<%= $ipaddr_eth0 %>" placeholder="192.168.10.10">
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="netmask"><%= $tLabelIpNetmask %></label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="netmask" id="netmask" value="<%= $netmask_mj %>" data-real="<%= $netmask_eth0 %>" placeholder="255.255.255.0">
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="remote"><%= $tLabelVtundServer %></label>
            <div class="col-md-7">
              <div class="input-group">
                <input type="text" class="form-control" name="remote" id="remote" value="<%= $vpn1_mj %>" placeholder="vtun.net">
                <div class="input-group-text">
                  <input class="form-check-input mt-0 me-2" type="checkbox" name="remote" value="__delete">
                  <img src="/img/trash.svg" alt="Delete">
                </div>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
        </form>
      </div>
      <div class="card-footer bg-black text-white"><%= $tMsgUnderConstruction %></div>
    </div>
  </div>
</div>
<div class="row">
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
<%in _footer.cgi %>
