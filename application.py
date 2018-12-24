# Chad Shirts Bot
# Matt Kristoffersen
# CPSC 100 Final Project, FALL 2018
# December 4, 2018

import os
import math
import requests
import selenium
import time
import smtplib

import bs4 as bs
import urllib.request
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from seleniumrequests import Chrome

from helpers import apology, login_required, sendemail, validate

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///info.db")


@app.route("/")
@login_required
def index():
    rows = db.execute("SELECT * FROM information WHERE id = :id", id=session.get("user_id"))
    if not rows:
        return render_template("enter.html")

    return redirect("/buy")


@app.route("/enter", methods=["POST"])
@login_required
def enter():
    try:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        tel = request.form.get("tel")
        address = request.form.get("address")
        zip = request.form.get("zip")
        city = request.form.get("city")
        state = request.form.get("state")
        ccnum = request.form.get("ccnum")
        expdatemonth = request.form.get("expdatemonth")
        expdateyear = request.form.get("expdateyear")
        cvv = request.form.get("cvv")
    except:
        return apology("You didn't fill out part of the form!", 400)

    # Validate the credit card number
    x = validate(ccnum)
    if x is False:
        return apology("Invalid credit card number", 400)

    db.execute("INSERT INTO information VALUES(:id, :firstname, :lastname, :email, :tel, :address, :zip, :city, :state, :ccnum, :expdatemonth, :expdateyear, :cvv)", id=session.get(
               "user_id"), firstname=firstname, lastname=lastname, email=email, tel=tel, address=address, zip=zip, city=city, state=state, ccnum=ccnum, expdatemonth=expdatemonth, expdateyear=expdateyear, cvv=cvv)

    # Send email
    sendemail(email, "You have registered for the ChadShirts bot!")

    return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # Query database for username
    rows = db.execute("SELECT username FROM users")
    if not rows:
        return jsonify(True)
    username_from_register = request.args.get("username")
    for username in range(len(rows)):
        database_username = rows[username]['username']
        if username_from_register == database_username:
            return jsonify(False)

    return jsonify(True)


