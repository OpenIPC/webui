#!/usr/bin/haserl
<?
  export PATH=/bin:/sbin:/usr/bin:/usr/sbin
  echo -e "Content-type: text/html\r\n\r\n"
?>

<html>
  <head>
    <link rel="shortcut icon" href="/assets/img/favicon.png">
  <style>
    input, select {
      width: 200px; 
    }
  </style>    
  </head>
  <body>
    <div align=center>
      <img src="https://openipc.org/images/logo_openipc.png" width="256">
      <form action="/cgi-bin/majestic-settings.cgi" method="POST" enctype="multipart/form-data">
<!--          System       -->
        <p><b>System</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">logLevel</td>
            <td>
              <select autocomplete="off" name=".system.logLevel">
                <option <? [ "$(yaml-cli -g .system.logLevel)" == "ERROR" ] && echo -n 'selected' ?> value="ERROR">ERROR</option>
                <option <? [ "$(yaml-cli -g .system.logLevel)" == "WARN"  ] && echo -n 'selected' ?> value="WARN">WARN</option>
                <option <? [ "$(yaml-cli -g .system.logLevel)" == "INFO"  ] && echo -n 'selected' ?> value="DEBUG">INFO</option>
                <option <? [ "$(yaml-cli -g .system.logLevel)" == "DEBUG" ] && echo -n 'selected' ?> value="DEBUG">DEBUG</option>
                <option <? [ "$(yaml-cli -g .system.logLevel)" == "TRACE" ] && echo -n 'selected' ?> value="TRACE">TRACE</option>
              </select>
            </td>
          </tr>
          <tr title="set the value to hardcode sensor configuration, otherwise
it will be inferred from SENSOR environment variable">
            <td align=right>sensorConfig</td>
            <td><input type="text" name=".system.sensorConfig" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .system.sensorConfig ?>" placeholder="/etc/sensors/imx222_1080p_line.ini" size="25"></td>
          </tr>
          <tr title="set custom directory for sensor configs">
            <td align=right>sensorConfigDir</td>
            <td><input type="text" name=".system.sensorConfigDir" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .system.sensorConfigDir ?>" placeholder="/etc/sensors" size="25"></td>
          </tr>
          <tr>
            <td align=right>webPort</td>
            <td><input type="text" name=".system.webPort" pattern="^[0-9]+$" value="<? yaml-cli -g .system.webPort ?>" placeholder="80" size="25"></td>
          </tr>
          <tr>
            <td align=right>staticDir</td>
            <td><input type="text" name=".system.staticDir" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .system.staticDir ?>" placeholder="/var/www/html" size="25"></td>
          </tr>
          <tr>
            <td align=right>httpsPort</td>
            <td><input type="text" name=".system.httpsPort" pattern="^[0-9]+$" value="<? yaml-cli -g .system.httpsPort ?>" placeholder="443" size="25"></td>
          </tr>
          <tr>
            <td align=right>httpsCertificate</td>
            <td><input type="text" name=".system.httpsCertificate" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .system.httpsCertificate ?>" placeholder="/etc/ssl/certs/www.example.com.crt" size="25"></td>
          </tr>
          <tr>
            <td align=right>httpsCertificateKey</td>
            <td><input type="text" name=".system.httpsCertificateKey" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .system.httpsCertificateKey ?>" placeholder="/etc/ssl/certs/www.example.com.key" size="25"></td>
          </tr>
          <tr>
            <td align=right>updateChannel</td>
            <td>
              <select autocomplete="off" name=".system.updateChannel">
                <option <? [ "$(yaml-cli -g .system.updateChannel)" == "testing" ] && echo -n 'selected' ?> value="testing">testing</option>
                <option <? [ "$(yaml-cli -g .system.updateChannel)" == "beta"    ] && echo -n 'selected' ?> value="beta">beta</option>
                <option <? [ "$(yaml-cli -g .system.updateChannel)" == "stable"  ] && echo -n 'selected' ?> value="stable">stable</option>
                <option <? [ "$(yaml-cli -g .system.updateChannel)" == "none"    ] && echo -n 'selected' ?> value="none">none</option>
              </select>
            </td>
          </tr>
          <tr title="maximum buffer size of each client in Kbytes">
            <td align=right>buffer</td>
            <td><input type="text" name=".system.buffer" pattern="^[0-9]+$" value="<? yaml-cli -g .system.buffer ?>" placeholder="1024" size="25"></td>
          </tr>
        </table>
