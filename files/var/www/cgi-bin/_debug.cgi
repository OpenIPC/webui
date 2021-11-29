<pre class="debug">
<dl>
<dt>REQUEST_*</dt>
<dd><% echo "$(printenv|grep REQUEST_|sort)" %></dd>
<dt>FORM_*</dt>
<dd><% echo "$(printenv|grep FORM_|sort)" %></dd>
<dt>GET_*</h5>
<dd><% echo "$(printenv|grep GET_|sort)" %></dd>
<dt>POST_*</dt>
<dd><% echo "$(printenv|grep POST_|sort)" %></dd>
</dl>
</pre>
