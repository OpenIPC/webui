#!/usr/bin/haserl
Content-Type: text/html; charset=UTF-8
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")

<!DOCTYPE html>
<html lang="<%= $locale %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title "$page_title" %></title>
<link rel="stylesheet" href="/a/bootstrap.css">
<link rel="stylesheet" href="/a/bootstrap.override.css">
<script src="/a/bootstrap.js"></script>
<script src="/a/main.js"></script>
</head>
<body id="top">
<%in p/nav-main.cgi %>
<div class="bg-light text-end x-small p-2">
<div class="container"><% signature %></div>
</div>
<main>
<div class="container">
<h2><%= $page_title %></h2>
<% flash_read %>
