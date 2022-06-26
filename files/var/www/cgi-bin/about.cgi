#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="$t_about_0" %>
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
      <h5><%= $t_about_8 %></h4>
      <p class="mb-0"><%= $t_about_9 %></p>
    </div>
  </div>
</div>

<div class="row">
  <div class="col-lg-6">
    <h3><%= $t_about_1 %></h3>
    <dl>
      <dt><a href="https://github.com/OpenIPC/firmware">Firmware</a></dt>
      <dd><%= $t_about_2 %></dd>
      <dt><a href="https://github.com/OpenIPC/ipctool">IPC tool</a></dt>
      <dd><%= $t_about_3 %></dd>
      <dt><a href="https://github.com/OpenIPC/coupler">Coupler</a></dt>
      <dd><%= $t_about_4 %></dd>
      <dt><a href="https://github.com/OpenIPC/majestic">Majestic</a></dt>
      <dd><%= $t_about_5 %></dd>
      <dt><a href="https://github.com/OpenIPC/mini">Mini</a></dt>
      <dd><%= $t_about_6 %></dd>
      <dt><a href="https://github.com/OpenIPC/smolrtsp">SmolRTSP</a></dt>
      <dd><%= $t_about_7 %></dd>
    </dl>
  </div>
  <div class="col-lg-6">
    <h3><%= $t_about_d %></h3>
    <dl>
      <dt><a href="https://t.me/OpenIPC">OpenIPC (EN)</a></dt>
      <dd><%= $t_about_e %></dd>
      <dt><a href="https://t.me/openipc_modding">OpenIPC users (RU)</a></dt>
      <dd><%= $t_about_f %></dd>
      <dt><a href="https://t.me/openipc_software">OpenIPC development (RU)</a></dt>
      <dd><%= $t_about_g %></dd>
      <dt><a href="https://t.me/joinchat/YgHc5Bg4NOoxOTdi">Majestic Tests (RU)</a></dt>
      <dd><%= $t_about_h %></dd>
      <dt><a href="https://t.me/ExIPCam">ExIPCam users + repair</a></dt>
      <dd><%= $t_about_i %></dd>
      <dt><a href="https://t.me/openipc_demo">OpenIPC demo</a></dt>
      <dd><%= $t_about_j %></dd>
      <dt><a href="https://paywall.pw/openipc">OpenIPC paywall</a></dt>
      <dd><%= $t_about_k %></dd>
      <dt><a href="https://t.me/joinchat/T_GwQUBTJdfXJrFb">OpenIPC Iranian</a></dt>
      <dd><%= $t_about_l %></dd>
      <dt><a href="https://t.me/s/openipc_dev">OpenIPC dev</a></dt>
      <dd><%= $t_about_m %></dd>
    </dl>
  </div>
  <div class="col-12">
    <h3><%= $t_about_a %></h3>
    <p><%= $t_about_b %></p>
    <% row "$(team)" "row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-4 row-cols-xl-5 row-cols-xxl-6 g-4" %>
    <p><a href="https://github.com/orgs/OpenIPC/people"><%= $t_about_c %></a></p>
  </div>
</div>
<%in p/footer.cgi %>
