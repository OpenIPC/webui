#!/usr/bin/haserl --upload-limit=200 --upload-dir=/tmp
<%in _common.cgi %>
<%
page_title="$t_sensor_0"

if [ "POST" = "$REQUEST_METHOD" ]; then
  error=""

  if [ -n "$POST_sensor_driver_file" ]; then
    type="driver"
    magicnum="7f454c460101"
    file="$POST_sensor_driver_file"
    file_name="$POST_sensor_driver_file_name"
    file_path="$POST_sensor_driver_file_path"

    if [ -z "$file_name" ]; then
      error="$t_form_error_1"
    elif [ "$magicnum" != $(xxd -p -l 6 $file) ]; then
      error="$t_form_error_4"
    elif [ -f "/usr/lib/sensors/${file_name}" ]; then
      error="$t_form_error_9"
    fi
  fi

  if [ -n "$POST_sensor_config_file" ]; then
    type="config"
    file="$POST_sensor_config_file"
    file_name="$POST_sensor_config_file_name"
    file_path="$POST_sensor_config_file_path"
    if [ -z "$file_name" ]; then
      error="$t_form_error_1"
    elif [ -n $(grep "\[sensor\]" $file) ]; then
      error="$t_form_error_4"
    elif [ -f "/etc/sensors/${file_name}" ]; then
      error="$t_form_error_9"
    fi
  fi

  if [ -z "$error" ]; then
    case "$type" in
    driver)
      mv "$file_path" "/usr/lib/sensors/${file_name}"
      flash_save "success" "$t_sensor_1"
      redirect_to "/cgi-bin/sensor-upload.cgi"
      ;;
    config)
      mv "$file_path" "/etc/sensors/${file_name}"
      flash_save "success" "$t_sensor_2"
      redirect_to "/cgi-bin/sensor-upload.cgi"
      ;;
    esac
  fi
fi
%>
<%in _header.cgi %>
<%
[ -n "$error" ] && report_error "$error"

row_ "row-cols-1 row-cols-lg-2 g-3 mb-3"
  col_card_ "$t_sensor_3"
    alert_ "light"
      h6 "$t_sensor_4"
      form_upload_ "/cgi-bin/sensor-upload.cgi"
        field_file "sensor_driver_file"
        button_submit "$t_sensor_5" "primary"
      _form
    _alert
    ex "ls /usr/lib/sensors/"
  _col_card

  col_card_ "$t_sensor_6"
    alert_ "light"
      h6 "$t_sensor_7"
      form_upload_ "/cgi-bin/sensor-upload.cgi"
        field_file "sensor_config_file"
        button_submit "$t_sensor_8" "primary"
      _form
    _alert
    ex "ls /etc/sensors/"
  _col_card
_row
%>
<%in p/footer.cgi %>
