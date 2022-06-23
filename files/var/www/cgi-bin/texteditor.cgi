#!/usr/bin/haserl
<%in p/common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  f="$POST_f"
  t="$POST_t"

  # strip carriage return (\u000D) characters
  t=$(echo "$t"|sed "s/\r//g")

  if [ "restore" = "$POST_a" ]; then
    [ ! -f "$f" ] && redirect_to "${SCRIPT_NAME}?f=${f}" "danger" "$t_form_error_a"
    [ ! -f "$f.backup" ] && redirect_to "${SCRIPT_NAME}?f=${f}" "danger" "$t_form_error_a"
    mv "$f.backup" "$f"
    redirect_to "${SCRIPT_NAME}?f=${f}" "success" "$t_form_error_e"
  fi

  if [ -z "$t" ]; then
    flash_save "warning" "$t_form_error_b $t_form_error_c"
  else
    cp "$f" "$f.backup"
    echo "$t" > "$f"
    redirect_to "${SCRIPT_NAME}?f=${f}" "success" "$t_form_error_d"
  fi
else
  f="$GET_f"
  [ ! -f "$f" ] && flash_save "danger" "$t_form_error_a"

  if [ -n "$f" ]; then
    if [ "b" = "$( (cat -v "$f" | grep -q "\^@") && echo "b" )" ]; then
      flash_save "danger" "$t_form_error_f"
    elif [ "$(wc -c $f | awk '{print $1}')" -gt "102400" ]; then
      flash_save "danger" "$t_form_error_3"
    else
      t="$(cat $f | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")"
    fi
  fi
fi

page_title="$t_editor_0"
%>
<%in p/header.cgi %>
<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-4">
<div class="mb-1">
  <label class="form-label" for="f"><%= $t_editor_1 %></label>
  <input type="text" class="form-control" name="f" value="<%= $f %>" readonly>
</div>
<div class="mb-1">
  <textarea id="t" name="t" class="form-control font-monospace p-3" style="height:50vh"><%= "$t" %></textarea>
</div>
<% button_submit "$t_editor_2" %>
</form>

<%
if [ -f "${f}.backup" ]; then
  a="restore"
  h4 "$t_editor_3"
  ex "diff ${f}.backup ${f}"
  form_ $SCRIPT_NAME
    field_hidden "f"
    field_hidden "a"
    button_submit "$t_editor_4" "danger"
  _form
fi
%>
<%in p/footer.cgi %>
