#!/bin/sh

network_address=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)

tOptions_tools_action="ping,trace"
tOptions_web_version="master|Stable,dev|Development"
tOptions_ipeye_rtsp_feed="rtsp://${network_address}/stream=0,rtsp://${network_address}/stream=1"

sP_mj_restore_file="majestic.yaml"
sP_tools_target="FQDN or IP address"
sP_socks5_port="1080"
sP_webui_password="K3wLHaZk3R!"
sP_webui_password_confirmation="K3wLHaZk3R!"

tUnits_tools_packet_size="Byte"
