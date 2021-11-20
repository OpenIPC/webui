#!/usr/bin/haserl
<?
  export PATH=/bin:/sbin:/usr/bin:/usr/sbin
  echo -e "Content-type: text/html\r\n\r\n"
?>

<html>
  <head>
    <link rel="shortcut icon" href="/assets/img/favicon.png">
  </head>
  <body>
    <div align=center>
      <p><b>Device Name</b></p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="hostname">
        <input type="text" required name="sense" pattern="^[a-zA-Z0-9-_.]+$" value="<? cat /etc/hostname ?>" placeholder="DeviceName" size="25">
        <input type="submit" value="Save">
      </form>
      <p><b>Interface Password</b></p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="password">
        <input type="password" required name="sense" pattern="^[a-zA-Z0-9!@#\$%\^\&*_=+-]+$" value="<? awk -F ':' '/cgi-bin/ {print $3}' /etc/httpd.conf ?>" placeholder="You3Pass5Word" size="25">
        <input type="submit" value="Save">
      </form>
      <p><b>IP Address</b></p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="ipaddr">
        <input type="text" required name="sense" pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" value="<? ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $3}' ?>" placeholder="192.168.1.10" size="25">
        <input type="submit" value="Save">
      </form>
      <p><b>IP Netmask</b></p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="netmask">
        <input type="text" required name="sense" pattern="\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" value="<? ifconfig eth0 | grep "inet " | tr ':' ' ' | awk '{print $7}' ?>" placeholder="255.255.255.0" size="25">
        <input type="submit" value="Save">
      </form>
      <p><b>VTUNd Server</b></p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="remote">
        <input type="text" required name="sense" pattern="^[a-zA-Z0-9-.]+$" value="<? uci get openvpn.vpn1.remote ?>" placeholder="vtun.net" size="25">
        <input type="submit" value="Save">
      </form>
      <p><b>Update kernel</b></p>
      <form action="/cgi-bin/upload.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="kernel">
        <input type="file" required name="upfile">
        <input type="submit" value="Upload">
      </form>
      <p><b>Update rootfs</b></p>
      <form action="/cgi-bin/upload.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="rootfs">
        <input type="file" required name="upfile">
        <input type="submit" value="Upload">
      </form>
      <br>
      <p><font color="blue">All settings will be applied after rebooting the device !</p>
      <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
        <input type=hidden name="action" value="reboot">
        <input type="submit" value="Reboot Device" onclick="return confirm('Do you want to reboot the device ?')">
      </form>
    </div>
  </body>
</html>
