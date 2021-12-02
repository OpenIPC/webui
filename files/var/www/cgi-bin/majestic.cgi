#!/usr/bin/haserl
content-type: text/html

<%in _mj.cgi %>
<%in _header.cgi %>
<form action="/cgi-bin/majestic-settings.cgi" method="post">
<div class="cards">
<%
mj=$(echo "$mj"|sed "s/ /_/g")
for line in $mj
do
  param=${line%%|*}
  name=${param#.}
  domain=${name%.*}
  name=${name//./-}
  line=${line#*|}
  label=${line%%|*}
  line=${line#*|}
  units=${line%%|*}
  line=${line#*|}
  type=${line%%|*}
  line=${line#*|}
  options=${line%%|*}
  line=${line#*|}
  placeholder=${line%%|*}
  line=${line#*|}

  value=$(yaml-cli -g $param)

  if [ "$olddomain" != "$domain" ]; then
    [ ! -z "$olddomain" ] && echo "</dl></div>"
    olddomain="$domain"
    echo "<div>"
    echo "<h3>${domain}</h3>"
    echo "<dl>"
  fi
  echo "<dt>${label//_/ }</dt>"
  echo "<dd>"
  case "$type" in
    boolean)
      echo -n "<input type=\"checkbox\" name=\"${name}\" value=\"true\""
      [ "true" = "$value" ] && echo -n " checked"
      echo ">"
      ;;
    number)
      echo "<input type=\"number\" name=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      ;;
    range)
      echo "<input type=\"range\" name=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      echo "(<span id=\"v-${name}\" class=\"rval\">${value}</span>)"
      ;;
    select)
      echo "<select name=\"${name}\">"
      echo "<option value=\"\">- please select -</option>"
      for o in ${options//,/ }
      do
        echo -n "<option"
        [ "$o" = "$value" ] && echo -n " selected"
        echo ">${o}</option>"
      done
      echo "</select>"
      ;;
    string)
      echo "<input type=\"text\" name=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
      ;;
    *)
      ;;
  esac
  echo "<span>${units}</span>"
  echo "</dd>"
done
 echo "</dl>"
echo "</div>"
%>
</div>
<p>
<input type="submit" value="Save">
<input type="submit" value="Debug" onclick="javascript:document.querySelector('form').action='http://phphome.lan/info.php';">
</p>
</form>
<%in _footer.cgi %>
