<pre class="debug">
<dl>
<dt>REQUEST_*</dt>
<dd>
<% echo "$(printenv|grep REQUEST_|sort 2>&1)" %></dd>
<dt>FORM_*</dt>
<dd>
<% echo "$(printenv|grep FORM_|sort 2>&1)" %></dd>
<dt>GET_*</dt>
<dd>
<% echo "$(printenv|grep GET_|sort 2>&1)" %></dd>
<dt>POST_*</dt>
<dd>
<% echo "$(printenv|grep POST_|sort 2>&1)" %></dd>
</dl>
<% echo "$(cat /etc/majestic.yaml 2>&1)" %>
</pre>
