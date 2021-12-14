<%in _common.cgi %>
<%in _mj.cgi %>
<%in _header.cgi %>
<h2><%= $page_title %></h2>
<% flash_read %>
<form action="/cgi-bin/majestic-settings-update.cgi" method="post">
<div class="row row-cols-1 row-cols-xl-2 row-cols-xxl-3 g-4 mb-3">
<% mj=$(echo "$mj" | sed "s/ /_/g" | grep -E $only)
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
    [ ! -z "$olddomain" ] && echo '</div></div></div>'
    olddomain="$domain"
    echo '<div class="col">'
    echo '<div class="card h-100">'
    echo "<div class=\"card-header\">${domain}</div>"
    echo '<div class="card-body">'
  fi
  case "$type" in
    boolean)
      [ "true" = "$value" ] && checked=" checked" || checked=""
      echo "<div class=\"row mb-2\">" \
        "<div class=\"col\">" \
          "<div class=\"form-check form-switch\">" \
            "<input type=\"hidden\" name=\"${name}\" id=\"${name}\" value=\"false\">" \
            "<input class=\"form-check-input\" name=\"${name}\" id=\"${name}\" value=\"true\" type=\"checkbox\" role=\"switch\"${checked}>" \
            "<label for=\"${name}\" class=\"form-check-label\">${label//_/ }</label>" \
          "</div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div></div>"
      ;;
    number)
      echo -n "<div class=\"row mb-2\">"  \
        "<div class=\"col-md-7\"><label for=\"${name}\" class=\"form-label\">${label//_/ }</label></div>" \
        "<div class=\"col-md-5\">" \
          "<div class=\"input-group\">" \
            "<input class=\"form-control text-end\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ ! -z "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    range)
      echo "<div class=\"row mb-2\">" \
        "<div class=\"col-12\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div>" \
        "<div class=\"col-12\">" \
          "<div class=\"input-group\">"
      if [ ! -z $(echo "${options}" | grep -E auto) ]
      then
        [ "auto" = "$value" ] && checked=" checked" || checked=""
        echo "<span class=\"input-group-text\">" \
          "<label><input type=\"checkbox\" class=\"form-check-input auto-value\" data-for=\"${name}\" data-value=\"${default}\"${checked}> auto</label>" \
          "</span>"
      fi
      [ "auto" = "$value" ] && readonly=" readonly" || readonly=""
      echo "<input class=\"form-control text-end range\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" data-units=\"${units}\"${readonly}>"
      [ ! -z "$units" ] && echo "<span class=\"input-group-text\">${units}</span>"
      echo "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    select)
      echo -n "<div class=\"row mb-2\">" \
        "<div class=\"col-md-7\"><label class=\"form-label\" for=\"${name}\">${label//_/ }</label></div>" \
        "<div class=\"col-md-5\">" \
          "<div class=\"input-group\">" \
            "<select class=\"form-select\" name=\"${name}\" id=\"${name}\">"
      [ -z "$value" ] && echo -n "<option value=\"\"></option>"
      for o in ${options//,/ }
      do
        [ "$o" = "$value" ] && selected=" selected" || selected=""
        echo -n "<option${selected}>${o}</option>"
      done
      echo -n "</select>"
      [ ! -z "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    string)
      echo "<div class=\"row mb-2\">" \
        "<div class=\"col-12 form-label\"><label for=\"${name}\">${label//_/ }</label></div>" \
        "<div class=\"col-12\">" \
          "<div class=\"input-group\">" \
            "<input class=\"form-control\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      [ ! -z "$units" ] && echo "<span class=\"input-group-text\">${units}</span>"
      echo "</div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div></div>"
      ;;
    *)
      ;;
  esac
done
%>
</div></div></div></div>

<button type="submit" class="btn btn-primary">Save Changes</button>
</form>
<%in _footer.cgi %>
