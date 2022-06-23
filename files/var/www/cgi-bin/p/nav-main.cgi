<nav class="navbar navbar-dark navbar-expand-lg fixed-top">
<div class="container">
<a class="navbar-brand" href="/cgi-bin/status.cgi"><img alt="Image: OpenIPC logo" height="32" src="/a/logo.svg"></a>
<button aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbarNav" data-bs-toggle="collapse" type="button">
<span class="navbar-toggler-icon"></span>
</button>
<div class="collapse navbar-collapse justify-content-end" id="navbarNav">
<ul class="navbar-nav">
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownInformation" role="button"><%= $t_nav_1 %></a>
<ul aria-labelledby="dropdownInformation" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/status.cgi"><%= $t_nav_2 %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/info-cron.cgi"><%= $t_nav_3 %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/info-dmesg.cgi"><%= $t_nav_4 %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/info-httpd.cgi"><%= $t_nav_5 %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/info-log.cgi"><%= $t_nav_6 %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/info-overlay.cgi"><%= $t_nav_7 %></a></li>
</ul>
</li>
<li class="nav-item"><a class="nav-link" href="/cgi-bin/firmware.cgi"><%= $t_nav_8 %></a></li>
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownSettings" role="button"><%= $t_nav_9 %></a>
<ul aria-labelledby="dropdownSettings" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/network.cgi"><%= $t_nav_a %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/network-ntp.cgi"><%= $t_nav_b %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/webui-settings.cgi"><%= $t_nav_c %></a></li>
</ul>
</li>
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownMajestic" role="button"><%= $t_nav_d %></a>
<ul aria-labelledby="dropdownMajestic" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/majestic-settings.cgi"><%= $t_nav_e %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/majestic-config-actions.cgi"><%= $t_nav_f %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/majestic-debug.cgi"><%= $t_nav_g %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/preview-help.cgi"><%= $t_nav_h %></a></li>
</ul>
</li>
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownTools" role="button"><%= $t_nav_i %></a>
<ul aria-labelledby="dropdownTools" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/tools.cgi"><%= $t_nav_j %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/console.cgi"><%= $t_nav_k %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/ssh-keys.cgi"><%= $t_nav_l %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/sdcard.cgi"><%= $t_nav_m %></a></li>
</ul>
</li>
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownServices" role="button"><%= $t_nav_n %></a>
<ul aria-labelledby="dropdownServices" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/plugin-bigbro.cgi"><%= $t_nav_o %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/plugin-ipeye.cgi"><%= $t_nav_p %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/plugin-telegram.cgi"><%= $t_nav_q %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/plugin-vtun.cgi"><%= $t_nav_r %></a></li>
<li><a class="dropdown-item" href="/cgi-bin/plugin-yadisk.cgi"><%= $t_nav_s %></a></li>
</ul>
</li>
<li class="nav-item"><a class="nav-link" href="/cgi-bin/preview.cgi"><%= $t_nav_t %></a></li>
<li class="nav-item dropdown">
<a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownHelp" role="button"><%= $t_nav_u %></a>
<ul aria-labelledby="dropdownHelp" class="dropdown-menu">
<li><a class="dropdown-item" href="/cgi-bin/about.cgi"><%= $t_nav_v %></a></li>
<li><a class="dropdown-item" href="https://openipc.org/wiki/"><%= $t_nav_w %></a></li>
</ul>
</li>
</ul>
</div>
</div>
</nav>
