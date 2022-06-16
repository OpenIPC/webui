#!/usr/bin/haserl
<%in _common.cgi %>
<%in _mj.cgi %>
<%
get_system_info
page_title="$tPageTitleMajesticSettings"
only="$GET_group"
[ -z "$only" ] && only="system"
mj=$(echo "$mj" | sed "s/ /_/g")
%>
<%in _header.cgi %>
<%
navbar_ "navbar-expand-md"
  div_ "class=\"container-fluid\""
    navbar_toggler "navbarSupportedContent"
    image "/img/majestic-logo.png" "width=32 height=32 class=me-2"
    div_ "class=\"collapse navbar-collapse\" id=\"navbarSupportedContent\""
      ul_ "class=\"navbar-nav me-auto mb-2 mb-lg-0 navbar-nav-scroll\" style=\"--bs-scroll-height: 15em;\""
        for line in $mj; do
          param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}
          if [ "$olddomain" != "$domain" ]; then
            olddomain="$domain"; active=""; [ "$domain" == "$only" ] && active=" active"
            eval "title=\"\$tMjNav_$domain\""
            li "$(link_to "$title" "?group=${domain}" "class=\"nav-link${active}\"")" "class=\"nav-item small\""
          fi
        done
      _ul
    _div
  _div
_navbar

eval title="\$tMjTitle_${only}"
[ -z "$title" ] && title=$only

h3 "$title" "class=\"my-4\""

row_ "row-cols-1 row-cols-xl-2 g-4 mb-3"
  col_card_ "Settings"
    form_ "/cgi-bin/majestic-settings-update.cgi" "post"
      mj=$(echo "$mj" | sed "s/ /_/g" | grep -E "^\.$only")
      config=""
    for line in $mj; do
      param=${line%%|*}; fullname=${param#.}; domain=${fullname%.*}; name=mj_${fullname//./_}; line=${line#*|}
      type=${line%%|*}; line=${line#*|}

      eval "$name=\"$(yaml-cli -g "$param")\""
      config="${config}\n${param}: $(yaml-cli -g "$param")"
      case "$type" in
        boolean)
          field_switch "$name"
          ;;
        hidden)
          field_hidden "$name"
          ;;
        number)
          field_number "$name"
          ;;
        range)
          field_range "$name"
          ;;
        select)
          field_select "$name"
          ;;
        string)
          field_text "$name"
          ;;
        *)
          ;;
      esac
    done

    button_submit "$tButtonFormSubmit" "primary"
    _form
  _col_card

  col_card_ "Config excerpt"
    pre "$(echo -e "$config")"
  _col_card
_row
%>

<script src="/js/majestic-settings.js"></script>
<script>
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
</script>
<%in _footer.cgi %>
