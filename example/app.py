from flask import Flask, render_template
from flaskext.embedly import Embedly

app = Flask(__name__)
app.secret_key = 'foobar'
e = Embedly(app)

@app.route('/')
def sample():
    return render_template('sample.html', url = "http://vimeo.com/9503416")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
