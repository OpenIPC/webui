#!/usr/bin/haserl
<%in p/common.cgi %>
<%
ipm_file="/usr/sbin/imp-control.sh"
[ ! -f "${ipm_file}" ] && redirect_to '/' "danger" $STR_NOT_SUPPORTED
page_title="IMP Control"
commands="aihpf aiagc ains aiaec aivol aigain flip contrast brightness saturation sharpness sinter
temper aecomp aeitmax dpc drc hilight again dgain hue ispmode flicker whitebalance sensorfps
backlightcomp defogstrength framerate gopattr setbitrate setgoplength setqp setqpbounds setqpipdelta
rcmode aemin autozoom frontcrop mask getosdattr getosdgrpattr getgamma getevattr getaeluma getawbct
getafmetrics gettotalgain getaeattr getimpversion getsysversion getcpuinfo getdeviceid getmodelfamily"
%>
<%in p/header.cgi %>
<% for i in $commands; do %>
<% ex "${ipm_file} $i" %>
<% done %>
<% ex "${ipm_file} help" %>
<%in p/footer.cgi %>
