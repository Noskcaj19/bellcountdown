import os
import ndb_utils
from flask import Flask, render_template, redirect, request, flash
app = Flask(__name__)
app.secret_key = '9625403974088191.8326510132286338'

def development():
	if os.environ['SERVER_SOFTWARE'].find('Development') == 0 or os.environ['SERVER_NAME'].find('beta') == 0:
		return True
	else:
		return False

# Routing v1 users
@app.route('/s', defaults={'path': ''})
@app.route('/s/<path:path>')
def catch_all_old_url(path):
	flash("", "redirect")
	return redirect("/", 301)

@app.route('/')
def welcome_page():
	return render_template("welcome.html", development=development())

@app.route('/schedule/')
@app.route('/schedule/<string:type>/')
def static_schedule(type=None):
	if type == None:
		flash("No schedule selected, please use one of the links.")
		return redirect("/")
	elif type not in ["a", "b"]:
		flash("Invald schedule selected, please use one of the links.")
		return redirect("/")
	return render_template("schedules/static-schedule.html", schedule_type=type)

@app.route('/schedule/<string:type>/spin/')
def static_spining_schedule(type=None):
	if type == None:
		flash("No schedule selected, please use one of the links.")
		return redirect("/")
	elif type not in ["a", "b"]:
		flash("Invald schedule selected, please use one of the links.")
		return redirect("/")
	return render_template("schedules/static_spining-schedule.html", schedule_type=type)

@app.route('/api/seconds/')
def server_second_offset():
	return str(ndb_utils.getSecondOffset())

@app.route('/api/setSeconds/', methods=["POST"])
def set_server_second_offset():
	new_seconds = request.form.get("newSeconds", "")
	credentials = request.form.get("credentials", None)

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

if __name__ == '__main__':
	app.run()
