from flask import Flask, jsonify
import services.tailscale as ts


import os

app = Flask(__name__)


@app.route('/')
def index():
    return "imagine making a website."

@app.route("/devices")
def devices():
    devices = ts.get_devices()
    
    # who needs templates when you've got mad fucking skills?
    response = ""

    for device in devices:
        response+=("<span>")
        response+=(device.render())
        response+=("</span><br>")

    return response

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv("PORT", default=5001))