<!--          ISP       -->
        <p><b>ISP</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">memMode</td>
            <td>
              <select autocomplete="off" name=".isp.memMode">
                <option <? [ "$(yaml-cli -g .isp.memMode)" == "normal"     ] && echo -n 'selected' ?> value="normal">normal</option>
                <option <? [ "$(yaml-cli -g .isp.memMode)" == "reduction"  ] && echo -n 'selected' ?> value="reduction">reduction</option>
              </select>
            </td>
          </tr>
          <tr title="Automatic frame rate reduction mode (slow shutter mode)">
            <td align=right>slowShutter</td>
            <td>
              <select autocomplete="off" name=".isp.slowShutter">
                <option <? [ "$(yaml-cli -g .isp.slowShutter)" == "disabled" ] && echo -n 'selected' ?> value="disabled">disabled</option>
                <option <? [ "$(yaml-cli -g .isp.slowShutter)" == "low"      ] && echo -n 'selected' ?> value="low">low</option>
                <option <? [ "$(yaml-cli -g .isp.slowShutter)" == "medium"   ] && echo -n 'selected' ?> value="medium">medium</option>
                <option <? [ "$(yaml-cli -g .isp.slowShutter)" == "high"     ] && echo -n 'selected' ?> value="high">high</option>
              </select>
            </td>
            </tr>
          <tr title="use 50 or 60 for indoor camera depending on your location">
            <td align=right>antiFlicker</td>
            <td>
              <select autocomplete="off" name=".isp.antiFlicker">
                <option <? [ "$(yaml-cli -g .isp.antiFlicker)" == "disabled" ] && echo -n 'selected' ?> value="disabled">disabled</option>
                <option <? [ "$(yaml-cli -g .isp.antiFlicker)" == "50"       ] && echo -n 'selected' ?> value="50">50</option>
                <option <? [ "$(yaml-cli -g .isp.antiFlicker)" == "60"       ] && echo -n 'selected' ?> value="60">60</option>
              </select>
            </td>
            </tr>
          <tr>
            <td align=right>alignWidth</td>
            <td><input type="text" name=".isp.alignWidth" pattern="^[0-9]+$" value="<? yaml-cli -g .isp.alignWidth ?>" placeholder="8" size="25"></td>
          </tr>
          <tr title="4 for small memory systems and 10 and more for performant SoCs">
            <td align=right>blkCnt</td>
            <td><input type="text" name=".isp.blkCnt" pattern="^[0-9]+$" value="<? yaml-cli -g .isp.blkCnt ?>" placeholder="4" size="25"></td>
          </tr>
          <tr title="in Kbytes">
            <td align=right>threadStackSize</td>
            <td><input type="text" name=".isp.threadStackSize" pattern="^[0-9]+$" value="<? yaml-cli -g .isp.threadStackSize ?>" placeholder="16" size="25"></td>
          </tr>
          <tr title="Used to implement dynamic range compression">
            <td align=right>drc</td>
            <td><input type="text" name=".isp.drc" pattern="^[0-9]+$" value="<? yaml-cli -g .isp.drc ?>" placeholder="300" size="25"></td>
          </tr>
        </table>  
