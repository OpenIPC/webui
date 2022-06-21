#!/usr/bin/haserl
<%in _common.cgi %>
<%
if [ "POST" = "$REQUEST_METHOD" ]; then
  f="$POST_f"
  t="$POST_t"

  if [ "restore" = "$POST_a" ]; then
    [ ! -f "$f" ] && redirect_to "${SCRIPT_NAME}?f=${f}" "danger" "$tM_FileNotFound"
    [ ! -f "$f.backup" ] && redirect_to "${SCRIPT_NAME}?f=${f}" "danger" "$tM_FileNotFound"
    mv "$f.backup" "$f"
    redirect_to "${SCRIPT_NAME}?f=${f}" "success" "$tM_FileRestored"
  fi

  if [ -z "$t" ]; then
    flash_save "warning" "$fM_FileEmpty $tM_FileNotSaved"
  else
    cp "$f" "$f.backup"
    echo "$t" > "$f"
    redirect_to "${SCRIPT_NAME}?f=${f}" "success" "$tM_FileSaved"
  fi
else
  f="$GET_f"
  [ ! -f "$f" ] && flash_save "danger" "$tM_FileNotFound"

  if [ -n "$f" ]; then
    if [ "b" = "$( (cat -v "$f" | grep -q "\^@") && echo "b" )" ]; then
      flash_save "danger" "$tM_FileNotText"
    elif [ "$(wc -c $f | awk '{print $1}')" -gt "102400" ]; then
      flash_save "danger" "$tM_FileTooLarge"
    else
      t="$(cat $f | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g")"
    fi
  fi
fi

page_title="$tPT_TextEditor"
%>
<%in _header.cgi %>
<form action="<%= $SCRIPT_NAME %>" method="post" class="mb-4">
<div class="mb-1">
  <label class="form-label" for="f">File name</label>
  <input type="text" class="form-control" name="f" value="<%= $f %>" readonly>
</div>
<div class="mb-1">
  <textarea id="t" name="t" class="form-control font-monospace p-3" style="height:50vh"><%= "$t" %></textarea>
</div>
<% button_submit "$tB_SaveChanges" "primary" %>
</form>

<%
if [ -f "${f}.backup" ]; then
  a="restore"
  h4 "Changes against previous version"
  ex "diff ${f}.backup ${f}"
  form_ $SCRIPT_NAME
    field_hidden "f"
    field_hidden "a"
    button_submit "Restore" "danger"
  _form
fi
%>
<%in p/footer.cgi %>
