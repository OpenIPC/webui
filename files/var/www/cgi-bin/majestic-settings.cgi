#!/usr/bin/haserl
<%in p/common.cgi %>
<%in _mj.cgi %>
<%
page_title="$t_mjsettings_0"
mj=$(echo "$mj" | sed "s/ /_/g")
only="$GET_tab"; [ -z "$only" ] && only="system"
eval title="\$tT_mj_${only}"; [ -z "$title" ] && title=$only

if [ "POST" = "$REQUEST_METHOD" ]; then
  mj_conf=/etc/majestic.yaml
  orig_yaml=/tmp/majestic.yaml.original
  temp_yaml=/tmp/majestic.yaml

  cp -f $mj_conf $temp_yaml

  IFS=$'\n' # make newlines the only separator
  for name in $(printenv|grep POST_); do
    key=".$(echo $name | sed 's/^POST_mj_//' | cut -d= -f1 | sed 's/_/./g')"
    value="$(echo $name | cut -d= -f2)"

    # validation and normalization
    [ "$key" = ".track" ] && continue
    [ "$key" = ".reset" ] && continue
    [ "$key" = ".netip.password.plain" ] && continue
    if [ "$key" = ".image.rotate" ]; then
      value="${value//°/}"
      [ "$value" = "0" ] && value="none"
    fi

    oldvalue=$(yaml-cli -g "$key" -i $temp_yaml)
    if [ -z "$value" ]; then
      [ -n "$oldvalue" ] && yaml-cli -d $key -i "$temp_yaml" -o "$temp_yaml"
    else
      [ "$oldvalue" != "$value" ] && yaml-cli -s $key "$value" -i "$temp_yaml" -o "$temp_yaml"
    fi
  done

  [ -n "$(diff -q $temp_yaml $mj_conf)" ] && cp -f $temp_yaml $mj_conf

  rm $temp_yaml

  killall -1 majestic

  redirect_to "$HTTP_REFERER"
fi
%>

<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-xxl-3 g-4">
  <div class="col">
    <h3><%= $title %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
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
      <p><input type="submit" class="btn btn-primary mt-3" value="Save changes"></p>
    </form>
  </div>
  <div class="col">
    <h3>Config excerpt</h3>
    <% pre "$config" %>
  </div>
  <div class="col">
    <h3>Config group</h3>
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
