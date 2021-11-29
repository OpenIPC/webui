#!/usr/bin/haserl
content-type: text/html

<%
norm_name() {
  echo -n $(echo $1 | sed 's/\./_/g')
}

get_value() {
  echo -n $(yaml-cli -g ".$1")
}

to_top() {
  echo -n "<p class=\"small\"><a href=\"#top\">Go to top</a></p>"
}

checkbox() {
  echo -n "<input type=\"checkbox\" name=\"$(norm_name $1)\" value=\"true\""
  [ $(get_value $1) = "true" ] && echo -n " checked"
  echo -n ">"
}

number_field() {
  echo -n "<input type=\"number\" name=\"$(norm_name $1)\" value=\"$(get_value $1)\" $2 $3>"
}

text_field() {
  echo -n "<input type=\"text\" name=\"$(norm_name $1)\" value=\"$(get_value $1)\" $2 $3>"
}

range_field() {
  name = $(norm_name $1)
  value = $(get_value $1)
  echo -n "<input type=\"range\" name=\"$name\" value=\"$value\" $2 $3>"
  echo -n "(<span id=\"v-$name\" class=\"rval\">$value</span>)"
}

select_field() {
  echo -n "<select name=\"$(norm_name $1)\">"
  echo -n "<option value=\"\">-- options --</option>"
  for x in $(echo $2 | tr "|" " "); do
    echo -n "<option"
    [ $(get_value $1) = "$x" ] && echo -n " selected"
    echo -n ">$x</option>"
  done
  echo -n "</select>"
}
%>
<%in _header.cgi %>
<ol><% for i in System ISP Image OSD Nightmode Records Video0 Video1 JPEG MJPEG Audio RTSP HSL Youtube motionDetect IPEYE NETIP ONVIF RAW Watchdog; do
  echo "<li><a href=\"#$(echo "$i" | tr '[:upper:]' '[:lower:]')\">$i</a></li>"; done %></ol>

<form action="/cgi-bin/majestic-settings.cgi" method="post">

<div>
<h3 id="system">System</h3>
<label><b>logLevel</b> <% select_field "system.logLevel" "ERROR|WARN|INFO|DEBUG|TRACE" %></label>
<label><b>sensorConfig</b> <% text_field "system.sensorConfig" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/sensors/imx222_1080p_line.ini\" %> <i>If not set, uses SENSOR environment variable.</i></label>
<label><b>sensorConfigDir</b> <% text_field "system.sensorConfigDir" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/sensors\" %> <i>Path to sensor configs.</i></label>
<label><b>webPort</b> <% number_field "system.webPort" placeholder=\"80\" min=\"1\" max=\"65535\" %></label>
<label><b>staticDir</b> <% text_field "system.staticDir" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/var/www/html\" %></label>
<label><b>httpsPort</b> <% number_field "system.httpsPort" placeholder=\"443\" min=\"1\" max=\"65535\" %></label>
<label><b>httpsCertificate</b> <% text_field "system.httpsCertificate" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/ssl/certs/www.example.com.crt\" %></label>
<label><b>httpsCertificateKey</b> <% text_field "system.httpsCertificateKey" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/ssl/certs/www.example.com.key\" %></label>
<label><b>updateChannel</b> <% select_field "system.updateChannel" "testing|beta|stable|none" %></label>
<label><b>buffer</b> <% number_field "system.buffer" placeholder=\"1024\" min=\"0\" %> <i>KB. Maximum buffer size for each client.</i></label>
<% to_top %>
</div>

<div>
<h3 id="isp">ISP</h3>
<label><b>memMode</b> <% select_field "isp.memMode" "normal|reduction" %></label>
<label><b>slowShutter</b> <% select_field "isp.slowShutter" "disabled|low|medium|high" %> <i>Automatic frame rate reduction mode.</i></label>
<label><b>antiFlicker</b> <% select_field "isp.antiFlicker" "disabled|50|60" %> <i>Hz. For indoor camera, depends on power grid standard.</i></label>
<label><b>alignWidth</b> <% number_field "isp.alignWidth" placeholder=\"8\" min=\"0\" %></label>
<label><b>blkCnt</b> <% number_field "isp.blkCnt" placeholder=\"4\" min=\"0\" %> <i>4 for small memory systems, 10 and more for performant SoCs</i></label>
<label><b>threadStackSize</b> <% number_field "isp.threadStackSize" placeholder=\"16\" min=\"0\" %> <i>KB</i></label>
<label title="Set exposition in ms, from 1 to 500000 or auto"><b>exposure</b> <% number_field "isp.exposure" placeholder=\"auto\" min=\"0\" max=\"500000\" %><i>set 0 for auto</i></label>
<label><b>aGain</b> <% range_field "isp.aGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>dGain</b> <% range_field "isp.dGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>ispGain</b> <% range_field "isp.ispGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>drc</b> <% number_field "isp.drc" placeholder=\"300\" min=\"0\" %> <i>:1</i></label>
<% to_top %>
</div>

