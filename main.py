import os
import ndb_utils
from flask import Flask, render_template, redirect, flash
app = Flask(__name__)
app.secret_key = '9625403974088191.8326510132286338'


def development():
    if os.environ['SERVER_SOFTWARE'].find('Development') == 0 or os.environ['SERVER_NAME'].find('beta') == 0:
        return True
    else:
        return False


@app.route('/')
def welcome_page():
    return render_template("welcome.html", development=development())


@app.route('/schedule/')
@app.route('/schedule/<string:type>')
def temp_schedule(type=None):
    if type == None:
        flash("No schedule selected, please use one of the links.")
        return redirect("/")
    elif type not in ["a", "b"]:
        flash("Invald schedule selected, please use one of the links.")
        return redirect("/")
    return render_template("schedules/static-schedule.html", schedule_type=type)

@app.route('/api/seconds/')
def server_second_offset():
    return str(ndb_utils.getSecondOffset())

if __name__ == '__main__':
    app.run()