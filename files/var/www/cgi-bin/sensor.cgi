#!/usr/bin/haserl --upload-limit=200 --upload-dir=/tmp
<%in p/common.cgi %>
<%
page_title="Sensor Driver and Config"

if [ "POST" = "$REQUEST_METHOD" ]; then
	error=""

	if [ -n "$POST_sensor_driver_file" ]; then
		type="driver"
		file="$POST_sensor_driver_file"
		file_name="$POST_sensor_driver_file_name"
		file_path="$POST_sensor_driver_file_path"

		if [ -z "$file_name" ]; then
			error="No file found! Did you forget to upload?"
		elif [ "hisilicon" = "$soc_vendor" ] && [ "7f454c460101" != $(xxd -p -l 6 $file) ]; then
			error="File magic number does not match. Did you upload a wrong file?"
		elif [ -f "/usr/lib/sensors/${file_name}" ]; then
			error="File already exists!"
		fi
	fi

	if [ -n "$POST_sensor_config_file" ]; then
		type="config"
		file="$POST_sensor_config_file"
		file_name="$POST_sensor_config_file_name"
		file_path="$POST_sensor_config_file_path"

		if [ -z "$file_name" ]; then
			error="No file found! Did you forget to upload?"
		elif [ "hisilicon" = "$soc_vendor" ] && [ -n $(grep "\[sensor\]" $file) ]; then
			error="File magic number does not match. Did you upload a wrong file?"
		elif [ -f "/etc/sensors/${file_name}" ]; then
			error="File already exists!"
		fi
	fi

	if [ -z "$error" ]; then
		case "$type" in
			driver)
				mv "$file_path" "/usr/lib/sensors/${file_name}"
				redirect_to $SCRIPT_NAME "success" "Sensor driver uploaded."
				;;
			config)
				mv "$file_path" "/etc/sensors/${file_name}"
				redirect_to $SCRIPT_NAME "success" "Sensor config uploaded."
				;;
		esac
	fi
fi
%>
<%in p/header.cgi %>

<% [ -n "$error" ] && report_error "$error" %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Sensor Drivers</h3>
    <% ex "ls /usr/lib/sensors/" %>
  </div>
  <div class="col">
    <h3>Upload sensor driver</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_file "sensor_driver_file" "Sensor driver file" %>
      <% button_submit "Upload file" %>
    </form>
  </div>
  <div class="col">
    <h3>Sensor Configs</h3>
    <% ex "ls /etc/sensors/" %>
  </div>
  <div class="col">
    <h3>Upload sensor config</h3>
    <form action="<%= $SCRIPT_NAME %>" method="post" enctype="multipart/form-data">
      <% field_file "sensor_config_file" "Sensor config file" %>
      <% button_submit "Upload file" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
