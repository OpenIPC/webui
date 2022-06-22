#!/usr/bin/haserl
<%in _common.cgi %>
<%in _mj.cgi %>
<%
page_title="$t_mjsettings_0"
mj=$(echo "$mj" | sed "s/ /_/g")
only="$GET_tab"; [ -z "$only" ] && only="system"
eval title="\$tT_mj_${only}"; [ -z "$title" ] && title=$only
%>
<%in _header.cgi %>
<div class="row row-cols-3 g-5">
<div class="col">
<div class="list-group list-group-flush" id="mj-tabs">
<%
for _l in $mj; do
  _p=${_l%%|*}; fullname=${_p#.}; _d=${fullname%.*}
  if [ "$_od" != "$_d" ]; then
    _od="$_d"
    _c="class=\"list-group-item\""; [ "$_d" = "$only" ] && _c=" class=\"list-group-item active\" aria-current=\"true\""
    echo "<a $_c href=\"?tab=${_d}\">$(eval echo \$tT_mj_${_d})</a>"
  fi
done
unset _c; unset _d; unset _l; unset _od; unset _p;
%>
</div>
</div>
<form action="/cgi-bin/majestic-settings-update.cgi" method="post">
<div class="col">
<h5><%= $title %></h5>
<%
config=""
for line in $(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only"); do
  param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}; name=mj_${fullname//./_}; line=${line#*|}; type=${line%%|*}; line=${line#*|}
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
      echo "UNKNOWN FIELD: $name"
      ;;
  esac
done
%>
<button type="submit" class="btn btn-primary mt-3" ><%= $t_btn_submit %></button>
</form>
</div>
<div class="col">
<h6><%= $t_mjsettings_2 %>
<% pre "$(echo -e "$config")" %>
</div>
</div>

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
