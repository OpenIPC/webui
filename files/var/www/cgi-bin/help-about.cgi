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
  col_first
    div_ "class=\"card h-100\""
      image "https://avatars.githubusercontent.com/u/${2}" "title=\"${1}\" class=\"card-img-top\""
      div_ "class=\"card-body\""
        h5 "${1}" "class=\"card-title\""
        p "${3//_/ }" "class=\"card-text small\""
        div_ "class=\"social\""
          link_to "$(image "/img/github.svg" "class=\"img-fluid\" title=\"@${4}\"")" "https://github.com/${4}/"
          link_to "$(image "/img/telegram.svg" "class=\"img-fluid\" title=\"@${5}\"")" "https://t.me/${5}"
        _div
      _div
    _div
  col_last
}
%>
<%in _header.cgi %>
<%
row_
  col_ "col-xl-5 col-xxl-6"
    h3 "Projects"
    dl_
      dt "$(link_to "Firmware" "https://github.com/OpenIPC/firmware")"
      dd "The Holy Grail of the community. Universal firmware for IP-cameras to replace proprietary, outdated and often insecure vendor pre-installed firmware."
      dt "$(link_to "IPC tool" "https://github.com/OpenIPC/ipctool")"
      dd "An IP-camera hardware inspector on steroids. This tool will not only identify your camera's processor, sensor, flash chip, but also help you with backing up the original firmware and more."
      dt "$(link_to "Coupler" "https://github.com/OpenIPC/coupler")"
      dd "A tool that allows you a smooth transition from the IP-camera manufacturer's pre-installed proprietary firmware to OpenIPC Firmware. No special skills are required."
      dt "$(link_to "Majestic" "https://github.com/OpenIPC/majestic")"
      dd "A universal IP-camera streamer. This project is the major part of the OpenIPC Firmware. Although it is not fully open source at this stage of development, we are considering opening up the codebase when the project matures enough and gets enough funding for open development."
      dt "$(link_to "Mini" "https://github.com/OpenIPC/mini")"
      dd "An open source IP-camera streamer. Think of it as Majestic's little brother."
      dt "$(link_to "SmolRTSP" "https://github.com/OpenIPC/smolrtsp")"
      dd "A simple RTSP 1.0 server library tailored for embedded devices, such as IP cameras. It supports both TCP and UDP, allows any payload format, and provides a convenient and flexible API."
    _dl
    alert_ "warning"
      row_
        col_ "col-md-6 col-lg-7 col-xl-12 col-xxl-6 mb-3 mb-md-0 mb-xl-3"
          h4 "Do you like what we do?"
          p "Please consider <a href=\"https://opencollective.com/openipc\">supporting our projects</a>." "class=\"mb-0\""
        _col
        col_ "col-md-6 col-lg-5 col-xl-12 col-xxl-5"
          p "$(link_to "$(image "https://opencollective.com/webpack/donate/button@2x.png?color=blue" "class=\"img-fluid\" alt=\"Image: Donate to our collective\"")" "https://opencollective.com/openipc")" "class=\"mb-0\""
        _col
      _row
    _alert
  _col
  col_ "col-xl-7 col-xxl-6"
    h3 "Team"
    p "OpenIPC is a community-driven open source project, and $(link_to "many people" "https://github.com/orgs/OpenIPC/people") contribute to its codebase. Koodos to them! There is also a core team of skilled developers who work hard to expand the list of supported hardware platforms, extend the functionality and stability of the firmware, review submitted code, and coordinate community efforts. Get to know the team and their areas of expertise:"
    row "$(team)" "row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-5 row-cols-xl-4 row-cols-xxl-4 g-3 mb-3"
  _col
_row
%>
<%in _footer.cgi %>
