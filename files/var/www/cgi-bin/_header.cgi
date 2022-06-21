#!/usr/bin/haserl
Content-Type: text/html; charset=UTF-8
Date: $(TZ=GMT date +"%a, %d %b %Y %T %Z")

<!DOCTYPE html>
<html lang="<%= $locale %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title "$page_title" %></title>
<%
link_css "/a/bootstrap.css"
link_css "/a/bootstrap.override.css"
[ "$HTTP_MODE" = "development" ] && link_css "/a/debug.css"
link_js "/a/bootstrap.js"
link_js "/a/main.js"
%>
</head>
<body id="top">
<% render "nav-main" %>
<div class="bg-light text-end x-small p-2">
<div class="container"><% signature %></div>
</div>
<main>
<div class="container">
<h2><%= $page_title %></h2>
<% flash_read %>
