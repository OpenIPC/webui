content-type: text/html

<%
[ ! -z "$page_title" ] && page_title="$page_title - OpenIPC" || page_title="OpenIPC"
%>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title><%= $page_title %></title>
  <link rel="shortcut icon" href="/favicon.png">
  <link rel="stylesheet" href="/bootstrap.min.css">
  <link rel="stylesheet" href="/bootstrap.override.css">
  <script src="/bootstrap.bundle.min.js"></script>
  <script src="/main.js"></script>
</head>
<body id="top">
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
  <div class="container">
    <a class="navbar-brand" href="/cgi-bin/status.cgi"><img src="/img/logo.svg" width="116" height="32" alt=""></a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
      aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownInformation" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Information</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownInformation">
            <li><a class="dropdown-item" href="/cgi-bin/status.cgi">Information</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/dmesg.cgi">Diagnostic message</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/log.cgi">Log read</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/info/httpd.cgi">HTTPd environment</a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/updates.cgi">Updates</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownNetwork" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Network</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownNetwork">
            <li><a class="dropdown-item" href="/cgi-bin/network.cgi">Settings</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/network-ntp.cgi">NTP Settings</a></li>
          </ul>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" id="dropdownMajestic" href="#"
            role="button" data-bs-toggle="dropdown" aria-expanded="false">Majestic</a>
          <ul class="dropdown-menu" aria-labelledby="dropdownMajestic">
            <li><a class="dropdown-item" href="/cgi-bin/majestic.cgi">Settings</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-diff.cgi">Review Changes</a></li>
            <li><a class="dropdown-item text-danger confirm" href="/cgi-bin/majestic-reset.cgi">Restore Original</a></li>
            <li><a class="dropdown-item" href="/cgi-bin/majestic-download.cgi">Backup</a></li>
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/tools.cgi">Tools</a></li>
        <li class="nav-item"><a class="nav-link" href="/cgi-bin/preview.cgi">Preview</a></li>
      </ul>
    </div>
  </div>
</nav>
<main>
  <div class="container p-3">