<div>
<h3 id="image">Image</h3>
<label><b>mirror</b> <% checkbox "image.mirror" %></label>
<label title="turn image upside down"><b>flip</b> <% checkbox "image.flip" %></label>
<label title="rotate image by none, 90 or 270 degrees"><b>rotate</b> <% select_field "image.rotate" "none|90|270" %></label>
<label><b>contrast</b> <% range_field "image.contrast" placeholder=\"auto\" min=\"0\" max=\"99\" %> <i>set 0 for auto</i></label>
<label><b>hue</b> <% range_field "image.hue" placeholder=\"50\" min=\"1\" max=\"99\" %></label>
<label><b>saturation</b> <% range_field "image.saturation" placeholder=\"50\" min=\"1\" max=\"99\" %></label>
<label><b>luminance</b> <% range_field "image.luminance" placeholder=\"auto\" min=\"0\" max=\"99\" %> <i>set 0 for auto</i></label>
<% to_top %>
</div>

<div>
<h3 id="osd">OSD</h3>
<label><b>enabled</b> <% checkbox "osd.enabled" %></label>
<label><b>font</b> <% text_field "osd.font" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/usr/lib/fonts/fonts.bin\" %></label>
<label><b>template</b> <% text_field "osd.template" pattern=\"^[a-zA-Z0-9%: ]+$\" placeholder=\"%a %e %B %Y %H:%M:%S %Z\" %> <i>use %f for milliseconds (consumes more resources)</i></label>
<label><b>posX</b> <% number_field "osd.posX" placeholder=\"-100\" min=\"-5000\" max=\"5000\" %> <i>+ from top/left, - from bottom/right</i></label>
<label><b>posY</b> <% number_field "osd.posY" placeholder=\"-100\" min=\"-5000\" max=\"5000\" %> <i>+ from top/left, - from bottom/right</i></label>
<% to_top %>
</div>

<div>
<h3 id="nightmode">Nightmode</h3>
<label><b>enabled</b> <% checkbox "nightMode.enabled" %></label>
<label><b>irSensorPin</b> <% number_field "nightMode.irSensorPin" placeholder=\"62\" min=\"1\" %></label>
<label><b>irSensorPinInvert</b> <% checkbox "nightMode.irSensorPinInvert" %></label>
<label><b>irCutPin1</b> <% number_field "nightMode.irCutPin1" placeholder=\"1\" min=\"1\" %></label>
<label><b>irCutPin2</b> <% number_field "nightMode.irCutPin2" placeholder=\"2\" min=\"1\" %></label>
<label><b>pinSwitchDelayUs</b> <% number_field "nightMode.pinSwitchDelayUs" placeholder=\"150\" min=\"0\" max=\"1000\" %> <i>IRcut filter pin switch delay in μs </i></label>
<h5 class="red">WARNING! Very long delay can damage IRcut filter!</h5>
<label title="turn on backlight illumination when night mode is on"><b>backlightPin</b> <% number_field "nightMode.backlightPin" placeholder=\"65\" min=\"1\" max=\"100\" %></label>
<label title="use /night/{invert,on,off} endpoints to change mode by API for remote callers"><b>nightAPI</b> <% checkbox "nightMode.nightAPI" %></label>
<label title="use special value for drc parameter in night mode"><b>drcOverride</b> <% number_field "nightMode.drcOverride" placeholder=\"300\" min=\"1\" %></label>
<% to_top %>
</div>

<div>
<h3 id="records">Records</h3>
<label><b>enabled</b> <% checkbox "records.enabled" %></label>
<label><b>path</b> <% text_field "records.path" pattern=\"^[a-zA-Z0-9-_./%]+$\" placeholder=\"/mnt/mmc/%Y/%m/%d/%H.mp4\" %></label>
<label><b>maxUsage</b> <% number_field "records.maxUsage" placeholder=\"95\" min=\"1\" max=\"100\" %></label>
<% to_top %>
</div>

<div>
<h3 id="video0">Video0</h3>
<label><b>enabled</b> <% checkbox "video0.enabled" %></label>
<label><b>codec</b> <% select_field "video0.codec" "h265|h264" %></label>
<label><b>size</b> <% text_field "video0.size" pattern=\"^[xX0-9]+$\" placeholder=\"1920x1080\" %></label>
<label><b>fps</b> <% number_field "video0.fps" placeholder=\"25\" min=\"1\" max=\"60\" %></label>
<label><b>bitrate</b> <% number_field "video0.bitrate" placeholder=\"4096\" min=\"1\" max=\"115200\" %> <i>kbps</i></label>
<label><b>gopSize</b> <% number_field "video0.gopSize" placeholder=\"1\" min=\"1\" max=\"180\" %> <i>send I-frame every second</i></label>
<label><b>gopMode</b> <% select_field "video0.gopMode" "normal|dual|smart" %></label>
<label><b>rcMode</b> <% select_field "video0.rcMode" "avbr" %></label>
<label><b>crop</b> <% text_field "video0.crop" pattern=\"^[xX0-9]+$\" placeholder=\"0x0x960x540\" %></label>
<% to_top %>
</div>

