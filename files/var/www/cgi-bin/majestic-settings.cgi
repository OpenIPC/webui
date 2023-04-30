#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Majestic settings"
mj=$(echo "$mj" | sed "s/ /_/g")
only="$GET_tab"; [ -z "$only" ] && only="system"
eval title="\$tT_mj_${only}"

# hide certain domains if not supported
if [ -n "$(eval echo "\$mj_hide_${only}" | sed -n "/\b${soc_family}\b/p")" ]; then
  redirect_to "majestic-settings.cgi" "danger" "$title is not supported on your system."
fi

if [ "POST" = "$REQUEST_METHOD" ]; then
  mj_conf=/etc/majestic.yaml
  temp_yaml=/tmp/majestic.yaml

  # make a copy of the actual config into memory
  cp -f $mj_conf $temp_yaml

  OIFS=$IFS
  IFS=$'\n' # make newlines the only separator
  for yaml_param_name in $(printenv|grep POST_); do
    form_field_name=$(echo $yaml_param_name | sed 's/^POST_mj_//')
    key=".$(echo $form_field_name | cut -d= -f1 | sed 's/_/./g')"

    # do not include helping fields into config
    if [ "$key" = ".netip.password.plain" ] || [ "$key" = ".osd.corner" ]; then
      continue
    fi

    value="$(echo $form_field_name | cut -d= -f2)"

    # normalization
    # (that's why we can't have nice things)
    case "$key" in
      .image.rotate)
        [ "0" = "$value" ] && value="none"
        ;;
      .isp.antiFlicker)
        [ "50Hz" = "$value" ] && value="50"
        [ "60Hz" = "$value" ] && value="60"
        ;;
      .motionDetect.visualize)
        [ "true" = "$value" ] && yaml-cli -s ".osd.enabled" "true" -i $temp_yaml
        ;;
      .osd.enabled)
        [ "false" = "$value" ] && yaml-cli -s ".motionDetect.visualize" "false" -i $temp_yaml
        ;;
      .system.webAdmin)
        [ "true" = "$value" ] && value="enabled"
        [ "false" = "$value" ] && value="disabled"
        ;;
    esac

    # read existing value
    oldvalue=$(yaml-cli -g "$key" -i $temp_yaml)

    if [ -z "$value" ]; then
      # if no new value submitted but there is an existing value, delete the yaml_param_name
      [ -n "$oldvalue" ] && yaml-cli -d $key -i "$temp_yaml" -o "$temp_yaml"
    else
      # if new value is submitted and it differs from the existing one, update the yaml_param_name
      [ "$oldvalue" != "$value" ] && yaml-cli -s $key "$value" -i "$temp_yaml" -o "$temp_yaml"
    fi
  done
  IFS=$OIFS

  # update config if differs
  [ -n "$(diff -q $temp_yaml $mj_conf)" ] && cp -f $temp_yaml $mj_conf

  # clean up
  rm $temp_yaml

  # reload majestic
  killall -1 majestic

  redirect_to "$HTTP_REFERER"
fi
%>
<%in p/header.cgi %>

