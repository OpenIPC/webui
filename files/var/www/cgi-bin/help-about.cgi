#!/usr/bin/haserl
<%in _common.cgi %>
<%
page_title="$tPageTitleAbout"

team() {
  ppl="$(grep -v ^# team.txt | sed "s/ /_/g" )"  
  for line in $ppl; do
    name=${line%%|*}; line=${line#*|}
    gh_photo=${line%%|*}; line=${line#*|}
    projects=${line%%|*}; line=${line#*|}
    gh_name=${line%%|*}; line=${line#*|}
    tg_name=${line%%|*}; line=${line#*|}
    person "$name" "$gh_photo" "$projects" "$gh_name" "$tg_name"
  done
}

person() {
  name="$1"
  gh_photo="$2"
  projects="$3"
  gh_name="$4"; [ -z "$gh_name" ] && gh_name="$1"
  tg_name="$5"; [ -z "$tg_name" ] && tg_name="$1"
  echo "<div class=\"col\"><div class=\"card h-100\">" \
    "<img src=\"https://avatars.githubusercontent.com/u/${gh_photo}\" alt=\"Image: ${name}\" class=\"card-img-top\">" \
    "<div class=\"card-body\">" \
    "<h5 class=\"card-title\">${name}</h5>" \
    "<p class=\"card-text\">${projects//_/ }</p>" \
    "<div class=\"social\">" \
    "<a href=\"https://github.com/${gh_name}/\"><img src=\"/img/github.svg\" alt=\"Image: GitHub\" class=\"img-fluid\" title=\"@${gh_name}\"></a>" \
    "<a href=\"https://t.me/${tg_name}\"><img src=\"/img/telegram.svg\" alt=\"Image: Telegram\" class=\"img-fluid\" title=\"@${tg_name}\"></a>" \
    "</div></div></div></div>"
}
%>
<%in _header.cgi %>

<h3>Projects</h3>
<p><a href="https://github.com/OpenIPC/firmware"><b>Firmware</b></a> is the Holy Grail of the community. Universal firmware for IP-cameras to replace proprietary, outdated and often insecure vendor pre-installed firmware.</p>
<p><a href="https://github.com/OpenIPC/ipctool"><b>IPC tool</b></a> is an IP-camera hardware inspector on steroids. This tool will not only identify your camera's processor, sensor, flash chip, but also help you with backing up the original firmware and more.</p>
<p><a href="https://github.com/OpenIPC/coupler"><b>Coupler</b></a> is a tool that allows you a smooth transition from the IP-camera manufacturer's pre-installed proprietary firmware to OpenIPC Firmware. No special skills are required.</p>
<p><a href="https://github.com/OpenIPC/majestic"><b>Majestic</b></a> is a universal IP-camera streamer. This project is the major part of the OpenIPC Firmware. Although it is not fully open source at this stage of development, we are considering opening up the codebase when the project matures enough and gets enough funding for open development.</p>
<p><a href="https://github.com/OpenIPC/mini"><b>Mini</b></a> is an open source IP-camera streamer. Think of it as Majestic's little brother.</p>
<p><a href="https://github.com/OpenIPC/smolrtsp"><b>SmolRTSP</b></a> is a simple RTSP 1.0 server library tailored for embedded devices, such as IP cameras. It supports both TCP and UDP, allows any payload format, and provides a convenient and flexible API.</p>

<div class="alert alert-warning mb-4">
<div class="row">
<div class="col-md-6 col-lg-7 col-xl-8 col-xxl-9">
<h4>Do you like what we do?</h4>
<p class="mb-md-0">Please consider <a href="https://opencollective.com/openipc">supporting our projects</a>.</p>
</div>
<div class="col-md-6 col-lg-5 col-xl-4 col-xxl-3">
<p><a href="https://opencollective.com/openipc"><img class="img-fluid" alt="Image: Donate to our collective" src="https://opencollective.com/webpack/donate/button@2x.png?color=blue"></a></p>
</div>
</div>
</div>

<h3>Team</h3>
<p>OpenIPC is a community-driven open source project, and <a href="https://github.com/orgs/OpenIPC/people">many people</a> contribute to its codebase. Koodos to them! There is also a core team of skilled developers who work hard to expand the list of supported hardware platforms, extend the functionality and stability of the firmware, review submitted code, and coordinate community efforts. Get to know the team and their areas of expertise:</p>

<div class="row row-cols-2 row-cols-sm-3 row-cols-lg-4 row-cols-xl-6 g-3 mb-3">
<% team %>
</div>

<%in _footer.cgi %>
