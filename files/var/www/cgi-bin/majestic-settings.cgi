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
<img src="/img/majestic-logo.png" alt="Image: Majestic Logo" width="32" height="32" class="me-2">

<%
div_ "class=\"collapse navbar-collapse\" id=\"navbarSupportedContent\""
  ul_ "class=\"navbar-nav me-auto mb-2 mb-lg-0 navbar-nav-scroll\" style=\"--bs-scroll-height: 15em;\""
    for line in $mj; do
      param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}
      if [ "$olddomain" != "$domain" ]; then
        olddomain="$domain"; active=""; [ "$domain" == "$only" ] && active=" active"
        eval "title=\"\$tMjNav_$domain\""
        li "$(link_to "$title" "?group=${domain}" "class=\"nav-link${active}\"")" "class=\"nav-item small\""
      fi
    done
  _ul
_div
%>
</div>
</nav>
<%
eval title="\$tMjTitle_${only}"
[ -z "$title" ] && title=$only

h3 "$title" "class=\"my-4\""

form_ "/cgi-bin/majestic-settings-update.cgi" "post"
mj=$(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only")
for line in $mj; do
  param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}; name=mj_${fullname//./_}; line=${line#*|}
  units=${line%%|*}; line=${line#*|}
  type=${line%%|*}; line=${line#*|}
  options=${line%%|*}; line=${line#*|}
  placeholder=${line%%|*}; line=${line#*|}

  fullname=${fullname//./_}
  fullname=${fullname//-/_}

  # eval label="\$tLabel_${fullname}"
  # eval hint="\$tHint_${fullname}"

  # assign value to variable with the name
  eval $name="$(yaml-cli -g "$param")"

  case "$type" in
    boolean)
      field_switch "$name"
      ;;
    hidden)
      field_hidden "$name"
      ;;
    number)
      field_number "$name"
      ;;
    range)
      field_range "$name"
      ;;
    select)
      eval "${name}_options=\"${options//,/ }\""
      eval "${name}=\"${placeholder}\""
      field_select "$name"
      ;;
    string)
      field_text "$name"
      ;;
    *)
      ;;
  esac
done
button_submit
_form
%>

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
