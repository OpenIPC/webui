<%
# line format: parameter|label|units|type|o,p,t,i,o,n,s|
mj="
.system.logLevel|Severity of logging.||select|ERROR,WARN,INFO,DEBUG,TRACE
.system.sensorConfig|Path to sensor configuration file.||string|
.system.sensorConfigDir|Path to sensor configs directory.||string|
.system.webPort|Port for HTTP access.||number|1-65535
.system.staticDir|Home directory for static files.||string|
.system.httpsPort|Port for HTTPS access.||number|1-65535
.system.httpsCertificate|Path to public SSL certificate.||string|
.system.httpsCertificateKey|Path to private SSL key.||string|
.system.updateChannel|Channel to use for updates.||select|testing,beta,stable,none
.system.buffer|Maximum buffer size per client.|KB|number|
.isp.memMode|Memory mode.||select|normal,reduction
.isp.slowShutter|Automatic frame rate reduction mode (slow shutter mode).||string|
.isp.antiFlicker|Utility frequency in your power line.|Hz|select|50,60
.isp.alignWidth|Align width.||number|
.isp.blkCnt|Use 4 for small memory systems, 10+ for performant SoCs.||number|
.isp.threadStackSize|Thread stack size.|KB|number|
.isp.exposure|Exposition time. from 1 to 500000 or auto.|ms|number|
.isp.aGain|aGain||number|
.isp.dGain|dGain||number|
.isp.ispGain|ispGain||number|
.isp.drc|Dynamic Range Compression rate.|:1|number|
.image.mirror|Flip image horizontally.||boolean|true,false
.image.flip|Flip image vertically.||boolean|true,false
.image.rotate|Rotate image clockwise.|°|number|0,90,270
.image.contrast|Image contrast.|%|number|
.image.hue|Image hue.|%|number|
.image.saturation|Image saturation.|%|number|
.image.luminance|Image luminance.|%|number|
.osd.enabled|Enable On-Screen Display (OSD).||boolean|true,false
.osd.font|Path to font file ti use for OSD.||string|
.osd.template|OSD template. Supports strftime() format.||string|
.osd.posX|Horizontal position of OSD.|px|number|
.osd.posY|Vertical position of OSD.|px|number|
.osd.privacyMasks|Coordinates of masked areas separated by commas.|px|number|
.nightmode.enabled|Enable night mode.||boolean|true,false
.nightmode.irSensorPin|GPIO pin of signal from IR sensor.||number|
.nightmode.irSensorPinInvert|IR sensor is inverted.||boolean|true,false
.nightmode.irCutPin1|GPIO pin1 of signal for IRcut filter.||number|
.nightmode.irCutPin2|GPIO pin2 of signal for IRcut filter.||number|
.nightmode.pinSwitchDelayUs|Delay before triggering IRcut filter.||number|
.nightmode.backlightPin|GPIO pin to turn on backlight illumination in night mode.||number|
.nightmode.nightAPI|Use night mode API.||boolean|true,false
.nightmode.drcOverride|DRC in night mode.||number|
.records.enabled|Enable saving records.||boolean|true,false
.records.path|Template for saving video records. Supports strftime() format.||string|
.records.maxUsage|Limit of available space usage.|%|number|
.video0.enabled|Enable Video0.||boolean|true,false
.video0.codec|Video0 codec.||select|h264,h265
.video0.size|Video resolution.|px|string|1920x1080,1280x720,704x576
.video0.fps|Video frame rate.|frames|number|
.video0.bitrate|Video bitrate.|kbps|number|
.video0.gopSize|Send I-frame each 1 second.||number|
.video0.gopMode|GOP mode.||select|normal,dual,smart
.video0.rcMode|RC mode.||string|
.video0.crop|Crop video to size.|px|string|
.video1.enabled|Enable Video1.||boolean|true,false
.video1.codec|Video1 codec.||select|h264,h265
.video1.size|Video1 resolution.|px|string|1920x1080,1280x720,704x576
.video1.fps|Video1 frame rate.|frames|number|
.video1.bitrate|Video1 bitrate.|kbps|number|
.video1.gopSize|Send I-frame each 1 second.||number|
.video1.gopMode|GOP mode.||string|normal,dual,smart
.video1.rcMode|RC mode.||string|
.video1.crop|Crop video to size.|px|string|
.jpeg.enabled|Enable JPEG support.||boolean|true,false
.jpeg.size|Snapshot size.|px|string|
.jpeg.qfactor|JPEG quality level.|%|number|
.jpeg.toProgressive|Transform to Progressive JPEG.||boolean|true,false
.mjpeg.size|Video resolution.|px|string|
.mjpeg.fps|Video framerate.|frames|number|
.mjpeg.bitrate|Video bitrate.|kbps|number|
.audio.enabled|Enable audio.||boolean|true,false
.audio.volume|Audio volume level.|%|number|
.audio.srate|Audio sampling rate.|kHz|number|
.audio.codec|Codec for RTSP and MP4 encoding.||select|mp3,opus,aac,pcm
.audio.outputEnabled|Audio card.||boolean|
.rtsp.enabled|Enable output.||boolean|true,false
.hls.enabled|Enable HTTP Live Streaming (HLS).||boolean|true,false
.youtube.enabled|Enable Youtube support.||boolean|true,false
.youtube.key|Youtube API key.||string|
.motionDetect.enabled|Enable motion detection.||boolean|true,false
.motionDetect.profile|Motion detection profile to use.||select|outdoor,indoor
.motionDetect.visualize|Visualize motion detection.||boolean|true,false
.motionDetect.debug|Enable debugging.||boolean|true,false
.motionDetect.constraints|Regions of Interest (ROI) for motion detection.|px|string|
.ipeye.enabled|Enable IP EYE support.||boolean|true,false
.netip.enabled|Enable NETIP protocol support.||boolean|true,false
.netip.user|NETIP user.||string|
.netip.password|NETIP password.||string|
.netip.port|NETIP port.||number|
.netip.snapshots|NETIP snaphots.||string|
.netip.ignore_set_time|Ignore set time.||boolean|true,false
.onvif.enabled|Enable ONVIF protocol support.||boolean|true,false
.raw.enabled|Enable raw feed support.||boolean|true,false
.raw.mode|Raw feed mode.||select|slow,fast,none
.watchdog.enabled|Enable watchdog.||boolean|true,false
.watchdog.timeout|Watchdog timeout||number|
.cloud.enabled|Enable cloud support.||boolean|true,false
"
%>