<!--          Image       -->
        <p><b>Image</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">mirror</td>
            <td>
              <select autocomplete="off" name=".image.mirror">
                <option <? [ "$(yaml-cli -g .image.mirror)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .image.mirror)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr title="turn image upside down">
            <td align=right>flip</td>
            <td>
              <select autocomplete="off" name=".image.flip">
                <option <? [ "$(yaml-cli -g .image.flip)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .image.flip)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
            </tr>
          <tr title="rotate image by none, 90 or 270 degrees">
            <td align=right>rotate</td>
            <td>
              <select autocomplete="off" name=".image.rotate">
                <option <? [ "$(yaml-cli -g .image.rotate)" == "none" ] && echo -n 'selected' ?> value="none">none</option>
                <option <? [ "$(yaml-cli -g .image.rotate)" == "90"   ] && echo -n 'selected' ?> value="90">90</option>
                <option <? [ "$(yaml-cli -g .image.rotate)" == "270"  ] && echo -n 'selected' ?> value="270">270</option>
              </select>
            </td>
            </tr>
          <tr title="auto or 1-99 (50)">
            <td align=right>contrast</td>
            <td><input type="text" name=".image.contrast" pattern="^[auto0-9]+$" value="<? yaml-cli -g .image.contrast ?>" placeholder="auto" size="25"></td>
          </tr>
          <tr>
            <td align=right>hue</td>
            <td><input type="text" name=".image.hue" pattern="^[0-9]+$" value="<? yaml-cli -g .image.hue ?>" placeholder="50" size="25"></td>
          </tr>
          <tr>
            <td align=right>saturation</td>
            <td><input type="text" name=".image.saturation" pattern="^[0-9]+$" value="<? yaml-cli -g .image.saturation ?>" placeholder="50" size="25"></td>
          </tr>
          <tr title="auto or 1-99 (50)">
            <td align=right>luminance</td>
            <td><input type="text" name=".image.luminance" pattern="^[auto0-9]+$" value="<? yaml-cli -g .image.luminance ?>" placeholder="auto" size="25"></td>
          </tr>
        </table>
<!--          OSD       -->
        <p><b>OSD</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".osd.enabled">
                <option <? [ "$(yaml-cli -g .osd.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .osd.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>font</td>
            <td><input type="text" name=".osd.font" pattern="^[a-zA-Z0-9-_./]+$" value="<? yaml-cli -g .osd.font ?>" placeholder="/usr/lib/fonts/fonts.bin" size="25"></td>
          </tr>
          <tr title="add '%f' to show milliseconds (consumes more resources)">
            <td align=right>template</td>
            <td><input type="text" name=".osd.template" pattern="^[a-zA-Z0-9%: ]+$" value="<? yaml-cli -g .osd.template ?>" placeholder="%a %e %B %Y %H:%M:%S %Z" size="25"></td>
          </tr>
          <tr title="positive values count from left and top
negative ones from right and bottom">
            <td align=right>posX</td>
            <td><input type="text" name=".osd.posX" pattern="^[0-9-]+$" value="<? yaml-cli -g .osd.posX ?>" placeholder="-100" size="25"></td>
          </tr>
          <tr title="positive values count from left and top
negative ones from right and bottom">
            <td align=right>posY</td>
            <td><input type="text" name=".osd.posY" pattern="^[0-9-]+$" value="<? yaml-cli -g .osd.posY ?>" placeholder="-100" size="25"></td>
          </tr>
        </table>
<!--          Nightmode       -->
        <p><b>Nightmode</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".nightMode.enabled">
                <option <? [ "$(yaml-cli -g .nightMode.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .nightMode.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>irSensorPin</td>
            <td><input type="text" name=".nightMode.irSensorPin" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.irSensorPin ?>" placeholder="62" size="25"></td>
          </tr>
          <tr>
            <td align=right width="150">irSensorPinInvert</td>
            <td>
              <select autocomplete="off" name=".nightMode.irSensorPinInvert">
                <option <? [ "$(yaml-cli -g .nightMode.irSensorPinInvert)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .nightMode.irSensorPinInvert)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>irCutPin1</td>
            <td><input type="text" name=".nightMode.irCutPin1" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.irCutPin1 ?>" placeholder="1" size="25"></td>
          </tr>
          <tr>
            <td align=right>irCutPin2</td>
            <td><input type="text" name=".nightMode.irCutPin2" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.irCutPin2 ?>" placeholder="2" size="25"></td>
          </tr>
          <tr title="switch delay in us on IRcut filter pins. WARNING!
a very long delay can damage the IRcut filter!!!">
            <td align=right>pinSwitchDelayUs</td>
            <td><input type="text" name=".nightMode.pinSwitchDelayUs" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.pinSwitchDelayUs ?>" placeholder="150" size="25"></td>
          </tr>
          <trr title="turn on backlight illumination when night mode is on">
            <td align=right>backlightPin</td>
            <td><input type="text" name=".nightMode.backlightPin" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.backlightPin ?>" placeholder="65" size="25"></td>
          </tr>
          <tr title="use /night/{invert,on,off} endpoints to change mode by API for remote callers">
            <td align=right width="150">nightAPI</td>
            <td>
              <select autocomplete="off" name=".nightMode.nightAPI">
                <option <? [ "$(yaml-cli -g .nightMode.nightAPI)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .nightMode.nightAPI)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr title="use special value for drc parameter in night mode">
            <td align=right>drcOverride</td>
            <td><input type="text" name=".nightMode.drcOverride" pattern="^[0-9]+$" value="<? yaml-cli -g .nightMode.drcOverride ?>" placeholder="300" size="25"></td>
          </tr>
        </table>
<!--          Records       -->
        <p><b>Records</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".records.enabled">
                <option <? [ "$(yaml-cli -g .records.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .records.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>path</td>
            <td><input type="text" name=".records.path" pattern="^[a-zA-Z0-9-_./%]+$" value="<? yaml-cli -g .records.path ?>" placeholder="/mnt/mmc/%Y/%m/%d/%H.mp4" size="25"></td>
          </tr>
          <tr>
            <td align=right>maxUsage</td>
            <td><input type="text" name=".records.maxUsage" pattern="^[0-9]+$" value="<? yaml-cli -g .records.maxUsage ?>" placeholder="95" size="25"></td>
          </tr>
        </table>
<!--          Video0       -->
        <p><b>Video0</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".video0.enabled">
                <option <? [ "$(yaml-cli -g .video0.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .video0.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>codec</td>
            <td>
              <select autocomplete="off" name=".video0.codec">
                <option <? [ "$(yaml-cli -g .video0.codec)" == "h265" ] && echo -n 'selected' ?> value="h265">h265</option>
                <option <? [ "$(yaml-cli -g .video0.codec)" == "h264" ] && echo -n 'selected' ?> value="h264">h264</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>size</td>
            <td><input type="text" name=".video0.size" pattern="^[xX0-9]+$" value="<? yaml-cli -g .video0.size ?>" placeholder="1920x1080" size="25"></td>
          </tr>
          <tr>
            <td align=right>fps</td>
            <td><input type="text" name=".video0.fps" pattern="^[0-9]+$" value="<? yaml-cli -g .video0.fps ?>" placeholder="25" size="25"></td>
          </tr>
          <tr title="Kbits per second">
            <td align=right>bitrate</td>
            <td><input type="text" name=".video0.bitrate" pattern="^[0-9]+$" value="<? yaml-cli -g .video0.bitrate ?>" placeholder="4096" size="25"></td>
          </tr>
          <tr title="send I-frame each 1 second">
            <td align=right>gopSize</td>
            <td><input type="text" name=".video0.gopSize" pattern="^[0-9.]+$" value="<? yaml-cli -g .video0.gopSize ?>" placeholder="1" size="25"></td>
          </tr>
          <tr>
            <td align=right>gopMode</td>
            <td>
              <select autocomplete="off" name=".video0.gopMode">
                <option <? [ "$(yaml-cli -g .video0.gopMode)" == "normal" ] && echo -n 'selected' ?> value="normal">normal</option>
                <option <? [ "$(yaml-cli -g .video0.gopMode)" == "dual"   ] && echo -n 'selected' ?> value="dual">dual</option>
                <option <? [ "$(yaml-cli -g .video0.gopMode)" == "smart"  ] && echo -n 'selected' ?> value="smart">smart</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>rcMode</td>
            <td>
              <select autocomplete="off" name=".video0.rcMode">
                <option <? [ "$(yaml-cli -g .video0.rcMode)" == "avbr" ] && echo -n 'selected' ?> value="avbr">avbr</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>crop</td>
            <td><input type="text" name=".video0.crop" pattern="^[xX0-9]+$" value="<? yaml-cli -g .video0.crop ?>" placeholder="0x0x960x540" size="25"></td>
          </tr>
        </table>
<!--          Video1       -->
        <p><b>Video1</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".video1.enabled">
                <option <? [ "$(yaml-cli -g .video1.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .video1.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>codec</td>
            <td>
              <select autocomplete="off" name=".video1.codec">
                <option <? [ "$(yaml-cli -g .video1.codec)" == "h265" ] && echo -n 'selected' ?> value="h265">h265</option>
                <option <? [ "$(yaml-cli -g .video1.codec)" == "h264" ] && echo -n 'selected' ?> value="h264">h264</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>size</td>
            <td><input type="text" name=".video1.size" pattern="^[xX0-9]+$" value="<? yaml-cli -g .video1.size ?>" placeholder="704x576" size="25"></td>
          </tr>
          <tr>
            <td align=right>fps</td>
            <td><input type="text" name=".video1.fps" pattern="^[0-9]+$" value="<? yaml-cli -g .video1.fps ?>" placeholder="15" size="25"></td>
          </tr>
        </table>
<!--          jpeg       -->
        <p><b>JPEG</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".jpeg.enabled">
                <option <? [ "$(yaml-cli -g .jpeg.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .jpeg.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>size</td>
            <td><input type="text" name=".jpeg.size" pattern="^[xX0-9]+$" value="<? yaml-cli -g .jpeg.size ?>" placeholder="1920x1080" size="25"></td>
          </tr>
          <tr title="[1..99] jpeg quality">
            <td align=right>qfactor</td>
            <td><input type="text" name=".jpeg.qfactor" pattern="^[0-9]+$" value="<? yaml-cli -g .jpeg.qfactor ?>" placeholder="50" size="25"></td>
          </tr>
          <tr title="make additional step to transform snapshot to Progressive JPEG">
            <td align=right>toProgressive</td>
            <td>
              <select autocomplete="off" name=".jpeg.toProgressive">
                <option <? [ "$(yaml-cli -g .jpeg.toProgressive)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .jpeg.toProgressive)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          mjpeg       -->
        <p><b>MJPEG</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">size</td>
            <td><input type="text" name=".mjpeg.size" pattern="^[xX0-9]+$" value="<? yaml-cli -g .mjpeg.size ?>" placeholder="640x360" size="25"></td>
          </tr>
          <tr>
            <td align=right>fps</td>
            <td><input type="text" name=".mjpeg.fps" pattern="^[0-9]+$" value="<? yaml-cli -g .mjpeg.fps ?>" placeholder="5" size="25"></td>
          </tr>
          <tr>
            <td align=right>bitrate</td>
            <td><input type="text" name=".mjpeg.bitrate" pattern="^[0-9]+$" value="<? yaml-cli -g .mjpeg.bitrate ?>" placeholder="1024" size="25"></td>
          </tr>
        </table>
<!--          audio       -->
        <p><b>Audio</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".audio.enabled">
                <option <? [ "$(yaml-cli -g .audio.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .audio.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>volume</td>
            <td><input type="text" name=".audio.volume" pattern="^[auto0-9]+$" value="<? yaml-cli -g .audio.volume ?>" placeholder="auto" size="25"></td>
          </tr>
          <tr>
            <td align=right>srate</td>
            <td><input type="text" name=".audio.srate" pattern="^[0-9]+$" value="<? yaml-cli -g .audio.srate ?>" placeholder="8000" size="25"></td>
          </tr>
          <tr title="select default codec for RTSP and MP4 encoding">
            <td align=right>codec</td>
            <td>
              <select autocomplete="off" name=".audio.codec">
                <option <? [ "$(yaml-cli -g .audio.codec)" == "aac" ] && echo -n 'selected' ?> value="aac">aac</option>
                <option <? [ "$(yaml-cli -g .audio.codec)" == "mp3"  ] && echo -n 'selected' ?> value="mp3">mp3</option>
                <option <? [ "$(yaml-cli -g .audio.codec)" == "opus"  ] && echo -n 'selected' ?> value="opus">opus</option>
                <option <? [ "$(yaml-cli -g .audio.codec)" == "pcm"  ] && echo -n 'selected' ?> value="pcm">pcm</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>outputEnabled</td>
            <td>
              <select autocomplete="off" name=".audio.outputEnabled">
                <option <? [ "$(yaml-cli -g .audio.outputEnabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .audio.outputEnabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          RTSP       -->
        <p><b>RTSP</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".rtsp.enabled">
                <option <? [ "$(yaml-cli -g .rtsp.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .rtsp.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          HLS       -->
        <p><b>HLS</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".hls.enabled">
                <option <? [ "$(yaml-cli -g .hls.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .hls.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          Youtube       -->
        <p><b>Youtube</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".youtube.enabled">
                <option <? [ "$(yaml-cli -g .youtube.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .youtube.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
            <td align=right>key</td>
            <td><input type="text" name=".youtube.key" pattern="^[a-zA-Z0-9-]+$" value="<? yaml-cli -g .youtube.key ?>" placeholder="xxxx-xxxx-xxxx-xxxx-xxxx" size="25"></td>
          </tr>
        </table>
<!--          motionDetect       -->
        <p><b>motionDetect</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".motionDetect.enabled">
                <option <? [ "$(yaml-cli -g .motionDetect.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .motionDetect.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>profile</td>
            <td>
              <select autocomplete="off" name=".motionDetect.profile">
                <option <? [ "$(yaml-cli -g .motionDetect.profile)" == "outdoor" ] && echo -n 'selected' ?> value="outdoor">outdoor</option>
                <option <? [ "$(yaml-cli -g .motionDetect.profile)" == "indoor"  ] && echo -n 'selected' ?> value="indoor">indoor</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>visualize</td>
            <td>
              <select autocomplete="off" name=".motionDetect.visualize">
                <option <? [ "$(yaml-cli -g .motionDetect.visualize)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .motionDetect.visualize)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>debug</td>
            <td>
              <select autocomplete="off" name=".motionDetect.debug">
                <option <? [ "$(yaml-cli -g .motionDetect.debug)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .motionDetect.debug)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr title="ROI for motion detection algorithm
e.g. top upper quadrant">
            <td align=right>constraints</td>
            <td><input type="text" name=".motionDetect.constraints" pattern="^[xX0-9]+$" value="<? yaml-cli -g .motionDetect.constraints ?>" placeholder="0x0x1296x760" size="25"></td>
          </tr>
        </table>
<!--          ipeye       -->
        <p><b>IPEYE</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".ipeye.enabled">
                <option <? [ "$(yaml-cli -g .ipeye.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .ipeye.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          netip       -->
        <p><b>NETIP</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".netip.enabled">
                <option <? [ "$(yaml-cli -g .netip.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .netip.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
          <tr>
            <td align=right>user</td>
            <td><input type="text" name=".netip.user" value="<? yaml-cli -g .netip.user ?>" placeholder="admin" size="25"></td>
          </tr>
          <tr title="12345 password">
            <td align=right>password</td>
            <td><input type="text" name=".netip.password" value="<? yaml-cli -g .netip.password ?>" placeholder="6V0Y4HLF" size="25"></td>
          </tr>
          <tr>
            <td align=right>port</td>
            <td><input type="text" name=".netip.port" pattern="^[0-9]+$" value="<? yaml-cli -g .netip.port ?>" placeholder="34567" size="25"></td>
          </tr>
          <tr>
            <td align=right>snapshots</td>
            <td>
              <select autocomplete="off" name=".netip.snapshots">
                <option <? [ "$(yaml-cli -g .netip.snapshots)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .netip.snapshots)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          ONVIF       -->
        <p><b>ONVIF</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".onvif.enabled">
                <option <? [ "$(yaml-cli -g .onvif.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .onvif.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          raw       -->
        <p><b>RAW</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".raw.enabled">
                <option <? [ "$(yaml-cli -g .raw.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .raw.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
        </table>
<!--          watchdog       -->
        <p><b>Watchdog</b></p>
        <table border="0">          
          <tr>
            <td align=right width="150">enabled</td>
            <td>
              <select autocomplete="off" name=".watchdog.enabled">
                <option <? [ "$(yaml-cli -g .watchdog.enabled)" == "false" ] && echo -n 'selected' ?> value="false">false</option>
                <option <? [ "$(yaml-cli -g .watchdog.enabled)" == "true"  ] && echo -n 'selected' ?> value="true">true</option>
              </select>
            </td>
          </tr>
            <td align=right>timeout</td>
            <td><input type="text" name=".watchdog.timeout" pattern="^[0-9]+$" value="<? yaml-cli -g .watchdog.timeout ?>" placeholder="10" size="25"></td>
          </tr>
        </table>
      <p><input type="submit" name="action" value="Save" style="width:46;"></p>
      </form>
    </div>
  </body>
</html>