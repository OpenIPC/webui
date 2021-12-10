<% http_header_text %>

------- REQUEST_* :
<% echo "$(printenv|grep REQUEST_|sort 2>&1)" %>
------- FORM_*    :
<% echo "$(printenv|grep FORM_|sort 2>&1)" %>
------- GET_*     :
<% echo "$(printenv|grep GET_|sort 2>&1)" %>
------- POST_*    :
<% echo "$(printenv|grep POST_|sort 2>&1)" %>

---------------------------------------------
