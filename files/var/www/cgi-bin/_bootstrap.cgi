#!/usr/bin/haserl
<%
label_cols="col-md-4"
input_cols="col-md-8"

# alert_ "type" "extras"
alert_() { div_ "class=\"alert alert-${1}\" ${2}"; }
_alert() { _div; }
# alert "text" "type" "extras"
alert() { alert_ "$2" "$3"; echo -e "$1"; _alert; }

# button "text" "type" "extras"
button() { echo "<button type=\"button\" class=\"btn btn-${2}\" ${3}>${1}</button>"; }

# button_link_to "text" "url" "type" "extras"
button_link_to() { echo "<a class=\"btn btn-${3}\" href=\"${2}\" ${4}>${1}</a>"; }

# button_submit "text" "type" "extras"
button_submit() { echo "<button type=\"submit\" class=\"btn btn-${2} mt-3\" ${3}>${1}</button>"; }

# button_submit_action "action" "text" "extras"
button_submit_action() { echo "<button type=\"submit\" class=\"btn btn-danger\" name=\"action\" value=\"${1}\" ${3}>${2}</button>"; }

button_home() { button_link_to "$tButtonGoHome" "/" "primary"; }
button_reboot() { button_link_to "$tButtonReboot" "/cgi-bin/reboot.cgi" "danger"; }

# button_refresh
button_refresh() { link_to "$tButtonRefresh" "#" "class=\"btn btn-primary refresh\""; }

# row_ "class"
row_() { div_ "class=\"row ${1}\""; }
_row() { _div; }
row() { row_ "$2"; echo "$1"; _row; }

# col_ "class"
col_() { div_ "class=\"${1:=col}\""; }
_col() { _div; }

# card_ "text"
card_() { div_ "class=\"card mb-3 ${2}\""; card_header "$1"; card_body_; }
_card() { _div; _div; }

# card_header "text"
card_header() { div "$1" "class=\"card-header\""; }

card_body_() { div_ "class=\"card-body\""; }
_card_body() { _div; }
card_body() { card_body_; _card_body; }

# col_card "text"
col_card_() { col_ "col mb-3"; card_ "$1" "h-100"; }
_col_card() { _card; _col; }
col_card() { col_card_ "$1"; echo "$2"; _col_card; }

# col_first
col_first() { div_ "class=\"col\""; }
col_last() { _div; }
col_next() { col_last; col_first; }

# container "text"
container_() { div_ "class=\"container\""; }
_container() { _div; }
container() { container_; echo "$1"; _container; }

# field_checbox "name" "extras"
field_checkbox() {
  div_ "class=\"mb-2 boolean\""
    div_ "class=\"form-check\""
      echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}-false\" value=\"false\">"
      echo "<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" $(t_checked "$1" "true") value=\"true\" class=\"form-check-input\" ${2}>"
      label "$(t_label "$1")" "for=\"${1}\" class=\"form-check-label\""
    _div
  _div
}

# field_file "name"
field_file() {
  row_ "mb-2 file"
    label "$(t_label "$1")" "for=\"${1}\" class=\"col-md-3 form-label\""
    col_ "col-md-9"
      echo "<input type=\"file\" name=\"${1}\" id=\"${1}\" placeholder=\"$(t_placeholder "$1")\" class=\"form-control\">"
    _col
  _row
}

# field_hidden "name"
field_hidden() {
  echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}\" value=\"$(t_value "$1")\">";
}

# field_number "name"
field_number() {
  row_ "mb-2 number"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} col-form-label\""
    col_ "$input_cols"
      div_ "class=\"input-group\""
        echo "<input class=\"form-control text-end\" type=\"text\" name=\"${1}\" id=\"${1}\" value=\"$(t_value "$1")\" placeholder=\"$(t_placeholder "$1")\">"
        units "$1"
      _div
      help "$1"
    _col
  _row
}

# field_password "name"
field_password() {
  row_ "mb-2 password"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} col-form-label\""
    col_ "$input_cols"
      echo "<input type=\"password\" name=\"${1}\" id=\"${1}\" value=\"$(t_value "$1")\" class=\"form-control\" placeholder=\"$(t_placeholder "$1")\">"
    _col
  _row
}

