from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "BFB0DDE2B39686AB4492FACD0F362FB3C7F3424E38C15B0C871E206C969E0175"

from source_code import clx_views

app.run(debug=True)