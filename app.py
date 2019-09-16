from bokeh.embed import components
from bokeh.io import curdoc
from flask import Flask, render_template
from datetime import datetime
from MapCreator import MapCreator
app = Flask(__name__)

@app.route('/')
def homepage():
    map_creator = MapCreator()

    layout = map_creator.colony_loss_map()
    script, div = components(layout)
    # the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return render_template('home.html', script=script, div=div)
    #
    # return """
    # <h1>Hello heroku</h1>
    # <p>It is currently {time}.</p>
    #
    # <img src="http://loremflickr.com/600/400">
    # """.format(time=the_time)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

