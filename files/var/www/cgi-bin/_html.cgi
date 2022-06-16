#!/usr/bin/haserl
<%
# tag "tag" "text" "extras"
tag() { echo "<${1} ${3}>${2}</${1}>"; }

A() { echo "<${1} ${2}>"; }
Z() { echo "</${1}>"; }

# tag "text" "extras"
b()     { tag "b"     "$1" "$2"; }
dd()    { tag "dd"    "$1" "$2"; }
div()   { tag "div"   "$1" "$2"; }
dt()    { tag "dt"    "$1" "$2"; }
h1()    { tag "h1"    "$1" "$2"; }
h2()    { tag "h2"    "$1" "$2"; }
h3()    { tag "h3"    "$1" "$2"; }
h4()    { tag "h4"    "$1" "$2"; }
h5()    { tag "h5"    "$1" "$2"; }
h6()    { tag "h6"    "$1" "$2"; }
i()     { tag "i"     "$1" "$2"; }
label() { tag "label" "$1" "$2"; }
li()    { tag "li"    "$1" "$2"; }
p()     { tag "p"     "$1" "$2"; }
span()  { tag "span"  "$1" "$2"; }
td()    { tag "td"    "$1" "$2"; }
th()    { tag "th"    "$1" "$2"; }

footer_() { A "footer" "$1"; }
_footer() { Z "footer"; }

div_() { A "div" "$1"; }
_div() { Z "div"; }

dl_() { A "dl" "$1"; }
_dl() { Z "dl"; }

li_() { A "li" "$1"; }
_li() { Z "li"; }

main_() { A "main" "$1"; }
_main() { Z "main"; }

nav_() { A "nav" "$1"; }
_nav() { Z "nav"; }

ol_() { A "ol" "$1"; }
_ol() { Z "ol"; }

pre_() { A "pre" "$1"; }
_pre() { Z "pre"; }

span_() { A "span" "$1"; }
_span() { Z "span"; }

ul_() { A "ul" "$1"; }
_ul() { Z "ul"; }

form_() {
  A "form" "action=\"${1}\" method=\"${2:=get}\" ${3}"
}
_form() { Z "form"; }

# image "src" "extras"
image() {
  echo "<img src=\"${1}\" alt=\"Image: ${1}\" ${2}>"
}

link_css() {
  echo "<link rel=\"stylesheet\" href=\"${1}\">"
}

link_js() {
  echo "<script src="${1}"></script>"
}

link_to() {
  echo "<a href=\"${2}\" ${3}>${1}</a>"
}

# pre "text" "extras"
pre() {
  # replace <, >, &, ", and ' with HTML entities
  tag "pre" "$(echo "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")" "$2"
}

video_source() {
  echo "<source src=\"${1}\" type=\"${2}\">"
}

video_() {
  echo "<video autoplay controls ${1}>"
}
_video() {
  echo "</video>";
}
%>
