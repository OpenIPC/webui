#!/usr/bin/haserl
<%in _common.cgi %>
<%
get_soc_temp
page_title="$tPageTitleDeviceStatus"
%>
<%in _header.cgi %>
<%
row_
  col_card_ "$tHeaderDeviceInfo"
    b "$tHardware"
    pre_ "class=\"small\""
      print2c "${tSoC}:" "${soc}"
      print2c "${tSoCFamily}:" "${soc_family}"
      print2c "${tSensor}:" "${sensor_ini}"
      print2c "${tFlash}:" "${flash_size} MB"
      [ -n "$soc_temp" ] && print2c "${tSoCTemp}:" "${soc_temp}°C"
    _pre

    b "$tFirmware"
    pre_ "class=\"small\""
      print2c "${tVersion}:" "${fw_version}-${fw_variant}"
      print2c "${tBuild}:" "${fw_build}"
    _pre

    b "$tSystem"
    pre_ "class=\"small mb-0\""
      print2c "${tHostname}:" "${hostname}"
      print2c "${tWanMac}:" "${wan_mac}"
    _pre
  _col_card

  col_card_ "$tHeaderSystemInfo"
    ex "/bin/date"
    div_ "class=\"small mb-3\""
      link_to "$tEditTimezone" "/cgi-bin/network-ntp.cgi"
      link_to "$tSyncTime" "/cgi-bin/ntp-update.cgi"
    _div
    ex "/usr/bin/uptime"
    ex "cat /proc/meminfo | grep Mem"
  _col_card

  col_card_ "$tHeaderResources"
    ex "df -T"
  _col_card
_row

row_
  col_card_ "$tHeaderTopProcesses"
    ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20"
  _col_card
_row
%>
<%in _footer.cgi %>