@app.route("/userinfo", methods=["GET"])
@login_required
def info():
    cust_info = db.execute("SELECT * FROM information WHERE id = :id", id=session.get("user_id"))

    # This part censors the ccnum so that malicious entities can't steal your identity.
    s = list(cust_info[0]["ccnum"])
    for i in range(len(s) - 4):
        s[i] = "*"
    s = "".join(s)
    cust_info[0]["ccnum"] = s
    info = cust_info[0]
    return render_template("information.html", info=info)


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if request.method == "GET":
        return render_template("enter.html")

    else:
        try:
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            tel = request.form.get("tel")
            address = request.form.get("address")
            zip = request.form.get("zip")
            city = request.form.get("city")
            state = request.form.get("state")
            country = request.form.get("country")
            ccnum = request.form.get("ccnum")
            expdatemonth = request.form.get("expdatemonth")
            expdateyear = request.form.get("expdateyear")
            cvv = request.form.get("cvv")
        except:
            return apology("You didn't fill out part of the form!", 400)

        # Validate the credit card number (just because :))
        x = validate(ccnum)
        if x is False:
            return apology("Invalid credit card number", 400)

        db.execute("UPDATE information SET firstname = :firstname, lastname = :lastname, email = :email, telephone=:tel, address=:address, zip=:zip, city=:city, state=:state, ccnum=:ccnum, expdatemonth=:expdatemonth, expdateyear=:expdateyear, cvv=:cvv WHERE id=:id",
                   id=session.get("user_id"), firstname=firstname, lastname=lastname, email=email, tel=tel, address=address, zip=zip, city=city, state=state, ccnum=ccnum, expdatemonth=expdatemonth, expdateyear=expdateyear, cvv=cvv)

        # Send email
        sendemail(email, "You have successfully updated your information!")

        return redirect("/userinfo")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    # https://stackoverflow.com/questions/41895651/python-beautifulsoup-how-to-extract-find
    url = 'https://shirtsbychad.bigcartel.com/product/negative-chad-shirt'
    if request.method == "GET":
        page = requests.get(url)
        soup = bs.BeautifulSoup(page.text, "html.parser")

        # Grabs the right image from the chadshirts website.
        images = []
        for img in soup.find_all('img'):
            images.append(img.get('src'))
        image = images[1]
        name = soup.find('h1').text

        try:
            price = soup.find('h3').text
        except:
            price = "Not available yet!"

        return render_template("buy.html", image=image, name=name, price=price)

    if request.method == "POST":

        # Grabs size from the form on buy.html.
        size = request.form.get("size")

        # This is all selenium stuff. Chrome was hard to work with because of the chromedriver, but I got it to work!
        # Primes Headless Chrome for our diabolical deeds.
        chrome_options = Options()
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

        # Orients Headless Chrome toward the correct website.
        driver = webdriver.Chrome(options=chrome_options, executable_path='/Users/mattkristoffersen/Downloads/project/chromedriver')
        driver.get(url)

        # https://stackoverflow.com/questions/7867537/selenium-python-drop-down-menu-option-value
        selection = Select(driver.find_element_by_id("option"))
        selection.select_by_visible_text(size)
        driver.get_screenshot_as_file("1.png")

        # purchase
        try:
            submit_button = driver.find_elements_by_xpath('//*[@id="product-addtocart"]')[0]
            submit_button.click()
        except:
            return apology("Not available", 400)

        driver.get_screenshot_as_file("2.png")

        # Checkout
        time.sleep(2)
        submit_button = driver.find_elements_by_xpath('//*[@id="checkout-btn"]')[0]
        submit_button.click()
        time.sleep(.5)
        driver.get_screenshot_as_file("3.png")

        # enter information
        cust_info = db.execute("SELECT * FROM information WHERE id = :id", id=session.get("user_id"))
        info = cust_info[0]
        try:
            inputElement = driver.find_element_by_id("buyer_first_name")
            inputElement.send_keys(info["firstname"])
            inputElement = driver.find_element_by_id("buyer_last_name")
            inputElement.send_keys(info["lastname"])
            inputElement = driver.find_element_by_id("buyer_email")
            inputElement.send_keys(info["email"])
            driver.get_screenshot_as_file("4.png")

            # Click submit!
            submit_button = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[1]/div/form/div[4]')
            submit_button.click()
            time.sleep(2)
            driver.get_screenshot_as_file("5.png")

        except:
            return apology("Error entering customer information", 400)

        # more information
        try:
            inputElement = driver.find_element_by_id("shipping_address_1")
            inputElement.send_keys(info["address"])
            inputElement = driver.find_element_by_name("shipping_city")
            inputElement.send_keys(info["city"])
            selection = Select(driver.find_element_by_name("shipping_state"))
            selection.select_by_visible_text(info["state"])
            inputElement = driver.find_element_by_name("shipping_zip")
            inputElement.send_keys(info["zip"])
            driver.get_screenshot_as_file("6.png")
            submit_button = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[2]/div/form/div[5]')
            submit_button.click()
            time.sleep(2)
        except:
            return apology("Error entering shipping information", 400)

        # more information
        # I got through the stripe anti-bot stuff thanks to https://stackoverflow.com/questions/48805576/using-selenium-webdriver-to-interact-with-stripe-card-element-iframe-cucumber
        try:
            driver.switch_to.frame(driver.find_element_by_xpath('//iframe[@name="__privateStripeFrame3"]'))
            inputElement = driver.find_element_by_name("cardnumber")
            inputElement.send_keys(info["ccnum"])
            driver.get_screenshot_as_file("checkout4.png")
            time.sleep(.5)
            inputElement.send_keys("1" + info["expdatemonth"] + info["expdateyear"] + info["cvv"])
            driver.get_screenshot_as_file("7.png")
            driver.switch_to.default_content()
            submit_button = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[3]/div/form/div[3]')
            submit_button.click()
        except:
            return apology("Error entering credit card information", 400)

        # These sleeps are for bigcartel to verify the information. If I were to not have these then headlesschrome would click at nothing.
        time.sleep(2)
        driver.get_screenshot_as_file("8.png")

        # Pay now!
        try:
            submit_button = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div[4]/div/form/div[2]/span/button')
            submit_button.click()

        except:
            return apology("Something went wrong! Don't worry, I didn't buy anything.", 400)
        time.sleep(.5)
        driver.get_screenshot_as_file("9.png")

        # send email!
        sendemail(info["email"], "The bot has done its job! Check 9.png to see if it worked!")

        return render_template("success.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (filled out the form)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation must match", 400)

        # Hash password
        hash = generate_password_hash(request.form.get("password"))

        # Place username and hashed password into database.
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash)
        if not result:
            return apology("That username already exists", 400)

        # Log in
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # Through GET (by pressing the top button)
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
