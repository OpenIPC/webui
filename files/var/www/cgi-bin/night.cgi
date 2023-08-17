#!/usr/bin/haserl
<%in p/common.cgi %>
<%
case "$POST_mode" in
  on)
    test "no" == "$POST_bw" && \
    echo 1 > /sys/class/gpio/gpio$(cli -g .nightMode.backlightPin)/value || \
    curl -s http://127.0.0.1/night/on
    ;;
  off)
    test "no" == "$POST_bw" && \
    echo 0 > /sys/class/gpio/gpio$(cli -g .nightMode.backlightPin)/value || \
    curl -s http://127.0.0.1/night/off
    ;;
  toggle)
    curl -s http://127.0.0.1/night/toggle
    ;;
  *)
    ;;
esac
header_ok
%>
