from flask import Flask, render_template, redirect, request, session, flash
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = "skdjfhwreiutyw9e8h"
successMsg = ""

# Email's regular expression
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Date regular expression
date_reg_exp = re.compile('\d{2}/\d{2}/\d{4}')


@app.route("/")
def index():

    dMsg = ""
    if "registered" in session and session["registered"]:
        dMsg = "Thanks for submitting your information."
        session.clear()

    return render_template("index.html", successMsg = dMsg)


@app.route("/register", methods=["post"])
def register():
    # Validate Not Blank
    if length(request.form["email"]) <= 0:
        reportError("Please enter a value for email!")
        return redirect("/")

    if length(request.form["firstname"]) <= 0:
        reportError("Please enter a value for First Name!")
        return redirect("/")

    if length(request.form["lastname"]) <= 0:
        reportError("Please enter a value for Last Name!")
        return redirect("/")

    if length(request.form["password"]) <= 0:
        reportError("Please enter a value for Password!")
        return redirect("/")

    if length(request.form["passconfirm"]) <= 0:
        reportError("Please enter a value for Password Confirm!")
        return redirect("/")

    if length(request.form["birthdate"]) <= 0:
        reportError("Please enter a value for Birthdate!")
        return redirect("/")

    # Validate Email
    if not email_regex.match(request.form['email']):
        reportError("Invalid Email Address!")
        return redirect("/")

    # Validate First name
    if not request.form["firstname"].isalpha():
        reportError("First name should contain alphabet only!")
        return redirect("/")

    # Validate Last name
    if not request.form["lastname"].isalpha():
        reportError("Last name should contain alphabet only!")
        return redirect("/")

    # Validate Password length
    if len(request.form["password"]) < 8:
        reportError("Password should have at least 8 characters!")
        return redirect("/")

    # Validate Password chars
    if not charCheckPassword(request.form["password"]):
        reportError("Password should contain at one uppercase, one lowercase, and one number!")
        return redirect("/")
    
    # Validate Match password
    if request.form["password"] != request.form["passconfirm"]:
        reportError("Password and it's confirm are not matching!")
        return redirect("/")

    # Validate Date
    if not date_reg_exp.match(request.form["birthdate"]):
        reportError("Birthdate is incorrect!")
        return redirect("/")

    try:
        brdate = datetime.strptime(request.form["birthdate"], '%m/%d/%Y')
    except:
        reportError("Birthdate is incorrect!")
        return redirect("/")

    if not dateValidate(brdate):
        reportError("Birthdate is can not be in the future!")
        return redirect("/")


    session["registered"] = True

    return redirect("/")


def dateValidate(ddate):
    print("#" * 40)
    print(ddate)
        
    tdate = datetime.now()
    print("#" * 40)
    print(tdate)

    if ddate > tdate:
        return False

    return True

def length(str):
    if len(str) == 0 or str.isspace():
        return 0
    
    bgn = 0
    end = len(str)

    for i in range(0, end):
        if str[i] == " ":
            bgn += 1

    for i in range(len(str) - 1, 0, -1):
        if str[i] == " ":
            end -= 1

    dlen = end - bgn + 1

    return dlen


def charCheckPassword(pwd):
    result = True
    upper = 0
    lower = 0
    number = 0

    for c in pwd:
        if c.isupper():
            upper += 1
        if c.islower():
            lower += 1
        if c.isnumeric():
            number += 1

    if upper == 0 or lower == 0 or number == 0:
        return False

    return result


def reportError(message):
    flash(message, "error")

    session["email"] = request.form["email"]
    session["firstname"] = request.form["firstname"]
    session["lastname"] = request.form["lastname"]
    session["birthdate"] = request.form["birthdate"]


if __name__ == "__main__":
    app.run(debug = True)