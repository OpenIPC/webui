<%in _common.cgi %>
<% get_system_info %>
<%in _mj.cgi %>
<%in _header.cgi %>
<form action="/cgi-bin/majestic-settings-update.cgi" method="post">
<div class="row row-cols-1 row-cols-xl-2 row-cols-xxl-3 g-4 mb-3">
<%
mj=$(echo "$mj" | sed "s/ /_/g" | grep -E $only)
for line in $mj; do
  param=${line%%|*}; name=${param#.}; domain=${name%.*}; name=${name//./-}; line=${line#*|}
  label=${line%%|*}; line=${line#*|}
  units=${line%%|*}; line=${line#*|}
  type=${line%%|*}; line=${line#*|}
  options=${line%%|*}; line=${line#*|}
  placeholder=${line%%|*}; line=${line#*|}
  hint=${line%%|*}; line=${line#*|}
  value=$(yaml-cli -g "$param")

  if [ "$olddomain" != "$domain" ]; then
    [ -n "$olddomain" ] && echo -n '</div></div></div>'
    olddomain="$domain"
    echo "<div class=\"col\"><div class=\"card h-100\"><div class=\"card-header\">${domain}</div><div class=\"card-body\">"
  fi

  echo -n "<div class=\"row mb-2 ${type}\">"
  case "$type" in
    boolean)
      echo -n "<div class=\"col\">"
      [ "true" = "$value" ] && checked=" checked" || checked=""
      echo -n "<div class=\"form-check form-switch\"><input type=\"hidden\" name=\"${name}\" id=\"${name}-false\"" \
        " value=\"false\"><input class=\"form-check-input\" name=\"${name}\" id=\"${name}\" type=\"checkbox\"${checked}" \
        " role=\"switch\" value=\"true\"><label class=\"form-check-label\" for=\"${name}\">${label//_/ }</label></div>"
      [ -n "$hint" ] && echo -n "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n "</div>"
      ;;
    hidden)
      echo -n "<input type=\"hidden\" name=\"${name}\" id=\"${name}\" value=\"${value}\">"
      ;;
    number)
      echo -n "<div class=\"col-md-7\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div><div" \
        " class=\"col-md-5\"><div class=\"input-group\"><input class=\"form-control text-end\" type=\"text\"" \
        " name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ -n "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo -n "</div></div>"
      [ -n "$hint" ] && echo -n "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      ;;
    range)
      echo -n "<div class=\"col-12\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div><div" \
        " class=\"col-12\"><div class=\"input-group\">"
      if [ ! -z $(echo "${options}" | grep -E auto) ]; then
        [ "auto" = "$value" ] && checked=" checked" || checked=""
        echo -n "<span class=\"input-group-text\"><label><input class=\"form-check-input auto-value\"" \
          " type=\"checkbox\" data-for=\"${name}\" data-value=\"${default}\"${checked}> auto</label></span>"
      fi
      [ "auto" = "$value" ] && readonly=" readonly" || readonly=""
      echo -n "<input class=\"form-control text-end range\" type=\"text\" name=\"${name}\" id=\"${name}\"" \
       " value=\"${value}\" placeholder=\"${placeholder}\" data-units=\"${units}\"${readonly}>"
      [ -n "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo -n "</div></div>"
      [ -n "$hint" ] && echo -n "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      ;;
    select)
      echo -n "<div class=\"col-md-7\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div><div" \
        " class=\"col-md-5\"><div class=\"input-group\"><select class=\"form-select\" name=\"${name}\" id=\"${name}\">"
      [ -z "$value" ] && echo -n "<option value=\"\"></option>"
      for o in ${options//,/ }; do
        [ "$o" = "$value" ] && selected=" selected" || selected=""
        echo -n "<option${selected}>${o}</option>"
      done
      echo -n "</select>"
      [ -n "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo -n "</div></div>"
      [ -n "$hint" ] && echo -n "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      ;;
    string)
      [ "$name" != "isp-sensorConfig" ] && placeholder=${placeholder//_/ }
      echo -n "<div class=\"col-12\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div><div" \
        " class=\"col-12\"><div class=\"input-group\"><input class=\"form-control\" type=\"text\" name=\"${name}\"" \
        " id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ -n "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo -n "</div>"
      [ -n "$hint" ] && echo -n "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo -n "</div>"
      ;;
    *)
      ;;
  esac
  echo "</div>"
done
%>
</div></div></div></div>
<button type="submit" class="btn btn-primary"><%= $tButtonFormSubmit %></button>
</form>

<script src="/js/majestic-settings.js"></script>
<script>
  if (screen.width < 768) {
    const button = $('button[type=submit]');
    const div = document.createElement('div');
    div.classList.add('fixed-bottom','p-3','bg-light');
    div.appendChild(button.cloneNode(true));
    button.replaceWith(div);
  }

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
