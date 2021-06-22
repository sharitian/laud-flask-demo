from flask import Flask, render_template, url_for, request, flash, redirect, session
from flask_mysqldb import MySQL
import yaml
import chisq


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


@app.route("/view")
def view():
	cur = mysql.connection.cursor()
	resultValue = cur.execute("SELECT * FROM diamonds1")
	if resultValue > 0:
		field_names = [i[0] for i in cur.description]
		diamondDetails = cur.fetchall()
		return render_template("view.html", diamondDetails = diamondDetails, field_names = field_names)


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
		return redirect(url_for("result"))
	else:
		return render_template("chi.html")


@app.route("/table")
def table():
	cat1 = session["cat1"] 
	cat2 = session["cat2"] 
	cur = mysql.connection.cursor()
	query = "SELECT " + cat1 + ", " + cat2 + ", " + "count(*) as count FROM diamonds1 GROUP BY " + cat1 + ", " + cat2 + " ORDER BY " +  cat1
	resultValue = cur.execute(query)
	if resultValue > 0:
		field_names = [i[0] for i in cur.description]
		cont_table = cur.fetchall()
		return render_template("table.html", cont_table = cont_table, field_names = field_names)


@app.route("/result")
def result():
	if "cat1" in session and "cat2" in session:
		cat1 = session["cat1"] 
		cat2 = session["cat2"] 
		return chisq.chi_sq(cat1, cat2)
	else:
		return redirect(url_for("query"))

@app.route("/clear")
def clear():
	session.pop("cat1", None)
	session.pop("cat2", None)
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug = True)

