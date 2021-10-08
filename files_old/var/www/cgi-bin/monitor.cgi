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
      <img src="https://openipc.org/images/logo_openipc.png" width="256">
      <p><b>Device Info</b></p>
      <pre><? echo "openipc-$(ipctool --chip_id)-$(ipctool --sensor_id | awk -F '_' '{print $1}')" ?></pre>
      <p><b>Uptime Device</b></p>
      <pre><? uptime ?></pre>
      <p><b>Routing Table</b></p>
      <table>
        <tr><td><pre><? route -n ?></pre></td></tr>
      </table>
      <p><b>Network Status</b></p>
      <table>
        <tr><td><pre><? ifconfig eth0 ?></pre></td></tr>
        <tr><td><pre><? ifconfig tunell ?></pre></td></tr>
        <tr><td><pre><? ifconfig usb0 ?></pre></td></tr>
        <tr><td><pre><? ifconfig wg0 ?></pre></td></tr>
        <tr><td><pre><? ifconfig wlan0 ?></pre></td></tr>
      </table>
      <p><b>Ping Quality</b></p>
      <table>
        <tr>
          <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
            <td>
              <input type=hidden name="action" value="ping">
              <input type="text" required name="sense" pattern="^[a-zA-Z0-9-_.]+$" value="77.88.8.8" placeholder="host or ip" size="25">
            </td>
            <td>
              <input type="radio" required checked="checked" name="iface" value="auto"> auto <br>
              <input type="radio" name="iface" value="eth0"> eth0 <br>
              <input type="radio" name="iface" value="wlan0"> wlan0 <br>
            </td>
            <td>
              <input type="submit" value="Run">
            </td>
          </form>
        </tr>
      </table>
      <p><b>Trace Route</b></p>
      <table>
        <tr>
          <form action="/cgi-bin/update.cgi" method="POST" enctype="multipart/form-data">
            <td>
              <input type=hidden name="action" value="trace">
              <input type="text" required name="sense" pattern="^[a-zA-Z0-9-_.]+$" value="77.88.8.8" placeholder="host or ip" size="25">
            </td>
            <td>
              <input type="radio" required checked="checked" name="iface" value="auto"> auto <br>
              <input type="radio" name="iface" value="eth0"> eth0 <br>
              <input type="radio" name="iface" value="wlan0"> wlan0 <br>
            </td>
            <td>
              <input type="submit" value="Run">
            </td>
          </form>
        </tr>
      </table>
      <br><br><br>
      <form action="/cgi-bin/index.cgi" method="POST" enctype="multipart/form-data">
        <input type="submit" value="Global Settings">
      </form>
    </div>
  </body>
</html>
