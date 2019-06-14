import datetime
from flask import render_template, redirect, request

from source_code import app
from source_code.clx_config import ConfigForm


@app.route("/")
def climatix_root():
    now = datetime.datetime.now()
    datetime_format = '%Y-%m-%d %H:%M:%S'
    formatted_datetime = now.strftime(datetime_format)
    return render_template("clx_root.html", timestamp=formatted_datetime)


@app.route("/config", methods=["GET", "POST"])
def configure_climatix():
    now = datetime.datetime.now()
    datetime_format = '%Y-%m-%d %H:%M:%S'
    formatted_datetime = now.strftime(datetime_format)
    config_form = ConfigForm()
    if config_form.validate_on_submit():
        valid_configuration = config_form.data.copy()
        valid_configuration.pop("csrf_token")
        return redirect("/monitor")
    return render_template("clx_config.html", config_form=ConfigForm(), timestamp=formatted_datetime)


@app.route("/monitoring", methods=["GET"])
def monitor_climatix():
    now = datetime.datetime.now()
    datetime_format = '%Y-%m-%d %H:%M:%S'
    formatted_datetime = now.strftime(datetime_format)
    return render_template("clx_monitor.html", timestamp=formatted_datetime)
