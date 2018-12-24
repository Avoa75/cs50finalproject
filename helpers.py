import requests
import urllib.parse
import smtplib

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def sendemail(email, message):
    # Send an email
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login('chadshirtsbot@gmail.com', 'test123456!')
    try:
        smtpserver.sendmail(
          "chadshirtsbot@gmail.com", 
          email, 
          message)
    except:
        return apology("Error sending email", 400)
    smtpserver.quit()
    
    return True

def validate(ccnum):
    # http://code.activestate.com/recipes/172845-python-luhn-checksum-for-credit-card-validation/
    sum = 0
    num_digits = len(ccnum)
    oddeven = num_digits & 1

    for count in range(0, num_digits):
        digit = int(ccnum[count])

        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum = sum + digit

    if (sum % 10) is 0:
        return True

    else:
        return False
