import ndb_utils
import os.path
from datetime import date, timedelta
from flask import Flask, render_template, redirect, request, flash
app = Flask(__name__)
app.secret_key = '9625403974088191.8326510132286338'

# Routing v1 users
@app.route('/update-redirect/')
def update_redirect():
	return render_template("redirect.html")

@app.route('/s/', defaults={'path': ''})
@app.route('/s/<path:path>')
def catch_all_old_url(path):
	return redirect("/update-redirect/", 301)

@app.route('/')
def welcome_page():
	return render_template("welcome.html", second_offset=ndb_utils.getSecondOffset())

@app.route('/schedule/')
@app.route('/schedule/<string:type>/')
def static_schedule(type=None):
	if type == None:
		flash("No schedule selected, please use one of the links.", "error")
		return redirect("/")
	elif type not in ["a", "b"]:
		flash("Invald schedule selected, please use one of the links.", "error")
		return redirect("/")
	return render_template("schedules/static-schedule.html", schedule_type=type)

@app.route('/schedule/<string:type>/spin/')
def static_spining_schedule(type=None):
	if type == None:
		flash("No schedule selected, please use one of the links.", "error")
		return redirect('/')
	elif type not in ['a', 'b']:
		flash("Invald schedule selected, please use one of the links.", "error")
		return redirect('/')
	return render_template("schedules/static_spining-schedule.html", schedule_type=type)

@app.route('/api/seconds/')
def server_second_offset():
	return str(ndb_utils.getSecondOffset())

@app.route('/api/setSeconds/', methods=["POST"])
def set_server_second_offset():
	new_seconds = request.form.get('newSeconds', "")
	credentials = request.form.get('credentials', None)

	if new_seconds == "":
		return "Missing form field", 400

	path = os.path.join(os.path.split(__file__)[0], 'auth-credentials.passwd')
	with open(path) as auth_file:
		correct_passwd = auth_file.read()
	if credentials == None:
		return "No Credentials", 401
	if credentials != correct_passwd:
		return "Unauthorized", 403

	ndb_utils.set_second_offset(float(new_seconds))
	return "Success", 200

@app.route('/api/days_remaining/')
def days_left():
	today = date.today()
	target = date(2018, 5, 31)
	dates = [today + timedelta(x + 1) for x in range((target - today).days)]
	weekdays = sum(1 for day in dates if day.weekday() < 5)
	return str(weekdays)

if __name__ == '__main__':
	app.run()
