#!/usr/bin/haserl
<%in _common.cgi %>
<%in _mj.cgi %>
<%
get_system_info
page_title="$tPageTitleMajesticSettings"
only="$GET_group"
[ -z "$only" ] && only="system"
mj=$(echo "$mj" | sed "s/ /_/g")
%>
<%in _header.cgi %>
<nav class="navbar navbar-expand-md navbar-light bg-light mb-3">
<div class="container-fluid">
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
  aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
<img src="/img/majestic-logo.png" alt="Image: Majestic Logo" width="32" height="32">
<div class="collapse navbar-collapse" id="navbarSupportedContent">
<ul class="navbar-nav me-auto mb-2 mb-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 15em;">
<%
for line in $mj; do
  param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}
  if [ "$olddomain" != "$domain" ]; then
    olddomain="$domain"; active=""; [ "$domain" == "$only" ] && active=" active"
    eval title="\$tMjNav_$domain"
    echo "<li class=\"nav-item small\"><a class=\"nav-link${active}\" href="?group=${domain}">${title}</a></li>"
  fi
done
%>
</ul>
</div>
</div>
</nav>
<%
eval title="\$tMjTitle_${only}"
[ -z "$title" ] && title=$only
%>
<h3 class="my-4"><%= $title %></h3>
<form action="/cgi-bin/majestic-settings-update.cgi" method="post">
<%
mj=$(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only")
for line in $mj; do
  param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}; name=${fullname//./-}; line=${line#*|}
  units=${line%%|*}; line=${line#*|}
  type=${line%%|*}; line=${line#*|}
  options=${line%%|*}; line=${line#*|}
  placeholder=${line%%|*}; line=${line#*|}
  value=$(yaml-cli -g "$param")
  fullname=${fullname//./_}
  fullname=${fullname//-/_}
  eval label="\$tMjLabel_${fullname}"
  eval hint="\$tMjHint_${fullname}"
  echo -n -e "<div class=\"row ${type}\">"
  case "$type" in
    boolean)
      [ "true" = "$value" ] && checked=" checked" || checked=""
      echo -n -e \
        "<label class=\"col-md-5 col-form-label form-check-label\" for=\"${name}\">${label//_/ }</label>" \
        "<div class=\"col-md-7\">" \
        "<div class=\"form-check form-switch\">" \
        "<input type=\"hidden\" name=\"${name}\" id=\"${name}-false\" value=\"false\">" \
        "<input class=\"form-check-input\" name=\"${name}\" id=\"${name}\" type=\"checkbox\"${checked} role=\"switch\" value=\"true\">" \
        "</div>"
      [ -n "$hint" ] && echo -n -e "  <p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n -e "</div>"
      ;;
    hidden)
      echo -n -e "<input type=\"hidden\" name=\"${name}\" id=\"${name}\" value=\"${value}\">"
      ;;
    number)
      echo -n -e \
        "<label class=\"col-md-5 col-form-label\" for=\"${name}\">${label//_/ }</label>" \
        "<div class=\"col-md-7\">" \
        "<div class=\"input-group\">" \
        "<input class=\"form-control text-end\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ -n "$units" ] && echo -n -e "<span class=\"input-group-text\">${units}</span>"
      echo -n -e "</div>"
      [ -n "$hint" ] && echo -n -e "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n -e "</div>"
      ;;
    range)
      echo -n -e \
        "<label class=\"col-md-5 col-form-label\" for=\"${name}\">${label//_/ }</label>" \
        "<div class=\"col-md-7\">" \
        "<div class=\"input-group\">"
      if [ ! -z $(echo "${options}" | grep -E auto) ]; then
        [ "auto" = "$value" ] && checked=" checked" || checked=""
        echo -n -e \
          "<span class=\"input-group-text\">" \
          "<label><input class=\"form-check-input auto-value\" type=\"checkbox\" data-for=\"${name}\" data-value=\"${default}\"${checked}> auto</label>" \
          "</span>"
      fi
      [ "auto" = "$value" ] && readonly=" readonly" || readonly=""
      echo -n -e "<input class=\"form-control text-end range\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" data-units=\"${units}\"${readonly}>"
      [ -n "$units" ] && echo -n -e "<span class=\"input-group-text\">${units}</span>"
      echo -n -e "</div>"
      [ -n "$hint" ] && echo -n -e "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n -e "</div>"
      ;;
    select)
      echo -n -e \
        "<label class=\"col-md-5 col-form-label\" for=\"${name}\">${label//_/ }</label>" \
        "<div class=\"col-md-7\">" \
        "<div class=\"input-group\">" \
        "<select class=\"form-select\" name=\"${name}\" id=\"${name}\">"
      [ -z "$value" ] && echo -n -e "<option value=\"\"></option>"
      for o in ${options//,/ }; do
        [ "$o" = "$value" ] && selected=" selected" || selected=""
        echo -n -e "<option${selected}>${o}</option>"
      done
      echo -n -e "</select>"
      [ -n "$units" ] && echo -n -e "<span class=\"input-group-text\">${units}</span>"
      echo -n -e "</div>"
      [ -n "$hint" ] && echo -n -e "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n -e "</div>"
      ;;
    string)
      [ "$name" != "isp-sensorConfig" ] && placeholder=${placeholder//_/ }
      echo -n -e \
        "<label class=\"col-md-5 col-form-label\" for=\"${name}\">${label//_/ }</label>" \
        "<div class=\"col-md-7\">" \
        "<div class=\"input-group\">" \
        "<input class=\"form-control\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ -n "$units" ] && echo -n -e "<span class=\"input-group-text\">${units}</span>"
      echo -n -e "</div>"
      [ -n "$hint" ] && echo -n -e "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n -e "</div>"
      ;;
    *)
      ;;
  esac
  echo -n -e "</div>\n\n"
done
%>
<button type="submit" class="btn btn-primary my-4"><%= $tButtonFormSubmit %></button>
</form>
<script src="/js/majestic-settings.js"></script>
<script>
  if (screen.width > 767) $$('.col-form-label').forEach(el => el.classList.add("border-bottom"));
  if ($('#isp-sensorConfig')) {
    const inp = $('#isp-sensorConfig');
    const sel = document.createElement('select');
    sel.classList.add('form-select');
    sel.name=inp.name;
    sel.id=inp.id;
    sel.options.add(new Option());
    let opt;
    <% for i in $(ls -1 /etc/sensors/*.ini); do %>
      opt = new Option('<%= $i %>');
      opt.selected = ('<%= $i %>' == inp.value);
      sel.options.add(opt);
    <% done %>
    inp.replaceWith(sel);
  }
</script>
<%in _footer.cgi %>
