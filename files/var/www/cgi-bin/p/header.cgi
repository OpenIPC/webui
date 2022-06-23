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
<p class="text-end x-small"><span class="container"><% signature %></span></p>
<main>
<div class="container">
<h2><%= $page_title %></h2>
<% flash_read %>
