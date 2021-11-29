#!/usr/bin/haserl
content-type: text/html

<%
checkbox() {
  echo -n "<input type=\"checkbox\" name=\"$1\""
  [ "$(yaml-cli -g $1)" == "true"  ] && echo -n " checked"
  echo -n ">\n"
}

text_field() {
  echo -n "<input type=\"text\" name=\"$1\" value=\"$(yaml-cli -g $1)\" $2 $3>"
}

number_field() {
  echo -n "<input type=\"number\" name=\"$1\" value=\"$(yaml-cli -g $1)\" $2 $3>"
}

select() {
  echo "<select name=\"$1\">"
  for n in $(echo $2 | tr "|" " "); do
    echo -n "<option></option>"
    echo -n "<option"
    [ "$(yaml-cli -g $1)" == "$n" ] && echo -n " selected"
    echo -n ">$n</option>\n"
  done
  echo -n "</select>"
}
%>
<%in _header.cgi %>

<ol>
<li><a href="#system">System</a></li>
<li><a href="#isp">ISP</a></li>
<li><a href="#image">Image</a></li>
<li><a href="#osd">OSD</a></li>
<li><a href="#nightmode">Nightmode</a></li>
<li><a href="#records">Records</a></li>
<li><a href="#video0">Video0</a></li>
<li><a href="#video1">Video1</a></li>
<li><a href="#jpeg">JPEG</a></li>
<li><a href="#mjpeg">MJPEG</a></li>
<li><a href="#audio">Audio</a></li>
<li><a href="#rtsp">RTSP</a></li>
<li><a href="#hsl">HSL</a></li>
<li><a href="#youtube">Youtube</a></li>
<li><a href="#motiondetect">motionDetect</a></li>
<li><a href="#ipeye">IPEYE</a></li>
<li><a href="#netip">NETIP</a></li>
<li><a href="#onvif">ONVIF</a></li>
<li><a href="#raw">RAW</a></li>
<li><a href="#watchdog">Watchdog</a></li>
</ol>

<form action="/cgi-bin/majestic-settings.cgi" method="post">

