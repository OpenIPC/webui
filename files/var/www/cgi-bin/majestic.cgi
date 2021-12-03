#!/usr/bin/haserl
content-type: text/html

<%in _mj.cgi %>
<%in _header.cgi %>
<h2>Majestic Settings</h2>
<form action="/cgi-bin/majestic-settings.cgi" method="post">
<div class="row row-cols-1 row-cols-xl-2 g-4 mb-4">
<%
mj=$(echo "$mj"|sed "s/ /_/g")
for line in $mj
do
  param=${line%%|*}; name=${param#.}; domain=${name%.*}; name=${name//./-}; line=${line#*|}
  label=${line%%|*}; line=${line#*|}
  units=${line%%|*}; line=${line#*|}
  type=${line%%|*}; line=${line#*|}
  options=${line%%|*}; line=${line#*|}
  placeholder=${line%%|*}; line=${line#*|}
  hint=${line%%|*}; line=${line#*|}

  value=$(yaml-cli -g $param)

  if [ "$olddomain" != "$domain" ]; then
    [ ! -z "$olddomain" ] && echo '</div></div></div>'
    olddomain="$domain"
    echo '<div class="col">'
    echo '<div class="card h-100 mb-3">'
    echo "<h5 class=\"card-header\">${domain}</h5>"
    echo '<div class="card-body">'
  fi
  case "$type" in
    boolean)
      [ "true" = "$value" ] && checked=" checked" || checked=""
      echo "<div class=\"row mb-2\">" \
        "<div class=\"col\"><div class=\"form-check form-switch\">" \
          "<input name=\"${name}\" id=\"${name}\" value=\"true\" type=\"checkbox\" role=\"switch\"${checked} class=\"form-check-input\">" \
          "<label for=\"${name}\" class=\"form-check-label\">${label//_/ }</label>" \
        "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    number)
      echo -n "<div class=\"row mb-2\">"  \
        "<div class=\"col-md-7\"><label for=\"${name}\" class=\"form-label\">${label//_/ }</label></div>" \
        "<div class=\"col-md-5\"><div class=\"input-group\">" \
          "<input type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" class=\"form-control text-end\">"
      [ ! -z "$units" ] && echo -n "<span class=\"input-group-text\">${units}</span>"
      echo "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    range)
      echo "<div class=\"row mb-2\">" \
        "<div class=\"col-lg-6\"><label for=\"${name}\" class=\"form-label\">${label//_/ }</label></div>" \
        "<div class=\"col-lg-6\"><div class=\"input-group\">"
      if [ ! -z $(echo "${options}" | grep -E auto) ]
      then
        [ "auto" = "$value" ] && checked=" checked" || checked=""
        echo "<span class=\"input-group-text\"><label><input type=\"checkbox\" class=\"form-check-input auto-value\" data-for=\"${name}\" data-value=\"${default}\"${checked}> auto</label></span>"
      fi
      [ "auto" = "$value" ] && readonly=" readonly" || readonly=""
      echo "<input type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" class=\"form-control text-end range\" data-units=\"${units}\"${readonly}>"
      [ ! -z "$units" ] && echo "<span class=\"input-group-text\">${units}</span>"
      echo "</div></div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div>"
      ;;
    select)
      echo -n "<div class=\"row mb-2\">" \
        "<div class=\"col-md-7\"><label for=\"${name}\" class=\"form-label\">${label//_/ }</label></div>" \
        "<div class=\"col-md-5\"><div class=\"input-group\">" \
          "<select name=\"${name}\" id=\"${name}\" class=\"form-control\">"
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
        "<div class=\"col-12\"><label for=\"${name}\" class=\"form-label\">${label//_/ }</label></div>" \
        "<div class=\"col-12\"><div class=\"input-group\">" \
          "<input type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" class=\"form-control\">"
      [ ! -z "$units" ] && echo "<span class=\"input-group-text\">${units}</span>"
      echo "</div>"
      [ ! -z "$hint" ] && echo "<p class=\"hint text-secondary\">${hint//_/ }</p>"
      echo "</div></div>"
      ;;
    *)
      ;;
  esac
done
echo "</div></div></div>"
%>
</div>
<p>
<input type="submit" class="btn btn-primary" value="Save">
<input type="submit" class="btn btn-warning" value="Debug" onclick="javascript:document.querySelector('form').action='http://phphome.lan/info.php';">
</p>
</form>
<%in _footer.cgi %>
