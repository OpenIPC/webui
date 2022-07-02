#!/bin/sh

network_address=$(printenv | grep HTTP_HOST | cut -d= -f2 | cut -d: -f1)

tOptions_tools_action="ping,trace"
tOptions_web_version="master|Stable,dev|Development"

sP_mj_restore_file="majestic.yaml"
sP_tools_target="FQDN or IP address"
sP_socks5_port="1080"

tUnits_tools_packet_size="Byte"
