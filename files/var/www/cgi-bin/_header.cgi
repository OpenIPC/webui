<% export PATH=/bin:/sbin:/usr/bin:/usr/sbin %>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OpenIPC</title>
<link rel="shortcut icon" href="/favicon.png">
<% if [ ! -z $(yaml-cli -g .net.intranet) ]; then %>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>
<% else %>
<link rel="stylesheet" href="/bootstrap.min.css">
<script src="/bootstrap.bundle.min.js"></script>
<% fi %>
<link rel="stylesheet" href="/bootstrap.override.css">
<script src="/main.js"></script>
</head>
<body id="top">
<nav class="navbar navbar-expand-lg navbar-dark">
<div class="container">
<a class="navbar-brand" href="/"><img src="/logo.png" width="116" height="32" alt=""></a>
<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
<div class="collapse navbar-collapse justify-content-end" id="navbarNav">
<ul class="navbar-nav">
<li class="nav-item"><a class="nav-link" href="/cgi-bin/index.cgi">Global Settings</a></li>
<li class="nav-item"><a class="nav-link" href="/cgi-bin/majestic.cgi">Majestic Settings</a></li>
<li class="nav-item"><a class="nav-link" href="/cgi-bin/monitor.cgi">Monitoring Tools</a></li>
</ul>
</div>
</div>
</nav>
<main>
<div class="container p-3">
