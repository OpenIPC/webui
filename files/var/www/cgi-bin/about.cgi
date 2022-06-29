#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="About OpenIPC" %>
<%in p/header.cgi %>
<%
TEAM="# OpenIPC Team members in following format: Username | GitHub PhotoID | Projects | GitHub name | Telegram name
FlyRouter|88846|Project Coordination|ZigFisher|FlyRouter
widgetii|6576495|Majestic Streamer, IPCtool|widgetii|widgetii
dimerrr|106577375|U-Boot, Kernels, Coupler, IPCtool|dimerrr|dimerrr
John|21039610|Linux|p0i5k|p0i5k
Hirrolot|40539574|SmolRTSP|Hirrolot|hirrolot
cronyx|2557102|Linux|cronyx|cronyx
themactep|37488|Web UI|themactep|themactep
"
team() {
  _pp="$(echo "$TEAM"|grep -v ^#|sed "s/ /_/g")"
  for _p in $_pp; do
    _n=${_p%%|*}; _p=${_p#*|}
    _a=${_p%%|*}; _p=${_p#*|}
    _b=${_p%%|*}; _p=${_p#*|}
    _c=${_p%%|*}; _p=${_p#*|}
    _d=${_p%%|*}; _p=${_p#*|}
%>
<%in p/person.cgi %>
<%
  done
  unset _a; unset _b; unset _c; unset _d; unset _n; unset _p; unset _pp
}
%>
<div class="alert alert-primary">
  <div class="row">
    <div class="col-md-6 text-end">
      <p class="mb-0">
        <a href="https://opencollective.com/openipc"><img class="img-fluid" src="https://opencollective.com/webpack/donate/button.png?color=blue" alt="Image: OpenCollective donation button" title="Donate to our collective"></a>
      </p>
    </div>
    <div class="col-md-6">
      <h5>Do you like what we do?</h4>
      <p class="mb-0">Please consider supporting our projects.</p>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-lg-6">
    <h3>Projects</h3>
    <dl>
      <dt><a href="https://github.com/OpenIPC/firmware">Firmware</a></dt>
      <dd>The Holy Grail of the community. Universal firmware for IP-cameras to replace proprietary, outdated and often insecure vendor pre-installed firmware.</dd>
      <dt><a href="https://github.com/OpenIPC/ipctool">IPC tool</a></dt>
      <dd>An IP-camera hardware inspector on steroids. This tool will not only identify your camera's processor, sensor, flash chip, but also help you with backing up the original firmware and more.</dd>
      <dt><a href="https://github.com/OpenIPC/coupler">Coupler</a></dt>
      <dd>A tool that allows you a smooth transition from the IP-camera manufacturer's pre-installed proprietary firmware to OpenIPC Firmware. No special skills are required.</dd>
      <dt><a href="https://github.com/OpenIPC/majestic">Majestic</a></dt>
      <dd>A universal IP-camera streamer. This project is the major part of the OpenIPC Firmware. Although it is not fully open source at this stage of development, we are considering opening up the codebase when the project matures enough and gets enough funding for open development.</dd>
      <dt><a href="https://github.com/OpenIPC/mini">Mini</a></dt>
      <dd>An open source IP-camera streamer. Think of it as Majestic's little brother.</dd>
      <dt><a href="https://github.com/OpenIPC/smolrtsp">SmolRTSP</a></dt>
      <dd>A simple RTSP 1.0 server library tailored for embedded devices, such as IP cameras. It supports both TCP and UDP, allows any payload format, and provides a convenient and flexible API.</dd>
    </dl>
  </div>
  <div class="col-lg-6">
    <h3>Telegram Channels</h3>
    <dl>
      <dt><a href="https://t.me/OpenIPC">OpenIPC (EN)</a></dt>
      <dd>International channel about OpenIPC. (English)</dd>
      <dt><a href="https://t.me/openipc_modding">OpenIPC users (RU)</a></dt>
      <dd>Channel about OpenIPC for Russian-speaking users. (Russian)</dd>
      <dt><a href="https://t.me/openipc_software">OpenIPC development (RU)</a></dt>
      <dd>Channel for OpenIPC developers. (Mostly Russian)</dd>
      <dt><a href="https://t.me/joinchat/YgHc5Bg4NOoxOTdi">Majestic Tests (RU)</a></dt>
      <dd>Telegram group for Majestic streamer testers. (Mostly Russian)</dd>
      <dt><a href="https://t.me/ExIPCam">ExIPCam users + repair</a></dt>
      <dd>Discussion of the ExIPCam program and hardware/software repairing devices. (Russian)</dd>
      <dt><a href="https://t.me/openipc_demo">OpenIPC demo</a></dt>
      <dd>Experimental Telegram Bot. (After connecting, send "/menu")</dd>
      <dt><a href="https://paywall.pw/openipc">OpenIPC paywall</a></dt>
      <dd>Paid technical support group.</dd>
      <dt><a href="https://t.me/joinchat/T_GwQUBTJdfXJrFb">OpenIPC Iranian</a></dt>
      <dd>تیم OpenIPC برای کاربران ایرانی (Telegram group for Iranian OpenIPC users). (Persian)</dd>
      <dt><a href="https://t.me/s/openipc_dev">OpenIPC dev</a></dt>
      <dd>GitHub notifications on the latest Firmware & Software.</dd>
    </dl>
  </div>
  <div class="col-12">
    <h3>Team</h3>
    <p>OpenIPC is a community-driven open source project, and many people contribute to its codebase. Koodos to them! There is also a core team of skilled developers who work hard to expand the list of supported hardware platforms, extend the functionality and stability of the firmware, review submitted code, and coordinate community efforts. Get to know the team and their areas of expertise:</p>
    <div class="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-4 row-cols-xl-5 row-cols-xxl-6 g-4">
      <% team %>
    </div>
    <p><a href="https://github.com/orgs/OpenIPC/people" class="btn btn-secondary">List of contributors</a></p>
  </div>
</div>
<%in p/footer.cgi %>
