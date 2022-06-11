#!/usr/bin/haserl
<%
# alert "text" "type" "extras"
alert() {
  alert_ "$2" "$3"
  echo "$1"
  _alert
}

# alert_ "type" "extras"
alert_() {
  type="info"; [ -n "$1" ] && type="$1"
  extras=""; [ -n "$2" ] && extras=" ${2}"
  div_ "class=\"alert alert-${type}\"${extras}"
}

# _alert
_alert() {
  _div
}

# button "text" "type" "extras"
button() {
  type="$2"; [ -z "$type" ] && type="primary"
  extras=""; [ -z "$3" ] && extras=" ${3}"
  echo "<button type=\"button\" class=\"btn btn-${type}\"${extras}>${1}</button>"
}

# button_link_to "text" "url" "type" "extras"
button_link_to() {
  type="$3"; [ -z "$type" ] && type="primary"
  extras=""; [ -z "$4" ] && extras=" ${4}"
  echo "<a class=\"btn btn-${type}\" href=\"${2}\">${1}</a>"
}

# button_submit "text" "type"
button_submit() {
  text="$1"; [ -z "$text" ] && text="$tButtonFormSubmit"
  type="$2"; [ -z "$type" ] && type="primary"
  echo "<button type=\"submit\" class=\"btn btn-${type} mt-3\">${text}</button>"
}

# button_submit_action "action" "text"
button_submit_action() {
  echo "<button type=\"submit\" class=\"btn btn-danger\" name=\"action\" value=\"${1}\">${2}</button>"
}

# button_submit_delete "action" "text"
button_submit_delete() {
  echo "<button type=\"submit\" class=\"btn btn-danger\" name=\"action\" value=\"${1}\" data-method=\"delete\">${2}</button>"
}

# button_home
button_home() {
  button_link_to "$tButtonGoHome" "/"
}

# button_refresh
button_refresh() {
  echo "<a class=\"btn btn-primary refresh\">${tButtonRefresh}</a>"
}

# card_header "text"
card_header() {
  div "$1" "class=\"card-header\""
}

# card_ "text"
card_() {
  div_ "class=\"card mb-3\""
  card_header "$1"
  div_ "class=\"card-body\""
}

# _card
_card() {
  _div
  _div
}

# col_card "text"
col_card_() {
  div_ "class=\"col mb-3\""
  div_ "class=\"card h-100\""
  card_header "$1"
  div_ "class=\"card-body\""
}

# _col_card
_col_card() {
  _div
  _div
  _div
}

# col_first
col_first() {
  div_ "class=\"col\""
}

# col_lastr
col_last() {
  _div
}

# col_next
col_next() {
  col_last
  col_first
}

# dd_cols "text" "extras"
dd_cols() {
  extras=""; [ -n "$2" ] && extras=" ${2}"
  dd "$1" "class=\"col-8 text-end\"${extras}"
}

# dt_cols "text" "extras"
dt_cols() {
  extras=""; [ -n "$2" ] && extras=" ${2}"
  dt "$1" "class=\"col-4\"${extras}"
}

# dropdown_to "text" "url"
dropdown_to() {
  tag "li" "<a class=\"dropdown-item\" href=\"${2}\">${1}</a>"
}

# field_checbox "name" "extras"
field_checkbox() {
  name="$1"
  extras=""; [ -n "$2" ] && extras=" ${2}"
  eval "value=\"\$${name}\""
  eval "text=\"\$tLabel_${name}\""; [ -z "$text" ] && text="Please translate \$tLabel_${name}"
  [ "true" = "$value" ] && checked=" checked" || checked=""

  div_ "class=\"mb-2 boolean\""
  div_ "class=\"form-check\""
  echo "<input type=\"hidden\" name=\"${name}\" id=\"${name}-false\" value=\"false\">"
  echo "<input type=\"checkbox\" name=\"${name}\" id=\"${name}\" ${checked} value=\"true\" class=\"form-check-input\"${extras}>"
  label "${text//_/ }" "for=\"${name}\" class=\"form-check-label\""
  _div
  _div
}

# field_file "name"
field_file() {
  name="$1"
  eval "text=\"\$tLabel_${name}\""
  eval "placeholder=\"\$tPlaceholder_${name}\""

  div_ "class=\"row mb-2 file\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-3 form-label\""
  div_ "class=\"col-md-9\""
  echo "<input type=\"file\" name=\"${name}\" id=\"${name}\" placeholder=\"${placeholder}\" class=\"form-control\">"
  _div
  _div
}

# field_hidden "name"
field_hidden() {
  name="$1"
  eval "value=\"\$${name}\""

  echo "<input type=\"hidden\" name=\"${name}\" id=\"${name}\" value=\"${value}\">"
}