<ul class="nav bg-light small mb-4 d-none d-lg-flex">
<%
mj=$(echo "$mj" | sed "s/ /_/g")
for _line in $mj; do
  _parameter=${_line%%|*};
  _param_name=${_parameter#.};
  _param_domain=${_param_name%.*}
  if [ "$_parameter_domain_old" != "$_param_domain" ]; then
    # hide certain domains for certain familier
    [ -n "$(eval echo "\$mj_hide_${_param_domain}" | sed -n "/\b${soc_family}\b/p")" ] && continue
    # show certain domains only for certain vendors
    [ -n "$(eval echo "\$mj_show_${_param_domain}_vendor")" ] && [ -z "$(eval echo "\$mj_show_${_param_domain}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
    _parameter_domain_old="$_param_domain"
    _css="class=\"nav-link\""; [ "$_param_domain" = "$only" ] && _css="class=\"nav-link active\" aria-current=\"true\""
    echo "<li class=\"nav-item\"><a ${_css} href=\"majestic-settings.cgi?tab=${_param_domain}\">$(eval echo \$tT_mj_${_param_domain})</a></li>"
  fi
done
unset _css; unset _param_domain; unset _line; unset _param_name; unset _parameter_domain_old; unset _parameter;
%>
</ul>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3><%= $title %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
config=""
_mj2="$(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only")"
for line in $_mj2; do
                                    # line: .isp.exposure|Sensor_exposure_time|&micro;s|range|auto,1-500000|auto|From_1_to_500000.
  yaml_param_name=${line%%|*}       # => .isp.exposure
  _param_name=${yaml_param_name#.}  # => isp.exposure
  _param_name=${_param_name//./_}   # => isp_exposure
  _param_name=${_param_name//-/_}   # => isp_exposure
  domain=${_param_name%%_*}         # => isp

  # hide certain domains if blacklisted
  [ -n "$(eval echo "\$mj_hide_${domain}" | sed -n "/\b${soc_family}\b/p")" ] && continue
  # hide certain parameters if blacklisted
  [ -n "$(eval echo "\$mj_hide_${_param_name}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
  [ -n "$(eval echo "\$mj_hide_${_param_name}" | sed -n "/\b${soc_family}\b/p")" ] && continue
  # show certain domains only if whitelisted
  [ -n "$(eval echo "\$mj_show_${domain}_vendor")" ] && [ -z "$(eval echo "\$mj_show_${domain}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
  # show certain parameters only if whitelisted
  [ -n "$(eval echo "\$mj_show_${_param_name}")" ] && [ -z "$(eval echo "\$mj_show_${_param_name}" | sed -n "/\b${soc_family}\b/p")" ] && continue
  [ -n "$(eval echo "\$mj_show_${_param_name}_vendor")" ] && [ -z "$(eval echo "\$mj_show_${_param_name}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
  # show certain parameters only in debug mode
  [ -n "$(echo "$mj_hide_unless_debug" | sed -n "/\b${_param_name}\b/p")" ] && [ "0$debug" -lt "1" ] && continue

  form_field_name=mj_${_param_name} # => mj_isp_exposure
  line=${line#*|}                   # line: Sensor_exposure_time|&micro;s|range|auto,1-500000|auto|From_1_to_500000.
  label_text=${line%%|*}            # => Sensor_exposure_time
  label_text=${label_text//_/ }     # => Sensor exposure time
  line=${line#*|}                   # line: &micro;s|range|auto,1-500000|auto|From_1_to_500000.
  units=${line%%|*}                 # => &micro;s
  line=${line#*|}                   # line: range|auto,1-500000|auto|From_1_to_500000.
  form_field_type=${line%%|*}       # => range
  line=${line#*|}                   # line: auto,1-500000|auto|From_1_to_500000.
  options=${line%%|*}               # => auto,1-500000
  line=${line#*|}                   # line: auto|From_1_to_500000.
  placeholder=${line%%|*}           # => auto
  line=${line#*|}                   # line: From_1_to_500000.
  hint=$line                        # => From_1_to_500000.
  hint=${hint//_/ }                 # => From 1 to 500000.

  value="$(yaml-cli -g "$yaml_param_name")"
# FIXME: this is not how it should be done. Instead, Majestic should be reporting its true values.
# [ -z "$value" ] && value="$placeholder"

  # assign yaml_param_name's value to a variable with yaml_param_name's form_field_name for form fields values
  eval "$form_field_name=\"\$value\""

  # hide some params in config
  if [ "mj_netip_password_plain" != "$form_field_name" ]; then
    config="${config}\n$(eval echo ${yaml_param_name}: \"\$$form_field_name\")"
  fi

  case "$form_field_type" in
    boolean)  field_switch   "$form_field_name" "$label_text" "$hint" "$options";;
    hidden)   field_hidden   "$form_field_name" "$label_text" "$hint";;
    number)   field_number   "$form_field_name" "$label_text" "$options" "$hint";;
    password) field_password "$form_field_name" "$label_text" "$hint";;
    range)    field_range    "$form_field_name" "$label_text" "$options" "$hint";;
    select)   field_select   "$form_field_name" "$label_text" "$options" "$hint";;
    string)   field_text     "$form_field_name" "$label_text" "$hint" "$placeholder";;
    *) echo "<span class=\"text-danger\">UNKNOWN FIELD TYPE ${form_field_type} FOR ${_name} WITH LABEL ${label_text}</span>";;
  esac
done
%>
      <% button_submit %>
    </form>
  </div>
  <div class="col">
    <h3>Related settings</h3>
    <pre><% echo -e "$config" %></pre>
  </div>
  <div class="col">
    <h3>Quick Links</h3>
    <p><a href="info-majestic.cgi">Majestic Config File (majestic.yaml)</a></p>
    <p><a href="majestic-endpoints.cgi">Majestic Endpoints</a></p>
  </div>
</div>

<script>
  let MD5 = function(d){return V(Y(X(d),8*d.length))};
  function X(d){for(var _=Array(d.length>>2),m=0;m<_.length;m++)_[m]=0;for(m=0;m<8*d.length;m+=8)_[m>>5]|=(255&d.charCodeAt(m/8))<<m%32;return _}
  function V(d){for(var _="",m=0;m<32*d.length;m+=8)_+=String.fromCharCode(d[m>>5]>>>m%32&255);return _}
  function Y(d,_){d[_>>5]|=128<<_%32,d[14+(_+64>>>9<<4)]=_;for(var m=1732584193,f=-271733879,r=-1732584194,i=271733878,n=0;n<d.length;n+=16){var h=m,t=f,g=r,e=i;f=md5_ii(f=md5_ii(f=md5_ii(f=md5_ii(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_hh(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_gg(f=md5_ff(f=md5_ff(f=md5_ff(f=md5_ff(f,r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+0],7,-680876936),f,r,d[n+1],12,-389564586),m,f,d[n+2],17,606105819),i,m,d[n+3],22,-1044525330),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+4],7,-176418897),f,r,d[n+5],12,1200080426),m,f,d[n+6],17,-1473231341),i,m,d[n+7],22,-45705983),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+8],7,1770035416),f,r,d[n+9],12,-1958414417),m,f,d[n+10],17,-42063),i,m,d[n+11],22,-1990404162),r=md5_ff(r,i=md5_ff(i,m=md5_ff(m,f,r,i,d[n+12],7,1804603682),f,r,d[n+13],12,-40341101),m,f,d[n+14],17,-1502002290),i,m,d[n+15],22,1236535329),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+1],5,-165796510),f,r,d[n+6],9,-1069501632),m,f,d[n+11],14,643717713),i,m,d[n+0],20,-373897302),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+5],5,-701558691),f,r,d[n+10],9,38016083),m,f,d[n+15],14,-660478335),i,m,d[n+4],20,-405537848),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+9],5,568446438),f,r,d[n+14],9,-1019803690),m,f,d[n+3],14,-187363961),i,m,d[n+8],20,1163531501),r=md5_gg(r,i=md5_gg(i,m=md5_gg(m,f,r,i,d[n+13],5,-1444681467),f,r,d[n+2],9,-51403784),m,f,d[n+7],14,1735328473),i,m,d[n+12],20,-1926607734),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+5],4,-378558),f,r,d[n+8],11,-2022574463),m,f,d[n+11],16,1839030562),i,m,d[n+14],23,-35309556),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+1],4,-1530992060),f,r,d[n+4],11,1272893353),m,f,d[n+7],16,-155497632),i,m,d[n+10],23,-1094730640),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+13],4,681279174),f,r,d[n+0],11,-358537222),m,f,d[n+3],16,-722521979),i,m,d[n+6],23,76029189),r=md5_hh(r,i=md5_hh(i,m=md5_hh(m,f,r,i,d[n+9],4,-640364487),f,r,d[n+12],11,-421815835),m,f,d[n+15],16,530742520),i,m,d[n+2],23,-995338651),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+0],6,-198630844),f,r,d[n+7],10,1126891415),m,f,d[n+14],15,-1416354905),i,m,d[n+5],21,-57434055),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+12],6,1700485571),f,r,d[n+3],10,-1894986606),m,f,d[n+10],15,-1051523),i,m,d[n+1],21,-2054922799),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+8],6,1873313359),f,r,d[n+15],10,-30611744),m,f,d[n+6],15,-1560198380),i,m,d[n+13],21,1309151649),r=md5_ii(r,i=md5_ii(i,m=md5_ii(m,f,r,i,d[n+4],6,-145523070),f,r,d[n+11],10,-1120210379),m,f,d[n+2],15,718787259),i,m,d[n+9],21,-343485551),m=safe_add(m,h),f=safe_add(f,t),r=safe_add(r,g),i=safe_add(i,e)}return Array(m,f,r,i)}
  function md5_cmn(d,_,m,f,r,i){return safe_add(bit_rol(safe_add(safe_add(_,d),safe_add(f,i)),r),m)}
  function md5_ff(d,_,m,f,r,i,n){return md5_cmn(_&m|~_&f,d,_,r,i,n)}
  function md5_gg(d,_,m,f,r,i,n){return md5_cmn(_&f|m&~f,d,_,r,i,n)}
  function md5_hh(d,_,m,f,r,i,n){return md5_cmn(_^m^f,d,_,r,i,n)}
  function md5_ii(d,_,m,f,r,i,n){return md5_cmn(m^(_|~f),d,_,r,i,n)}
  function safe_add(d,_){var m=(65535&d)+(65535&_);return(d>>16)+(_>>16)+(m>>16)<<16|65535&m}
  function bit_rol(d,_){return d<<_|d>>>32-_}
  function ord(str){return str.charCodeAt(0)}
  function chr(n){return String.fromCharCode(n)}

  function generateSofiaHash(text) {
    let h = "";
    let md5 = MD5(text);
    for (let i = 0; i <= 7; i++) {
      let n = (ord(md5[2*i]) + ord(md5[2*i+1])) % 62;
      n += (n > 9) ? (n > 35) ? 61 : 55 : 48;
      h += chr(n);
    }
    return h;
  }

<% if [ -d /etc/sensors/ ]; then %>
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
<% fi %>

  $("#mj_osd_corner")?.addEventListener("change", (ev) => {
    const padding = 16;
    switch (ev.target.value) {
      case "bl":
        $("#mj_osd_posX").value = padding;
        $("#mj_osd_posY").value = -(padding);
        break;
      case "br":
        $("#mj_osd_posX").value = -(padding);
        $("#mj_osd_posY").value = -(padding);
        break;
      case "tl":
        $("#mj_osd_posX").value = padding;
        $("#mj_osd_posY").value = padding;
        break;
      case "tr":
        $("#mj_osd_posX").value = -(padding);
        $("#mj_osd_posY").value = padding;
        break;
    }
  })

  $("#mj_netip_enabled")?.addEventListener("change", (ev) => {
    $("#mj_netip_user").required = ev.target.checked;
    $("#mj_netip_password_plain").required = ev.target.checked;
  })

  $("#mj_netip_password_plain") && $("form").addEventListener("submit", (ev) => {
    const pw = $("#mj_netip_password_plain").value.trim();
    if (pw !== "") $("#mj_netip_password").value = generateSofiaHash(pw);
  })
</script>

<%in p/footer.cgi %>
