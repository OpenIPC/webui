#!/usr/bin/haserl
content-type: text/html

<%in _header.cgi %>
<h2>Firmware</h2>

<div class="alert alert-danger">
<b>Attention: Destructive Actions!</b>
<p class="mb-0">Make sure you know what you are doing.</p>
</div>

<div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
<div class="col">
<div class="card mb-3 danger">
<h5 class="card-header">Upgrade from GitHub</h5>
<div class="card-body">
<form action="/cgi-bin/github.cgi" method="post">
<input type="hidden" name="action" value="github">
<p><input type="checkbox" name="reset" id="reset" value="true"> <label for="reset">Reset settings after upgrade.</label></p>
<p><input type="submit" class="btn btn-danger" value="Upgrade Firmware"></p>
</form>
</div>
</div>
<div class="card mb-3 danger">
<h5 class="card-header">Reset configuration</h5>
<div class="card-body">
<form action="/cgi-bin/reset.cgi" method="post">
<input type="hidden" name="action" value="reset">
<p><input type="submit" class="btn btn-danger" value="Reset Configuration"></p>
</form>
</div>
</div>
</div>
<div class="col">
<div class="card mb-3 danger">
<h5 class="card-header">Upload kernel</h5>
<div class="card-body">
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="kernel">
<div class="row">
<div class="col-12 mb-3"><label for="upfile">kernel file</label></div>
<div class="col-12 mb-3"><input type="file" name="upfile"></div>
</div>
<p><input type="submit" class="btn btn-danger" value="Upload File"></p>
</form>
</div>
</div>

<div class="card mb-3 danger">
<h5 class="card-header">Upload rootfs</h5>
<div class="card-body">
<form action="/cgi-bin/upload.cgi" method="post" enctype="multipart/form-data">
<input type="hidden" name="action" value="rootfs">
<div class="row">
<div class="col-12 mb-3"><label for="upfile">rootfs file</div>
<div class="col-12 mb-3"><input type="file" name="upfile"></div>
</div>
<p><input type="submit" class="btn btn-danger" value="Upload File"></p>
</form>
</div>
</div>
</div>
</div>

<%in _footer.cgi %>
