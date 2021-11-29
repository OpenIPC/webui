#!/usr/bin/haserl
content-type: text/html

<%
f() { echo "<form action=\"/cgi-bin/$1.cgi\" method=\"post\">"; }
fmp() { echo "<form action=\"/cgi-bin/$1.cgi\" method=\"post\" enctype=\"multipart/form-data\">"; }
fif() { echo "<label><b>$1</b> <input type=\"file\" name=\"$2\"></label>"; }
fih() { echo "<input type=\"hidden\" name=\"action\" value=\"$1\">"; }
fis() { echo "<p><input type=\"submit\" value=\"$1\"></p>"; }
%>
<%in _header.cgi %>

<h4>All changes will be applied on reboot!</h4>

<h3>Camera Settings</h3>
<% f "update" %>
<% fih "update" %>
<label><b>Device Name</b>
 <input class="t h" name="hostname" placeholder="DeviceName" value="<% cat /etc/hostname %>"></label>
<label><b>Interface Password</b>
 <input class="p" name="password" placeholder="You3Pass5Word" value="<% awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf || echo "" %>"></label>
<label><b>IP Address</b>
  <input class="t a" name="ipaddr" placeholder="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}' || echo "192.168.10.10" %>" value=""></label>
<label><b>IP Netmask</b>
  <input class="t a" name="netmask" placeholder="<% ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}' || echo "255.255.255.0" %>" value=""></label>
<label><b>VTUNd Server</b>
  <input class="t h" name="remote" placeholder="<% uci get openvpn.vpn1.remote || echo "vtun.net" %>" value=""></label>
<% fis "Save Settings" %>
</form>

<h3>Update kernel</h3>
<% fmp "upload" %>
<% fih "kernel" %>
<% fif "kernel file" "upfile" %>
<% fis "Upload File" %>
</form>

<h3>Update rootfs</h3>
<% fmp "upload" %>
<% fih "rootfs" %>
<% fif "rootfs file" "upfile" %>
<% fis "Upload File" %>
</form>

<%in _footer.cgi %>
