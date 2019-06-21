import datetime
import os
import requests
from flask import render_template, redirect, request

from source_code import app
from source_code.clx_config import ConfigForm


@app.route("/")
def climatix_root():
    now = datetime.datetime.now()
    datetime_format = '%Y-%m-%d %H:%M:%S'
    formatted_datetime = now.strftime(datetime_format)
    sync_file = open("1_datetime.txt", mode="w", encoding="UTF-8")
    sync_file.write(formatted_datetime)
    sync_file.close()
    return render_template("clx_root.html", timestamp=formatted_datetime)


@app.route("/config", methods=["GET", "POST"])
def configure_climatix():
    sync_file = open("1_datetime.txt", mode="r", encoding="UTF-8")
    formatted_datetime = sync_file.read()
    sync_file.close()
    config_form = ConfigForm()
    if config_form.validate_on_submit():
        valid_configuration = config_form.data.copy()
        valid_configuration.pop("csrf_token")
        conf_file = open("2_config.txt", mode="w", encoding="UTF-8")
        for key in valid_configuration.keys():
            conf_file.write(valid_configuration[key] + "\n")
        conf_file.close()
        return redirect("/monitor")
    return render_template("clx_config.html", config_form=ConfigForm(), timestamp=formatted_datetime)


@app.route("/monitor", methods=["GET"])
def monitor_climatix():
    sync_file = open("1_datetime.txt", mode="r", encoding="UTF-8")
    formatted_datetime = sync_file.read()
    sync_file.close()

    clx_configuration = {
        "ip_address": "",
        "user_name": "",
        "user_pass": "",
        "user_pin": "",
        "data_file": "",
        "comment": ""
    }
    conf_file = open("2_config.txt", mode="r", encoding="UTF-8")
    for key in clx_configuration.keys():
        clx_configuration[key] = conf_file.readline()
    conf_file.close()
    #clx_read = requests.request(GET, "192.168.10.101")
    return render_template("clx_monitor.html", timestamp=formatted_datetime, configuration=clx_configuration)
