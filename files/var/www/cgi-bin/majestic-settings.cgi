#!/usr/bin/haserl
<%in _common.cgi %>
<%in _mj.cgi %>
<%
page_title="$t_mjsettings_0"
only="$GET_group"
[ -z "$only" ] && only="system"
mj=$(echo "$mj" | sed "s/ /_/g")
%>
<%in _header.cgi %>
<nav class="navbar navbar-light bg-light mb-3 navbar-expand-xxl">
<div class="container-fluid">
<button aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbarSupportedContent" data-bs-toggle="collapse" type="button">
<span class="navbar-toggler-icon"></span>
</button>
<img alt="Image: Majestic logo" class="me-2" height="32" src="/a/majestic-logo.png" width="32">
<div class="collapse navbar-collapse" id="navbarSupportedContent">
<ul class="navbar-nav me-auto mb-2 mb-lg-0 navbar-nav-scroll" style="--bs-scroll-height: 15em;">
<%
for line in $mj; do
  param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}
  if [ "$olddomain" != "$domain" ]; then
    olddomain="$domain"; active=""; [ "$domain" == "$only" ] && active=" active"
    eval "title=\"\$tM_mj_$domain\""
    li "$(link_to "$title" "?group=${domain}" "nav-link${active}")" "nav-item small"
  fi
done
%>
</ul>
</div>
</div>
</nav>
<%
eval title="\$tT_mj_${only}"
[ -z "$title" ] && title=$only

h3 "$title" "my-4"

row_ "row-cols-1 row-cols-md-2 g-3 mb-3"
  col_card_ "$t_mjsettings_1"
    form_ "/cgi-bin/majestic-settings-update.cgi"
      mj=$(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only")
      config=""
      for line in $mj; do
        param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}; name=mj_${fullname//./_}; line=${line#*|}
        type=${line%%|*}; line=${line#*|}

        eval "$name=\"$(yaml-cli -g "$param")\""
        config="${config}\n${param}: $(yaml-cli -g "$param")"
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
            field_select "$name"
            ;;
          string)
            field_text "$name"
            ;;
          *)
            ;;
        esac
      done

      button_submit "$t_btn_submit" "primary"
    _form
  _col_card

  col_card_ "$t_mjsettings_2"
    pre "$(echo -e "$config")"
  _col_card
_row
%>

<script src="/a/majestic-settings.js"></script>
<script>
  if ($("#mj_isp_sensorConfig")) {
    const inp = $("#mj_isp_sensorConfig");
    const sel = document.createElement("select");
    sel.classList.add("form-select");
    sel.name=inp.name;
    sel.id=inp.id;
    sel.options.add(new Option());
    let opt;
    <% for i in $(ls -1 /etc/sensors/*.ini); do %>
      opt = new Option("<%= $i %>");
      opt.selected = ("<%= $i %>" == inp.value);
      sel.options.add(opt);
    <% done %>
    inp.replaceWith(sel);
  }
</script>
<%in p/footer.cgi %>
