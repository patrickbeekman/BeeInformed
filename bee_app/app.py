from flask import Flask, render_template

from bokeh.client import pull_session
from bokeh.embed import server_session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def app_page():
    return render_template("page.html")


if __name__ == "__main__":
    app.run(debug=True)
