from flask import Flask, render_template
app = Flask(__name__)
import os
def development():
    if os.environ['SERVER_SOFTWARE'].find('Development') == 0 or os.environ['SERVER_NAME'].find('beta') == 0:
        return True
    else:
        return False

@app.route('/')
def hello_world():
    return render_template("welcome.html", development=development())

if __name__ == '__main__':
    app.run()