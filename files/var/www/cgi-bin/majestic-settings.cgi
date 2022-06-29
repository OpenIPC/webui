#!/usr/bin/haserl
<%in p/common.cgi %>
<%in _mj.cgi %>
<%
page_title="Majestic settings"

mj=$(echo "$mj" | sed "s/ /_/g")
only="$GET_tab"; [ -z "$only" ] && only="system"
eval title="\$tT_mj_${only}"; [ -z "$title" ] && title=$only

if [ "POST" = "$REQUEST_METHOD" ]; then
  mj_conf=/etc/majestic.yaml
  temp_yaml=/tmp/majestic.yaml

  # make a copy of the actual config into memory
  cp -f $mj_conf $temp_yaml

  IFS=$'\n' # make newlines the only separator
  for param in $(printenv|grep POST_); do
    name=$(echo $param | sed 's/^POST_mj_//')
    key=".$(echo $name | cut -d= -f1 | sed 's/_/./g')"

    # do not include helping fields into config
    [ "$key" = ".netip.password.plain" ] && continue

    value="$(echo $name | cut -d= -f2)"

    # normalization
    case "$key" in
      .image.rotate)
        value="${value//°/}"
        [ "0" = "$value" ] && value="none"
        ;;
      .isp.antiFlicker)
        [ "50Hz" = "$value" ] && value="50"
        [ "60Hz" = "$value" ] && value="60"
        ;;
      .system.webAdmin)
        [ "true" = "$value" ] && value="enabled"
        [ "false" = "$value" ] && value="disabled"
        ;;
    esac

    # read existing value
    oldvalue=$(yaml-cli -g "$key" -i $temp_yaml)

    if [ -z "$value" ]; then
      # if no new value submitted but there is an existing value, delete the param
      [ -n "$oldvalue" ] && yaml-cli -d $key -i "$temp_yaml" -o "$temp_yaml"
    else
      # if new value is submitted and it differs from the existing one, update the param
      [ "$oldvalue" != "$value" ] && yaml-cli -s $key "$value" -i "$temp_yaml" -o "$temp_yaml"
    fi
  done

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

<div class="row row-cols-1 row-cols-xl-3 g-4">
  <div class="col">
    <h3><%= $title %></h3>
    <form action="<%= $SCRIPT_NAME %>" method="post">
<%
config=""
for line in $(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only"); do
  param=${line%%|*}; _n=${param#.}; domain=${_n%.*}; name=mj_${_n//./_}; line=${line#*|}; type=${line%%|*}; line=${line#*|}

  # assign param's value to a variable with param's name for form fields values
  eval $name=\"$(yaml-cli -g "$param")\"

  # hide some params in config
  [ "mj_netip_password_plain" != "$name" ] && config="${config}\n$(eval echo ${param}: \$$name)"

  case "$type" in
    boolean) field_switch "$name";;
    hidden)  field_hidden "$name";;
    number)  field_number "$name";;
    range)   field_range  "$name";;
    select)  field_select "$name";;
    string)  field_text   "$name";;
    *) echo "UNKNOWN FIELD: $name";;
  esac
done
%>
      <p class="mt-2"><input type="submit" class="btn btn-primary" value="Save changes"></p>
    </form>
  </div>
  <div class="col">
    <h3>Related settings</h3>
    <% pre "$config" %>
    <p><a href="info-majestic.cgi">See majestic.yaml</a></o>
  </div>
  <div class="col">
    <h3>Majestic config sections</h3>
    <div class="list-group list-group-flush" id="mj-tabs">
<%
for _l in $mj; do
  _p=${_l%%|*}; _n=${_p#.}; _d=${_n%.*}
  if [ "$_o" != "$_d" ]; then
    _o="$_d"
    _c="class=\"list-group-item\""; [ "$_d" = "$only" ] && _c="class=\"list-group-item active\" aria-current=\"true\""
    echo "<a ${_c} href=\"?tab=${_d}\">$(eval echo \$tT_mj_${_d})</a>"
  fi
done
unset _c; unset _d; unset _l; unset _n; unset _o; unset _p;
%>
    </div>
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
