from flask import Flask, jsonify, render_template, url_for, request, flash, redirect, session, make_response
import os, subprocess
from subprocess import Popen, PIPE, check_output
import csv
import io

path = os.getcwd()

app = Flask(__name__)

app.secret_key = "hello"


@app.route("/chisq_ind_query", methods = ["GET", "POST"])
def chisq_ind_query():
	if request.method == "POST":
		var1 = request.form["var1"]
		var2 = request.form["var2"]
		session["var1"] = var1
		session["var2"] = var2
		flash("Variables selected.")
		return redirect(url_for("command_server2", command=command_server2))
	else:
		return render_template("chisq_ind_query.html")

@app.route("/chisq_good_query", methods = ["GET", "POST"])
def chisq_good_query():
	if request.method == "POST":
		var1 = request.form["var1"]
		var2 = request.form["var2"]
		session["var1"] = var1
		session["var2"] = var2
		flash("Variables selected.")
		return redirect(url_for("command_server3", command=command_server3))
	else:
		return render_template("chisq_good_query.html")



@app.route("/chisq_ind")
def chisq_ind():
	return redirect(url_for("chisq_ind_query"))



@app.route("/test")
def test():
	user_input = 5
	print(user_input)
	return jsonify(5)




def run_command(command):
	return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE).stdout.read()




@app.route("/command2/<command>")
def command_server2(command):
	return run_command("python " + path + "/chisq_ind.py " + session["var1"] + " " + session["var2"])
	# if os.path.isfile("result.txt") == False:
	# 	f = open("result.txt", "w+")
	# 	f.close()
	# with open(path + "/result.txt", "r") as file:
	# 	content = file.read()
	# return render_template("result.html", content = content)

@app.route("/command3/<command>")
def command_server3(command):
	return run_command("python " + path + "/chisq_ind.py " + session["var1"] + " " + session["var2"])
	# if os.path.isfile("result.txt") == False:
	# 	f = open("result.txt", "w+")
	# 	f.close()
	# with open(path + "/result.txt", "r") as file:
	# 	content = file.read()
	# return render_template("result.html", content = content)

@app.route("/command4/<command>")
def command_server4(command):
	run_command("python " + path + "/laud/heatmap_df.py")

@app.route("/command5/<command>")
def command_server5(command):
	run_command("Rscript " + path + "/laud/heatmap.R" + session["meth"])


# @app.route("/", methods = ["GET", "POST"])
# def home():
# 	session.pop("r", None)
# 	session.pop("python", None)
# 	if request.method == "POST":
# 		if "I like R!" in request.form["form"]:
# 			session["r"] = request.form["form"]
# 			return redirect(url_for("command_server1", command=command_server1))
# 		elif "I like python!" in request.form["form"]:
# 			session["python"] = request.form["form"]
# 			return redirect(url_for("command_server0", command=command_server0))
# 	return render_template("home.html")



# @app.route("/command0/<command>")
# def command_server0(command):
# 	return run_command("python " + path + "/script.py " + "python")

# @app.route("/command1/<command>")
# def command_server1(command):
# 	return run_command("Rscript " + path + "/script.R " + "R")



if __name__ == "__main__":
	app.run(debug = True)
