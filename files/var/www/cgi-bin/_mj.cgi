<%
# line format: parameter|label|units|type|o,p,t,i,o,n,s|placeholder
mj="
.system.logLevel|Severity of logging.||select|ERROR,WARN,INFO,DEBUG,TRACE|TRACE
.system.sensorConfig|Path to sensor configuration file.||string||/etc/sensors/imx222_1080p_line.ini
.system.sensorConfigDir|Path to sensor configs directory.||string||/etc/sensors
.system.webPort|Port for HTTP access.||number|1-65535|80
.system.staticDir|Home directory for static files.||string||/var/www/html
.system.httpsPort|Port for HTTPS access.||number|1-65535|443
.system.httpsCertificate|Path to public SSL certificate.||string||/etc/ssl/certs/www.example.com.crt
.system.httpsCertificateKey|Path to private SSL key.||string||/etc/ssl/private/www.example.com.key
.system.updateChannel|Channel to use for updates.||select|testing,beta,stable,none|stable
.system.buffer|Maximum buffer size per client.|KB|number||1024
.isp.memMode|Memory mode.||select|normal,reduction|reduction
.isp.slowShutter|Automatic frame rate reduction mode (slow shutter mode).||select|disabled,low,medium,high|low
.isp.antiFlicker|Anti-flicker (utility frequency).|Hz|select|disabled,50,60|disabled
.isp.alignWidth|Align width.||number||8
.isp.blkCnt|Use 4 for small memory systems, 10+ for performant SoCs.||number|1-32|4
.isp.threadStackSize|Thread stack size.|KB|number|1-32|16
.isp.exposure|Exposition time. from 1 to 500000 or auto.|ms|number|1-500000|0
.isp.aGain|aGain||number|0.1-1.0|1
.isp.dGain|dGain||number|0.1-1.0|1
.isp.ispGain|ispGain||number|0.1-1.0|1
.isp.drc|Dynamic Range Compression rate.|:1|number|1-1000|300
.image.mirror|Flip image horizontally.||boolean|true,false|false
.image.flip|Flip image vertically.||boolean|true,false|false
.image.rotate|Rotate image clockwise.|°|select|0,90,270|0
.image.contrast|Image contrast.|%|range|0-100|0
.image.hue|Image hue.|%|range|1-100|50
.image.saturation|Image saturation.|%|range|1-100|50
.image.luminance|Image luminance.|%|range|0-100|0
.osd.enabled|Enable On-Screen Display (OSD).||boolean|true,false|false
.osd.font|Path to font file ti use for OSD.||string||/usr/lib/fonts/fonts.bin
.osd.template|OSD template. Supports strftime() format.||string||%a %e %B %Y %H:%M:%S %Z
.osd.posX|Horizontal position of OSD.|px|number|-2000-2000|-100
.osd.posY|Vertical position of OSD.|px|number|-2000-2000|-100
.osd.privacyMasks|Coordinates of masked areas separated by commas.|px|string||0x0x234x640,2124x0x468x1300
.nightmode.enabled|Enable night mode.||boolean|true,false|false
.nightmode.irSensorPin|GPIO pin of signal from IR sensor.||number|1-100|62
.nightmode.irSensorPinInvert|IR sensor is inverted.||boolean|true,false|false
.nightmode.irCutPin1|GPIO pin1 of signal for IRcut filter.||number|1-100|1
.nightmode.irCutPin2|GPIO pin2 of signal for IRcut filter.||number|1-100|2
.nightmode.pinSwitchDelayUs|Delay before triggering IRcut filter.||number|0-1000|150
.nightmode.backlightPin|GPIO pin to turn on backlight illumination in night mode.|1-100|number||65
.nightmode.nightAPI|Use night mode API.||boolean|true,false|false
.nightmode.drcOverride|DRC in night mode.||number|1-1000|300
.records.enabled|Enable saving records.||boolean|true,false|false
.records.path|Template for saving video records. Supports strftime() format.||string||/mnt/mmc/%Y/%m/%d/%H.mp4
.records.maxUsage|Limit of available space usage.|%|range|1-100|95
.video0.enabled|Enable Video0.||boolean|true,false|true
.video0.codec|Video0 codec.||select|h264,h265|h264
.video0.size|Video resolution.|px|string|1920x1080,1280x720,704x576|1920x1080
.video0.fps|Video frame rate.|frames|number|1-60|25
.video0.bitrate|Video bitrate.|kbps|number|1-4096|4096
.video0.gopSize|Send I-frame each 1 second.||number|1-20|1
.video0.gopMode|GOP mode.||select|normal,dual,smart|normal
.video0.rcMode|RC mode.||select|avbr|avbr
.video0.crop|Crop video to size.|px|string||0x0x960x540
.video1.enabled|Enable Video1.||boolean|true,false|false
.video1.codec|Video1 codec.||select|h264,h265|h264
.video1.size|Video1 resolution.|px|string|1920x1080,1280x720,704x576|704x576
.video1.fps|Video1 frame rate.|frames|number|1-60|15
.video1.bitrate|Video1 bitrate.|kbps|number|1-4096|2048
.video1.gopSize|Send I-frame each 1 second.||number|1-20|1
.video1.gopMode|GOP mode.||string|normal,dual,smart|normal
.video1.rcMode|RC mode.||string|avbr|avbr
.video1.crop|Crop video to size.|px|string||0x0x960x540
.jpeg.enabled|Enable JPEG support.||boolean|true,false|true
.jpeg.size|Snapshot size.|px|string||1920x1080
.jpeg.qfactor|JPEG quality level.|%|range|1-100|50
.jpeg.toProgressive|Transform to Progressive JPEG.||boolean|true,false|false
.mjpeg.size|Video resolution.|px|string||640x360
.mjpeg.fps|Video framerate.|frames|number|1-30|5
.mjpeg.bitrate|Video bitrate.|kbps|number|1-4096|1024
.audio.enabled|Enable audio.||boolean|true,false|false
.audio.volume|Audio volume level.|%|range|1-100|100
.audio.srate|Audio sampling rate.|kHz|number|1-44100|8000
.audio.codec|Codec for RTSP and MP4 encoding.||select|mp3,opus,aac,pcm|opus
.audio.outputEnabled|Audio card.||boolean||hw:3
.rtsp.enabled|Enable output.||boolean|true,false|true
.rtsp.port|Port for RTSP protocol.||number|1-65535|554
.hls.enabled|Enable HTTP Live Streaming (HLS).||boolean|true,false|true
.youtube.enabled|Enable Youtube support.||boolean|true,false|false
.youtube.key|Youtube API key.||string||xxxx-xxxx-xxxx-xxxx-xxxx
.motionDetect.enabled|Enable motion detection.||boolean|true,false|false
.motionDetect.profile|Motion detection profile to use.||select|outdoor,indoor|outdoor
.motionDetect.visualize|Visualize motion detection.||boolean|true,false|true
.motionDetect.debug|Enable debugging.||boolean|true,false|true
.motionDetect.constraints|Regions of Interest (ROI) for motion detection.|px|string||0x0x1296x760
.ipeye.enabled|Enable IP EYE support.||boolean|true,false|false
.netip.enabled|Enable NETIP protocol support.||boolean|true,false|false
.netip.user|NETIP user.||string||admin
.netip.password|NETIP password.||string||6V0Y4HLF
.netip.port|NETIP port.||number|1-65535|34567
.netip.snapshots|NETIP snaphots.||boolean|true,false|true
.netip.ignore_set_time|Ignore set time.||boolean|true,false|false
.onvif.enabled|Enable ONVIF protocol support.||boolean|true,false|false
.raw.enabled|Enable raw feed support.||boolean|true,false|false
.raw.mode|Raw feed mode.||select|slow,fast,none|slow
.watchdog.enabled|Enable watchdog.||boolean|true,false|true
.watchdog.timeout|Watchdog timeout||number|1-1000|10
.cloud.enabled|Enable cloud support.||boolean|true,false|false
"
%>
