#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="Network Administration"
hostname=$(hostname -s)
ipaddr=$(yaml-cli -g .network.lan.ipaddr)
ipaddr_eth0=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}')
macaddr=$(ifconfig -a | grep HWaddr | sed s/.*HWaddr// | uniq)
netmask=$(yaml-cli -g .network.lan.netmask)
netmask_eth0=$(ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}')
password=$(awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf)
vpn1=$(yaml-cli -g .openvpn.vpn1.remote)
timezone=$(cat /etc/TZ)
%>
<%in _header.cgi %>
<h2><%= $page_title %></h2>
<% flash_read %>
<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Settings</div>
      <div class="card-body">
        <form action="/cgi-bin/network-update.cgi" method="post">
          <input type="hidden" name="action" value="update">
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="hostname">Device Name</label>
            <div class="col-md-7 mb-1">
              <input class="form-control pat-host" type="text" name="hostname" id="hostname" value="<%= $hostname %>" placeholder="device-name">
            </div>
            <i class="hint">Make hostname unique using MAC address information (<%= $macaddr %>).</i>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="ipaddr">IP Address</label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="ipaddr" id="ipaddr" value="<%= $ipaddr %>" data-real="<%= $ipaddr_eth0 %>" placeholder="192.168.10.10">
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="netmask">IP Netmask</label>
            <div class="col-md-7">
              <input type="text" class="form-control" name="netmask" id="netmask" value="<%= $netmask %>" data-real="<%= $netmask_eth0 %>" placeholder="255.255.255.0">
            </div>
          </div>
          <div class="row mb-1">
            <label class="col-md-5 form-label" for="remote">VTUNd Server</label>
            <div class="col-md-7">
              <div class="input-group">
                <input type="text" class="form-control" name="remote" id="remote" value="<%= $vpn1 %>" placeholder="vtun.net">
                <div class="input-group-text">
                  <input class="form-check-input mt-0 me-2" type="checkbox" name="remote" value="__delete">
                  <img src="/img/trash.svg" alt="Delete">
                </div>
              </div>
            </div>
          </div>
          <button type="submit" class="btn btn-primary">Save Settings</button>
        </form>
      </div>
      <div class="card-footer bg-black text-white">Sorry, some things aren't working yet.</div>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header">Network Address</div>
      <div class="card-body">
        <b># ip address</b>
        <pre><% ip address | sed "s/</\&lt;/g" | sed "s/>/\&gt;/g" %></pre>
      </div>
    </div>
  </div>

  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header">Network Routing</div>
      <div class="card-body">
        <b># ip route list</b>
        <pre><% ip route list %></pre>
      </div>
    </div>
  </div>

  <div class="col-12 mb-3">
    <div class="card h-100">
      <div class="card-header">Network Status</div>
      <div class="card-body">
        <b># netstat -tulpan</b>
        <pre><% netstat -tulpan %></pre>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">DNS Resolver</div>
      <div class="card-body">
        <b># cat /etc/resolv.conf</b>
        <pre><% cat /etc/resolv.conf 2>&1 %></pre>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">NTP Configuration</div>
      <div class="card-body">
        <b># cat /etc/ntp.conf</b>
        <pre><% cat /etc/ntp.conf 2>&1 %></pre>
      </div>
    </div>
  </div>
</div>

<%in _footer.cgi %>