<div>
<h3 id="system">System</h3>
<label><b>logLevel</b> <% select ".system.logLevel" "ERROR|WARN|INFO|DEBUG|TRACE" %></label>
<label><b>sensorConfig</b> <% text_field ".system.sensorConfig" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/sensors/imx222_1080p_line.ini\" %> <i>If not set, uses SENSOR environment variable.</i></label>
<label><b>sensorConfigDir</b> <% text_field ".system.sensorConfigDir" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/sensors\" %> <i>Path to sensor configs.</i></label>
<label><b>webPort</b> <% number_field ".system.webPort" placeholder=\"80\" min=\"1\" max=\"65535\" %></label>
<label><b>staticDir</b> <% text_field ".system.staticDir" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/var/www/html\" %></label>
<label><b>httpsPort</b> <% number_field ".system.httpsPort" placeholder=\"443\" min=\"1\" max=\"65535\" %></label>
<label><b>httpsCertificate</b> <% text_field ".system.httpsCertificate" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/ssl/certs/www.example.com.crt\" %></label>
<label><b>httpsCertificateKey</b> <% text_field ".system.httpsCertificateKey" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/etc/ssl/certs/www.example.com.key\" %></label>
<label><b>updateChannel</b> <% select ".system.updateChannel" "testing|beta|stable|none" %></label>
<label><b>buffer</b> <% number_field ".system.buffer" placeholder=\"1024\" min=\"0\" %> <i>KB. Maximum buffer size for each client.</i></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="isp">ISP</h3>
<label><b>memMode</b> <% select ".isp.memMode" "normal|reduction" %></label>
<label><b>slowShutter</b> <% select ".isp.slowShutter" "disabled|low|medium|high" %> <i>Automatic frame rate reduction mode.</i></label>
<label><b>antiFlicker</b> <% select ".isp.antiFlicker" "disabled|50|60" %> <i>Hz. For indoor camera, depends on power grid standard.</i></label>
<label><b>alignWidth</b> <% number_field ".isp.alignWidth" placeholder=\"8\" min=\"0\" %></label>
<label><b>blkCnt</b> <% number_field ".isp.blkCnt" placeholder=\"4\" min=\"0\" %> <i>4 for small memory systems, 10 and more for performant SoCs</i></label>
<label><b>threadStackSize</b> <% number_field ".isp.threadStackSize" placeholder=\"16\" min=\"0\" %> <i>KB</i></label>
<label title="Set exposition in ms, from 1 to 500000 or auto"><b>exposure</b> <% number_field ".isp.exposure" placeholder=\"auto\" min=\"0\" max=\"500000\" %><i>set 0 for auto</i></label>
<label><b>aGain</b> <% number_field ".isp.aGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>dGain</b> <% number_field ".isp.dGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>ispGain</b> <% number_field ".isp.ispGain" placeholder=\"1\" min=\"0\" max=\"100\" %></label>
<label><b>drc</b> <% number_field ".isp.drc" placeholder=\"300\" min=\"0\" %> <i>:1</i></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="image">Image</h3>
<label><b>mirror</b> <% checkbox ".image.mirror" %></label>
<label title="turn image upside down"><b>flip</b> <% checkbox ".image.flip" %></label>
<label title="rotate image by none, 90 or 270 degrees"><b>rotate</b> <% select ".image.rotate" "none|90|270" %></label>
<label><b>contrast</b> <% number_field ".image.contrast" placeholder=\"auto\" min=\"0\" max=\"99\" %><i>set 0 for auto</i></label>
<label><b>hue</b> <% number_field ".image.hue" placeholder=\"50\" min=\"1\" max=\"99\" %></label>
<label><b>saturation</b> <% number_field ".image.saturation" placeholder=\"50\" min=\"1\" max=\"99\" %></label>
<label><b>luminance</b> <% number_field ".image.luminance" placeholder=\"auto\" min=\"0\" max=\"99\" %><i>set 0 for auto</i></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="osd">OSD</h3>
<label><b>enabled</b> <% checkbox ".osd.enabled" %></label>
<label><b>font</b> <% text_field ".osd.font" pattern=\"^[a-zA-Z0-9-_./]+$\" placeholder=\"/usr/lib/fonts/fonts.bin\" %></label>
<label><b>template</b> <% text_field ".osd.template" pattern=\"^[a-zA-Z0-9%: ]+$\" placeholder=\"%a %e %B %Y %H:%M:%S %Z\" %> <i>use %f for milliseconds (consumes more resources)</i></label>
<label><b>posX</b> <% number_field ".osd.posX" placeholder=\"-100\" min=\"-5000\" max=\"5000\" %> <i>+ from top/left, - from bottom/right</i></label>
<label><b>posY</b> <% number_field ".osd.posY" placeholder=\"-100\" min=\"-5000\" max=\"5000\" %> <i>+ from top/left, - from bottom/right</i></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="nightmode">Nightmode</h3>
<label><b>enabled</b> <% checkbox ".nightMode.enabled" %></label>
<label><b>irSensorPin</b> <% number_field ".nightMode.irSensorPin" placeholder=\"62\" min=\"1\" %></label>
<label><b>irSensorPinInvert</b> <% checkbox ".nightMode.irSensorPinInvert" %></label>
<label><b>irCutPin1</b> <% number_field ".nightMode.irCutPin1" placeholder=\"1\" min=\"1\" %></label>
<label><b>irCutPin2</b> <% number_field ".nightMode.irCutPin2" placeholder=\"2\" min=\"1\" %></label>
<label><b>pinSwitchDelayUs</b> <% number_field ".nightMode.pinSwitchDelayUs" placeholder=\"150\" min=\"0\" max=\"1000\" %> <i>IRcut filter pin switch delay in μs </i></label>
<h5 class="red">WARNING! Very long delay can damage IRcut filter!</h5>
<label title="turn on backlight illumination when night mode is on"><b>backlightPin</b> <% number_field ".nightMode.backlightPin" placeholder=\"65\" min=\"1\" max=\"100\" %></label>
<label title="use /night/{invert,on,off} endpoints to change mode by API for remote callers"><b>nightAPI</b> <% checkbox ".nightMode.nightAPI" %></label>
<label title="use special value for drc parameter in night mode"><b>drcOverride</b> <% number_field ".nightMode.drcOverride" placeholder=\"300\" min=\"1\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="records">Records</h3>
<label><b>enabled</b> <% checkbox ".records.enabled" %></label>
<label><b>path</b> <% text_field ".records.path" pattern=\"^[a-zA-Z0-9-_./%]+$\" placeholder=\"/mnt/mmc/%Y/%m/%d/%H.mp4\" %></label>
<label><b>maxUsage</b> <% number_field ".records.maxUsage" placeholder=\"95\" min=\"1\" max=\"100\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="video0">Video0</h3>
<label><b>enabled</b> <% checkbox ".video0.enabled" %></label>
<label><b>codec</b> <% select ".video0.codec" "h265|h264" %></label>
<label><b>size</b> <% text_field ".video0.size" pattern=\"^[xX0-9]+$\" placeholder=\"1920x1080\" %></label>
<label><b>fps</b> <% number_field ".video0.fps" placeholder=\"25\" min=\"1\" max=\"60\" %></label>
<label><b>bitrate</b> <% number_field ".video0.bitrate" placeholder=\"4096\" min=\"1\" max=\"115200\" %> <i>kbps</i></label>
<label><b>gopSize</b> <% number_field ".video0.gopSize" placeholder=\"1\" min=\"1\" max=\"180\" %> <i>send I-frame every second</i></label>
<label><b>gopMode</b> <% select ".video0.gopMode" "normal|dual|smart" %></label>
<label><b>rcMode</b> <% select ".video0.rcMode" "avbr" %></label>
<label><b>crop</b> <% text_field ".video0.crop" pattern=\"^[xX0-9]+$\" placeholder=\"0x0x960x540\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="video1">Video1</h3>
<label><b>enabled</b> <% checkbox ".video1.enabled" %></label>
<label><b>codec</b> <% select ".video1.codec" "h265|h264" %></label>
<label><b>size</b> <% text_field ".video1.size" pattern=\"^[xX0-9]+$\" placeholder=\"704x576\" %></label>
<label><b>fps</b> <% number_field ".video1.fps" placeholder=\"15\" min=\"1\" max=\"60\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="jpeg">JPEG</h3>
<label><b>enabled</b> <% checkbox ".jpeg.enabled" %></label>
<label><b>size</b> <% text_field ".jpeg.size" pattern=\"^[xX0-9]+$\" placeholder=\"1920x1080\" %></label>
<label><b>qfactor</b> <% number_field ".jpeg.qfactor" placeholder=\"50\" min=\"1\" max=\"99\" %> <i>JPEG quality</i></label>
<label><b>toProgressive</b> <% checkbox ".jpeg.toProgressive" %> <i>transform snapshot to Progressive JPEG</i></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="mjpeg">MJPEG</h3>
<label><b>size</b> <% text_field ".mjpeg.size" pattern=\"^[xX0-9]+$\" placeholder=\"640x360\" %></label>
<label><b>fps</b> <% number_field ".mjpeg.fps" placeholder=\"5\" min=\"1\" max=\"60\" %></label>
<label><b>bitrate</b> <% number_field ".mjpeg.bitrate" placeholder=\"1024\" min=\"1\" max=\"2048\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="audio">Audio</h3>
<label><b>enabled</b> <% checkbox ".audio.enabled" %></label>
<label><b>volume</b> <% number_field ".audio.volume" placeholder=\"auto\" min=\"0\" max=\"100\" %><i>set 0 for auto</i></label>
<label><b>srate</b> <% number_field ".audio.srate" placeholder=\"8000\" min=\"1\" max=\"44100\" %></label>
<label><b>codec</b> <% select ".audio.codec" "aac|mp3|opus|pcm" %> <i>default codec for RTSP and MP4 encoding</i></label>
<label><b>outputEnabled</b> <% checkbox ".audio.outputEnabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="rtsp">RTSP</h3>
<label><b>enabled</b> <% checkbox ".rtsp.enabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="hsl">HLS</h3>
<label><b>enabled</b> <% checkbox ".hls.enabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="youtube">Youtube</h3>
<label><b>enabled</b> <% checkbox ".youtube.enabled" %></label>
<label><b>key</b> <% text_field ".youtube.key" pattern=\"^[a-zA-Z0-9-]+$\" placeholder=\"xxxx-xxxx-xxxx-xxxx-xxxx\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="motiondetect">motionDetect</h3>
<label><b>enabled</b> <% checkbox ".motionDetect.enabled" %></label>
<label><b>profile</b> <% select ".motionDetect.profile" "outdoor|indoor" %></label>
<label><b>visualize</b> <% checkbox ".motionDetect.visualize" %></label>
<label><b>debug</b> <% checkbox ".motionDetect.debug" %></label>
<label title="ROI for motion detection algorithm e.g. top upper quadrant"><b>constraints</b> <% text_field ".motionDetect.constraints" pattern=\"^[xX0-9]+$\" placeholder=\"0x0x1296x760\" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="ipeye">IPEYE</h3>
<label><b>enabled</b> <% checkbox ".ipeye.enabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="netip">NETIP</h3>
<label><b>enabled</b> <% checkbox ".netip.enabled" %></label>
<label><b>user</b> <% text_field ".netip.user" placeholder=\"admin\" %></label>
<label><b>password</b> <% text_field ".netip.password" placeholder=\"6V0Y4HLF\" %></label>
<label><b>port</b> <% number_field ".netip.port" placeholder=\"34567\" min=\"1\" max=\"65535\" %></label>
<label><b>snapshots</b> <% checkbox ".netip.snapshots" %></label>
<label><b>ignore_set_time</b> <% checkbox ".netip.ignore_set_time" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="onvif">ONVIF</h3>
<label><b>enabled</b> <% checkbox ".onvif.enabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="raw">RAW</h3>
<label><b>enabled</b> <% checkbox ".raw.enabled" %></label>
<a href="#top">Top</a>
</div>

<div>
<h3 id="watchdog">Watchdog</h3>
<label><b>enabled</b> <% checkbox ".watchdog.enabled" %></label>
<label><b>timeout</b> <% number_field ".watchdog.timeout" placeholder=\"10\" min=\"1\" max=\"100\" %></label>
<a href="#top">Top</a>
</div>

<p><input type="submit" name="action" value="Save"></p>
</form>

<%in _footer.cgi %>