<div>
<h3 id="video1">Video1</h3>
<label><b>enabled</b> <% checkbox "video1.enabled" %></label>
<label><b>codec</b> <% select_field "video1.codec" "h265|h264" %></label>
<label><b>size</b> <% text_field "video1.size" pattern=\"^[xX0-9]+$\" placeholder=\"704x576\" %></label>
<label><b>fps</b> <% number_field "video1.fps" placeholder=\"15\" min=\"1\" max=\"60\" %></label>
<% to_top %>
</div>

<div>
<h3 id="jpeg">JPEG</h3>
<label><b>enabled</b> <% checkbox "jpeg.enabled" %></label>
<label><b>size</b> <% text_field "jpeg.size" pattern=\"^[xX0-9]+$\" placeholder=\"1920x1080\" %></label>
<label><b>qfactor</b> <% number_field "jpeg.qfactor" placeholder=\"50\" min=\"1\" max=\"99\" %> <i>JPEG quality</i></label>
<label><b>toProgressive</b> <% checkbox "jpeg.toProgressive" %> <i>transform snapshot to Progressive JPEG</i></label>
<% to_top %>
</div>

<div>
<h3 id="mjpeg">MJPEG</h3>
<label><b>size</b> <% text_field "mjpeg.size" pattern=\"^[xX0-9]+$\" placeholder=\"640x360\" %></label>
<label><b>fps</b> <% number_field "mjpeg.fps" placeholder=\"5\" min=\"1\" max=\"60\" %></label>
<label><b>bitrate</b> <% number_field "mjpeg.bitrate" placeholder=\"1024\" min=\"1\" max=\"2048\" %></label>
<% to_top %>
</div>

<div>
<h3 id="audio">Audio</h3>
<label><b>enabled</b> <% checkbox "audio.enabled" %></label>
<label><b>volume</b> <% number_field "audio.volume" placeholder=\"auto\" min=\"0\" max=\"100\" %><i>set 0 for auto</i></label>
<label><b>srate</b> <% number_field "audio.srate" placeholder=\"8000\" min=\"1\" max=\"44100\" %></label>
<label><b>codec</b> <% select_field "audio.codec" "aac|mp3|opus|pcm" %> <i>default codec for RTSP and MP4 encoding</i></label>
<label><b>outputEnabled</b> <% checkbox "audio.outputEnabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="rtsp">RTSP</h3>
<label><b>enabled</b> <% checkbox "rtsp.enabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="hsl">HLS</h3>
<label><b>enabled</b> <% checkbox "hls.enabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="youtube">Youtube</h3>
<label><b>enabled</b> <% checkbox "youtube.enabled" %></label>
<label><b>key</b> <% text_field "youtube.key" pattern=\"^[a-zA-Z0-9-]+$\" placeholder=\"xxxx-xxxx-xxxx-xxxx-xxxx\" %></label>
<% to_top %>
</div>

<div>
<h3 id="motiondetect">motionDetect</h3>
<label><b>enabled</b> <% checkbox "motionDetect.enabled" %></label>
<label><b>profile</b> <% select_field "motionDetect.profile" "outdoor|indoor" %></label>
<label><b>visualize</b> <% checkbox "motionDetect.visualize" %></label>
<label><b>debug</b> <% checkbox "motionDetect.debug" %></label>
<label title="ROI for motion detection algorithm e.g. top upper quadrant"><b>constraints</b> <% text_field "motionDetect.constraints" pattern=\"^[xX0-9]+$\" placeholder=\"0x0x1296x760\" %></label>
<% to_top %>
</div>

<div>
<h3 id="ipeye">IPEYE</h3>
<label><b>enabled</b> <% checkbox "ipeye.enabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="netip">NETIP</h3>
<label><b>enabled</b> <% checkbox "netip.enabled" %></label>
<label><b>user</b> <% text_field "netip.user" placeholder=\"admin\" %></label>
<label><b>password</b> <% text_field "netip.password" placeholder=\"6V0Y4HLF\" %></label>
<label><b>port</b> <% number_field "netip.port" placeholder=\"34567\" min=\"1\" max=\"65535\" %></label>
<label><b>snapshots</b> <% checkbox "netip.snapshots" %></label>
<label><b>ignore_set_time</b> <% checkbox "netip.ignore_set_time" %></label>
<% to_top %>
</div>

<div>
<h3 id="onvif">ONVIF</h3>
<label><b>enabled</b> <% checkbox "onvif.enabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="raw">RAW</h3>
<label><b>enabled</b> <% checkbox "raw.enabled" %></label>
<% to_top %>
</div>

<div>
<h3 id="watchdog">Watchdog</h3>
<label><b>enabled</b> <% checkbox "watchdog.enabled" %></label>
<label><b>timeout</b> <% number_field "watchdog.timeout" placeholder=\"10\" min=\"1\" max=\"100\" %> <i>sec</i></label>
<% to_top %>
</div>

<input type="submit" value="Save">
<input type="submit" value="Debug" onclick="javascript:document.querySelector('form').action='http://phphome.lan/info.php';">
</form>

<%in _footer.cgi %>
