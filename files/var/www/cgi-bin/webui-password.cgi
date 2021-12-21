#!/usr/bin/haserl
<% page_title="Web Interface Access" %>
<%in _common.cgi %>
<%in _header.cgi %>
<div class="row">
  <div class="col-md-6 m-auto">
    <div class="card">
      <div class="card-header">Web Interface</div>
        <div class="card-body">
          <form action="/cgi-bin/webui-password-update.cgi" method="post">
            <div class="row mb-1">
              <label class="col-md-5 form-label" for="username">Username</label>
              <div class="col-md-7">
                <div class="input-group mb-3">
                  <input type="text" class="form-control" id="username" name="username"
                    autocomplete="username" value="admin" disabled>
                </div>
              </div>
            </div>
            <div class="row mb-1">
              <label class="col-md-5 form-label" for="password">Password</label>
              <div class="col-md-7">
                <div class="input-group mb-3">
                  <input type="password" class="form-control password" name="password"
                    id="password" autocomplete="new-password" value="" placeholder="K3wLHaZk3R!">
                  <div class="input-group-text">
                    <input type="checkbox" class="toggle-password" tabindex="-1" title="Show password">
                  </div>
                </div>
              </div>
            </div>
            <div class="row mb-1">
              <label class="col-md-5 form-label" for="password">Confirm Password</label>
              <div class="col-md-7">
                <div class="input-group mb-3">
                  <input type="password" class="form-control password" name="passwordconfirmation"
                    id="passwordconfirmation" autocomplete="new-password" value="" placeholder="K3wLHaZk3R!">
                  <div class="input-group-text">
                    <input type="checkbox" class="toggle-password" tabindex="-1" title="Show password">
                  </div>
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
$$('.toggle-password').forEach(el => { el.addEventListener('click', (ev) => {
  if (ev.target.checked) {
    $$('input.password').forEach(el => el.type = 'text');
  } else {
    $$('input.password').forEach(el => el.type = 'password');
  }
  $$('.toggle-password').forEach(el => el.checked = ev.target.checked);
  $('#password').focus();
})});
</script>

<%in _footer.cgi %>
