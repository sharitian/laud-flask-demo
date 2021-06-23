from flask import Flask, render_template, url_for, request, flash, redirect, session, make_response
from flask_mysqldb import MySQL
import os, subprocess
from subprocess import Popen, PIPE, check_output
import yaml
import chisq
import csv
import io
import pandas as pd

path = os.getcwd()

app = Flask(__name__)

app.secret_key = "hello"

db = yaml.load(open("db.yaml"))
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]

mysql = MySQL(app)


@app.route("/")
def home():
	return render_template("home.html")


@app.route("/view", methods = ["GET", "POST"])
def view():
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT * FROM diamonds1")
	if resultValue > 0:
		field_names = [i[0] for i in cur.description]
		diamondDetails = cur.fetchall()
		return render_template("view.html", diamondDetails = diamondDetails, field_names = field_names)
	

# @app.route("/export")
# def export():
# 	si = io.StringIO()
# 	cw = csv.writer(si)
# 	cur = mysql.connection.cursor()
# 	cur.execute("SELECT * FROM diamonds1")
# 	rows = cur.fetchall()
# 	cw.writerow([i[0] for i in cur.description])
# 	cw.writerows(rows)
# 	response = make_response(si.getvalue())
# 	response.headers["Content-Disposition"] = "attachment; filename = report.csv"
# 	response.headers["Content-type"] = "text/csv"
# 	return response


@app.route("/export")
def export():
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT * FROM diamonds1")
	if resultValue > 0:
		field_names = [i[0] for i in cur.description]
		diamondDetails = cur.fetchall()
		df = pd.DataFrame(diamondDetails, columns = field_names)
		df.to_csv(os.getcwd() + "/report.csv", index = False)
		return redirect(url_for("view"))


@app.route("/query", methods = ["GET", "POST"])
def query():
	if request.method == "POST":
		cat1 = request.form["cat1"]
		cat2 = request.form["cat2"]
		session["cat1"] = cat1
		session["cat2"] = cat2
		flash("Categories selected.")
		return redirect(url_for("table"))
	else:
		return render_template("query.html")
		

@app.route("/chi", methods = ["GET", "POST"])
def chi():
	if request.method == "POST":
		if "cat1" in session and "cat2" in session:
			return redirect(url_for("command_server0", command=command_server0))
		else:
			return redirect(url_for("query"))
	else:
		if os.path.isfile("./report.csv"):
			return render_template("chi.html")
		else:
			return redirect(url_for("export"))



@app.route("/table")
def table():
	cat1 = session["cat1"] 
	cat2 = session["cat2"] 
	cur = mysql.connection.cursor()
	query = "SELECT " + cat1 + ", " + cat2 + " FROM diamonds1" 
	resultValue = cur.execute(query)
	if resultValue > 0:
		field_names = [i[0] for i in cur.description]
		cont_table = cur.fetchall()
		return render_template("table.html", cont_table = cont_table, field_names = field_names)



@app.route("/scat", methods = ["GET", "POST"])
def scat():
	if request.method == "POST":
		if "cat1" in session and "cat2" in session:
			return redirect(url_for("command_server1", command=command_server1))
		else:
			return redirect(url_for("query"))
	else:
		if os.path.isfile("./report.csv"):
			return render_template("scat.html")
		else:
			return redirect(url_for("export"))


@app.route("/clear")
def clear():
	session.pop("cat1", None)
	session.pop("cat2", None)
	if os.path.isfile("./report.csv"):
		os.remove(os.getcwd() + "/report.csv")
	return redirect(url_for("home"))


def run_command(command):
	return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE).stdout.read()


@app.route("/command0/<command>")
def command_server0(command):
	return run_command("python " + path + "/chisq.py " + session["cat1"] + " " + session["cat2"])

@app.route("/command1/<command>")
def command_server1(command):
	return run_command("Rscript " + path + "/visualize.R " + session["cat1"] + " " + session["cat2"])


if __name__ == "__main__":
	app.run(debug = True)

