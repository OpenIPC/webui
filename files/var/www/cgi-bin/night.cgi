#!/usr/bin/haserl
<%in p/common.cgi %>
<%
case "$POST_mode" in
  on)
    curl -s http://127.0.0.1/night/on
    ;;
  off)
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