# field_range "name"
field_range() {
  row_ "mb-2 range"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} col-form-label\""
    col_ "$input_cols"
      div_ "class=\"input-group\""
        if [ -n "$(t_options "$1" | grep -E auto)" ]; then
          span_ "class=\"input-group-text\""
            label "<input class=\"form-check-input auto-value\" type=\"checkbox\" data-for=\"${1}\" data-value=\"$(t_default "$1")\" $(t_checked "$1" "auto")> auto"
          _span
        fi
        echo "<input class=\"form-control text-end range\" type=\"text\" name=\"${1}\" id=\"${1}\" value=\"$(t_value "$1")\" placeholder=\"$(t_placeholder "$1")\" data-units=\"$(t_units "$1")\" $(t_readonly "$1" "auto")>"
        units "$1"
      _div
      help "$1"
    _col
  _row
}

# field_select "name"
field_select() {
  row_ "mb-2 select"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} col-form-label\""
    col_ "$input_cols"
      div_ "class=\"input-group\""
        echo "<select class=\"form-select\" id=\"${1}\" name=\"${1}\">"
        [ -z "$(t_value "$1")" ] && echo "<option value=\"\"></option>"
        for o in $(t_options "$1"); do
          _v="${o%|*}"; _n="${o#*|}"
          echo "<option value=\"${_v}\" $(t_selected "$1" "${_v}")>${_n}</option>"
          unset _v; unset _n
        done
        echo "</select>"
        units "$1"
      _div
      help "$1"
    _col
  _row
}

# field_swith "name"
field_switch() {
  row_ "mb-2 boolean"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} form-check-label\""
    col_ "$input_cols"
      div_ "class=\"form-check form-switch\""
        echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}-false\" value=\"false\">"
        echo "<input type=\"checkbox\" name=\"${1}\" id=\"${1}\" $(t_checked "$1" "true") role=\"switch\" value=\"true\" class=\"form-check-input\">"
      _div
      help "$1"
    _col
  _row
}

# field_text "name"
field_text() {
  row_ "mb-2 string"
    label "$(t_label "$1")" "for=\"${1}\" class=\"${label_cols} col-form-label\""
    col_ "$input_cols"
      div_ "class=\"input-group\""
        echo "<input type=\"text\" name=\"${1}\" id=\"${1}\" value=\"$(t_value "$1")\" class=\"form-control\" placeholder=\"$(t_placeholder "$1")\" ${2}>"
        units "$1"
      _div
      help "$1"
    _col
  _row
}

help() { [ -n "$(t_hint "$1")" ] && p "$(t_hint "$1")" "class=\"hint text-secondary\""; }

nav_() { A "nav" "$1"; }
_nav() { Z "nav"; }

navbar_() { nav_ "class=\"navbar navbar-light bg-light mb-3 ${1}\""; }
_navbar() { _nav; }

# nav_dropdown_ "text" "name"
nav_dropdown_() {
  li_ "class=\"nav-item dropdown\""
    link_to "$(eval echo \$tMenu${1})" "#" "class=\"nav-link dropdown-toggle\" id=\"dropdown${1}\" role=\"button\" data-bs-toggle=\"dropdown\" aria-expanded=\"false\""
  ul_ "class=\"dropdown-menu\" aria-labelledby=\"dropdown${1}\""
}
_nav_dropdown() { _ul; _li; }

# nav_dropdown_item "text" "url"
nav_dropdown_item() { link_to "$1" "$2" "class=\"dropdown-item\""; }

# nav_dropdown_to "text" "url"
nav_dropdown_to() { li "$(nav_dropdown_item "${1}" "${2}")"; }

nav_item() { li "$1" "class=\"nav-item\""; }
nav_link() { link_to "$1" "$2" "class=\"nav-link\""; }
nav_item_link() { nav_item "$(nav_link "$1" "$2")"; }

# navbar_toggler "id"
navbar_toggler() { echo "<button class=\"navbar-toggler\" type=\"button\" data-bs-toggle=\"collapse\" data-bs-target=\"#${1}\" aria-controls=\"${1}\" aria-expanded=\"false\" aria-label=\"Toggle navigation\"><span class=\"navbar-toggler-icon\"></span></button>"; }


units() { [ -n "$(t_units "$1")" ] && span "$(t_units "$1")" "class=\"input-group-text\""; }
%>