# field_number "name"
field_number() {
  name="$1"
  eval "value=\"\$${name}\""
  eval "text=\"\$tLabel_${name}\""; [ -z "$text" ] && text="Please translate \$tLabel_${name}"

  div_ "class=\"row mb-2 number\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 col-form-label\""
  div_ "class=\"col-md-7\""
  div_ "class=\"input-group\""
  echo "<input class=\"form-control text-end\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\">"
  [ -n "$units" ] && span "$units" "class=\"input-group-text\""
  _div
  [ -n "$hint" ] && help "$hint"
  _div
  _div
}

# field_password "name"
field_password() {
  name="$1"
  eval "text=\"\$tLabel_${name}\""
  eval "value=\"\$${name}\""

  div_ "class=\"row mb-2 password\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 col-form-label\""
  div_ "class=\"col-md-7\""
  echo "<input type=\"password\" name=\"${name}\" id=\"${name}\" value=\"${value}\" class=\"form-control\">"
  _div
  _div
}

# field_range "name"
field_range() {
  name="$1"
  eval "text=\"\$tLabel_${name}\""
  eval "value=\"\$${name}\""
  readonly=""; [ "auto" = "$value" ] && readonly=" readonly"

  div_ "class=\"row mb-2 range\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 col-form-label\""
  div_ "class=\"col-md-7\""
  div_ "class=\"input-group\""
  if [ ! -z $(echo "${options}" | grep -E auto) ]; then
    [ "auto" = "$value" ] && checked=" checked" || checked=""
    span_ "class=\"input-group-text\""
    label "<input class=\"form-check-input auto-value\" type=\"checkbox\" data-for=\"${name}\" data-value=\"${default}\"${checked}> auto"
    _span
  fi
  echo "<input class=\"form-control text-end range\" type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" placeholder=\"${placeholder}\" data-units=\"${units}\"${readonly}>"
  [ -n "$units" ] && span "${units}" "class=\"input-group-text\""
  _div
  [ -n "$hint" ] && help "$hint"
  _div
  _div
}

# field_select "name"
field_select() {
  name="$1"
  eval "text=\"\$tLabel_${name}\""
  eval "hint=\"\$tHint_${name}\"";
  eval "options=\"\$${name}_options\""
  eval "placeholder=\"\$tPlaceholder_${name}\"";
  eval "value=\"\$${name}\""

  div_ "class=\"row mb-2 select\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 col-form-label\""
  div_ "class=\"col-md-7\""
  div_ "class=\"input-group\""
  echo "<select class=\"form-select\" id=\"${name}\" name=\"${name}\">"
  echo "<option value=\"\"></option>"
  for item in $options; do
    option_name="${item}"
    option_value="${item}"; [ -z "$option_value" ] && option_value="$option_name"
    selected=""; [ -n "$value" ] && [ "$option_value" = "$value" ] && selected=" selected"
    echo "<option value=\"${option_value}\"${selected}>${option_name}</option>"
  done
  echo "</select>"
  [ -n "$units" ] && span "${units}" "class=\"input-group-text\""
  _div
  [ -n "$hint" ] && help "$hint"
  _div
  _div
}

# field_swith "name"
field_switch() {
  name="$1"
  eval "value=\"\$${name}\"";
  eval "text=\"\$tLabel_${name}\""
  eval "hint=\"\$tHint_${name}\""; [ -n "$hint" ] && hint="<p class=\"hint\">${hint}</p>"
  checked=""; [ "true" = "$value" ] && checked=" checked"

  div_ "class=\"row mb-2 boolean\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 form-check-label border-bottom\""
  div_ "class=\"col-md-7\""
  div_ "class=\"form-check form-switch\""
  echo "<input type=\"hidden\" name=\"${name}\" id=\"${name}-false\" value=\"false\">"
  echo "<input type=\"checkbox\" name=\"${name}\" id=\"${name}\"${checked} role=\"switch\" value=\"true\" class=\"form-check-input\">"
  _div
  [ -n "$hint" ] && help "$hint"
  _div
  _div
}

# field_text "name"
field_text() {
  name="$1"
  extras=""; [ -n "$2" ] && extras=" ${2}"
  eval "value=\"\$${name}\""
  eval "text=\"\$tLabel_${name}\"";
  eval "hint=\"\$tHint_${name}\"";
  eval "placeholder=\"\$tPlaceholder_${name}\"";

  input="<input type=\"text\" name=\"${name}\" id=\"${name}\" value=\"${value}\" class=\"form-control\" placeholder=\"${placeholder}\"${extras}>"

  [ -z "$text" ] && text="Missing translation for \$tLabel_${name}"
  [ "$name" != "isp_sensorConfig" ] && placeholder=${placeholder//_/ }

  div_ "class=\"row mb-2 string\""
  label "${text//_/ }" "for=\"${name}\" class=\"col-md-5 col-form-label\""
  div_ "class=\"col-md-7\""
  div_ "class=\"input-group\""
  echo "$input"
  [ -n "$units" ] && span "$units" "class=\"input-group-text\""
  _div
  [ -n "$hint" ] && help "$hint"
  _div
  _div
}

help() {
  p "${1//_/ }" "class=\"hint text-secondary\""
}
%>
