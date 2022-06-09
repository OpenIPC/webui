#!/usr/bin/haserl
<%
tag() {
  tag="$1"
  text="$2"
  extras=""; [ -n "$3" ] && extras=" $3"

  if [ "$tag" in "pre" ]; then
    # replace <, >, &, ", and ' with HTML entities
    text="$(echo "$text" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g;s/'/&#39;/g")"
  fi

  echo "<${tag}${extras}>${text}</${tag}>"
}

div_() { echo "<div ${1}>"; }
_div() { echo "</div>"; }

dl_() { echo "<dl ${1}>"; }
_dl() { echo "</dl>"; }

ul_() { echo "<ul ${1}>"; }
_ul() { echo "</ul>"; }

form_() {
  url="$1"
  method="get"; [ -n "$2" ] && method="$2"
  extras=""; [ -n "$3" ] && extras=" $3"
  echo "<form action=\"${url}\" method=\"${method}\"${extras}>"
}
_form() { echo "</form>"; }

b()    { tag "b"    "$1" "$2"; }
dd()   { tag "dd"   "$1" "$2"; }
div()  { tag "div"  "$1" "$2"; }
dt()   { tag "dt"   "$1" "$2"; }
h1()   { tag "h1"   "$1" "$2"; }
h2()   { tag "h2"   "$1" "$2"; }
h3()   { tag "h3"   "$1" "$2"; }
h4()   { tag "h4"   "$1" "$2"; }
h5()   { tag "h5"   "$1" "$2"; }
h6()   { tag "h6"   "$1" "$2"; }
i()    { tag "i"    "$1" "$2"; }
label() { tag "label" "$1" "$2"; }
li()   { tag "li"   "$1" "$2"; }
p()    { tag "p"    "$1" "$2"; }
pre()  { tag "pre"  "$1" "$2"; }
span() { tag "span" "$1" "$2"; }
td()   { tag "td"   "$1" "$2"; }
th()   { tag "th"   "$1" "$2"; }

link_to() {
  echo "<a href=\"${2}\" ${3}>${1}</a>"
}

pre() {
  # replace <, >, &, ", and ' with HTML entities
  text="$(echo "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g;s/'/&#39;/g")"
  extras=""; [ -n "$2" ] && extras=" ${2}"
  echo "<pre${extras}>${text}</pre>"
}
%>
