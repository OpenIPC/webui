<pre class="alert alert-warning">
<b>REQUEST_*</b>
<% echo "$(printenv|grep REQUEST_|sort 2>&1)" %>

<b>FORM_*</b>
<% echo "$(printenv|grep FORM_|sort 2>&1)" %>

<b>GET_*</b>
<% echo "$(printenv|grep GET_|sort 2>&1)" %>

<b>POST_*</b>
<% echo "$(printenv|grep POST_|sort 2>&1)" %>
</pre>

<pre class="alert alert-secondary">
<% echo "$(cat /etc/majestic.yaml 2>&1)" %>
</pre>
