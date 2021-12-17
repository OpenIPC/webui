#!/usr/bin/haserl
<% page_title="Web Interface Access" %>
<%in _common.cgi %>
<%in _header.cgi %>
<h2><%= $page_title %></h2>
<% flash_read %>
<div class="row">
  <div class="col-md-6 m-auto">
    <div class="card">
      <div class="card-header">Web Interface</div>
        <div class="card-body">
          <form action="/cgi-bin/webui-password-update.cgi" method="post">
            <div class="row mb-1">
              <label class="col-md-5 form-label" for="password">Password</label>
              <div class="col-md-7">
                <div class="input-group mb-3">
                  <input type="password" class="form-control password" name="password" id="password" value="" placeholder="K3wLHaZk3R!">
                  <div class="input-group-text">
                    <button type="button" class="btn btn-sm btn-white p-0" id="toggle-password"><img src="/img/eye-fill.svg" alt="Toggle password"></button>
                  </div>
                </div>
              </div>
            </div>
            <div class="row mb-1">
              <label class="col-md-5 form-label" for="password">Confirm Password</label>
              <div class="col-md-7">
                <div class="input-group mb-3">
                  <input type="password" class="form-control password" name="passwordconfirmation" id="passwordconfirmation" value="" placeholder="K3wLHaZk3R!">
                </div>
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Update Password</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
$('#toggle-password').addEventListener('click', (ev) => {
  const img = $('#toggle-password img');
  if ($('#password').type == 'password') {
    $$('input.password').forEach(el => el.type = 'text');
    img.src = '/img/eye-slash-fill.svg';
  } else {
    $$('input.password').forEach(el => el.type = 'password');
    img.src = '/img/eye-fill.svg';
  }
  $('#password').focus();
  ev.preventDefault();
})
</script>

<%in _footer.cgi %>
