#!/usr/bin/haserl --upload-limit=200 --upload-dir=/tmp
<%in _common.cgi %>
<%
page_title="$tPageTitleSensor"

if [ "POST" = "$REQUEST_METHOD" ]; then
  error=""

  if [ -n "$POST_sensor_driver_file" ]; then
    type="driver"
    magicnum="7f454c460101"
    file="$POST_sensor_driver_file"
    file_name="$POST_sensor_driver_file_name"
    file_path="$POST_sensor_driver_file_path"
    if [ -z "$file_name" ]; then
      error="$tMsgNoUploadedFileFound"
    elif [ "$magicnum" != $(xxd -p -l 6 $file) ]; then
      error="$tMsgUploadedFileHasWrongMagic"
    elif [ -f "/usr/lib/sensors/${file_name}" ]; then
      error="$tMsgFileExists"
    fi
  fi

  if [ -n "$POST_sensor_config_file" ]; then
    type="config"
    file="$POST_sensor_config_file"
    file_name="$POST_sensor_config_file_name"
    file_path="$POST_sensor_config_file_path"
    if [ -z "$file_name" ]; then
      error="$tMsgNoUploadedFileFound"
    elif [ -n $(grep "\[sensor\]" $file) ]; then
      error="$tMsgUploadedFileHasWrongMagic"
    elif [ -f "/etc/sensors/${file_name}" ]; then
      error="$tMsgFileExists"
    fi
  fi

  if [ -z "$error" ]; then
    case "$type" in
    driver)
      mv "$file_path" "/usr/lib/sensors/${file_name}"
      flash_save "success" "Sensor driver ${file_name} uploaded."
      redirect_to "/cgi-bin/sensor-upload.cgi"
      ;;
    config)
      mv "$file_path" "/etc/sensors/${file_name}"
      flash_save "success" "Sensor config ${file_name} uploaded."
      redirect_to "/cgi-bin/sensor-upload.cgi"
      ;;
    esac
  fi
fi
%>
<%in _header.cgi %>
<%
[ -n "$error" ] && report_error "$error"

row_ "row-cols-1 row-cols-lg-2 g-4 mb-4"
  col_card_ "$tHeaderSensorDrivers"
    alert_ "light"
      h6 "Upload sensor driver"
      form_ "/cgi-bin/sensor-upload.cgi" "post" "enctype=\"multipart/form-data\""
        field_file "sensor_driver_file"
        button_submit "$tButtonUploadFile" "primary"
      _form
    _alert
    ex "ls /usr/lib/sensors/"
  _col_card

  col_card_ "$tHeaderSensorConfigs"
    alert_ "light"
      h6 "Upload sensor config"
      form_ "/cgi-bin/sensor-upload.cgi" "post" "enctype=\"multipart/form-data\""
        field_file "sensor_config_file"
        button_submit "$tButtonUploadFile" "primary"
      _form
    _alert
    ex "ls /etc/sensors/"
  _col_card
_row
%>
<%in _footer.cgi %>
