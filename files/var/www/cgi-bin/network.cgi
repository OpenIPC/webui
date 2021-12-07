#!/usr/bin/haserl
<%
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
<h2>Network Administration</h2>

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Settings</div>
      <div class="card-body">
        <form action="/cgi-bin/network-update.cgi" method="post">
          <input type="hidden" name="action" value="update">

          <div class="row">
            <div class="col-12 col-md-5">
              <label for="hostname" class="form-label">Device Name</label>
            </div>
            <div class="col-md-7 mb-3">
              <input type="text" class="form-control" name="hostname" id="hostname" value="<%= $hostname %>" placeholder="device-name">
              <i class="hint">Make hostname unique using MAC address information (<%= $macaddr %>).</i>
            </div>
          </div>

          <div class="row">
            <div class="col-md-5">
              <label for="password" class="form-label">Interface Password</label>
            </div>
            <div class="col-md-7 mb-3">
              <input type="password" class="form-control" name="password" id="password" value="<%= $password %>" placeholder="K3wLHaZk3R!">
            </div>
          </div>

          <div class="row">
            <div class="col-md-5">
              <label for="timezone" class="form-label">Timezone</label>
            </div>
            <div class="col-md-7 mb-3">
              <input type="text" class="form-control" name="timezone" id="timezone" value="<%= $timezone %>" placeholder="GMT+2">
            </div>
          </div>

          <div class="row">
            <div class="col mb-0">
              <input type="submit" class="btn btn-primary" value="Save Settings">
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div class="col mb-3">
    <div class="card h-100">
      <div class="card-header">Settings</div>
      <div class="card-body">
        <form action="/cgi-bin/network-update.cgi" method="post">
          <input type="hidden" name="action" value="update">
          <div class="row">
            <div class="col-md-5">
              <label for="ipaddr" class="form-label">IP Address</label>
            </div>
            <div class="col-md-7  mb-3">
              <input type="text" class="form-control" name="ipaddr" id="ipaddr" value="<%= $ipaddr %>" data-real="<%= $ipaddr_eth0 %>" placeholder="192.168.10.10">
            </div>
          </div>
          <div class="row">
            <div class="col-md-5">
              <label for="netmask" class="form-label">IP Netmask</label>
            </div>
            <div class="col-md-7 mb-3">
              <input type="text" class="form-control" name="netmask" id="netmask" value="<%= $netmask %>" data-real="<%= $netmask_eth0 %>" placeholder="255.255.255.0">
            </div>
          </div>
          <div class="row">
            <div class="col-md-5">
              <label for="remote" class="form-label">VTUNd Server</label>
            </div>
            <div class="col-md-7 mb-3">
              <input type="text" class="form-control" name="remote" id="remote" value="<%= $vpn1 %>" placeholder="vtun.net">
            </div>
          </div>
          <div class="row">
            <div class="col mt-3 mb-0">
              <input type="submit" class="btn btn-primary" value="Save Settings">
            </div>
          </div>
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
