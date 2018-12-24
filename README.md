# Chad Shirts!

Hello, my name is Matt Kristoffersen and this is my user manual for the Chad Shirts bot that I created for my CS50 Final Project. I'm super proud of this, and I hope you are too!

Before I get started, I need to say some thank-yous:

* Sean Walker & Natalie Schultz-Henry for being super awesome TAs. They really, really helped me get through the PSets. And, also, their comments on my PSets gave me confidence in my abilities that I really needed.
* Jonathan & Lulu from my section. They made me laugh a lot :)
* Teagan, Josh, Kelli, Uriel, and Chris from Harvard for making my hackathon experience fantastic. I knew like almost no one going and they made me feel so welcome and happy.
* Alex Kristoffersen, my amazing brother, for helping me with Python and encouraging me to try to make a Chad Shirts bot to begin with. Thanks, Bubba, I miss you! He's an EECS major at UC Berkeley :) (have to brag about my brother, sorry)
* The Beatles, Lil Uzi Vert, and Godspeed You! Black Emperor for providing good coding music.

That's it. Enough for the sentimentality, let's get started.

# What did I make?

Excellent question!

Essentially, I used the skeleton of Finance to create a web app through which users can log in, enter information, and purchase a Chad Shirt tee at the press of a button. Upon entering information, the user will receive an automated email, and upon purchase success, the user will receive another email. 

[Chad Shirts](https://shirtsbychad.bigcartel.com/) is a t-shirt brand that my friend from back home Chad Ryan made. They are essentially blank t-shirts with the word **CHAD** written across the front. I think they're really cool! Catch me rocking one at the fair.

# Getting Started

This bot will not work in the CS50 IDE because of the sheer amount of modules that the user needs to download in order for the code to work. I had some problems with permissions when installing BeautifulSoup and Selenium on the IDE as well as getting Chromedriver to work--the project went so much smoother once I migrated it all to my computer. That being said, some assets (Chrome Driver and Google Chrome) are dependent on my own computer path, so I recommend changing said paths to work with the user's machine.

Here are the modules that the user needs to run my project:
* requests
* selenium
* smtplib
* bs4
* cs50
* flask
* flask_session
* tempfile
* werkzeug
* seleniumrequests
* functools
* urllib
* time

To install these modules, enter this command from your terminal of choice:

~~~
pip3 install X
~~~
Where X is the module of choice. 

**IMPORTANT NOTE**: This project will only work with Mac OSX machines. If you would like to run this on a Windows or Linux computer, then you must download your respective [chromedriver](http://chromedriver.chromium.org/) for your system and replace the one already in the /project/ folder. Also, you must change the Google Chrome.app path in application.py to whatever your Google Chrome app is. I do not recommend changing anything and instead highly recommend switching to an OSX computer.

**SECOND IMPORTANT NOTE:** This project uses ChromeDriver in order to run Chrome autonomously. This project will only work with Chrome. Please use Chrome.

**THIRD IMPORTANT NOTE:** If terminal is giving an error that pip3 is not a valid command, please install it. [Here's how](https://stackoverflow.com/a/47004414).

In general, if terminal sends an error about not having a certain module, install it to get rid of the error.

Once you have configured application.py to work with your system and have installed all necessary modules, you may continue!

# How to run my project

In your terminal of choice, enter the following commands: 

~~~
$ cd [project folder]
$ FLASK_APP=application.py flask run
~~~
If you did it right, the web app should be online. Copy the address from the terminal and paste it into a new Chrome browser tab. Press enter. You should be at the webapp! Isn't it nice?

# How to buy a shirt

Once you have arrived at the homepage, you should log in. If you do not have an account, press **Register** at the top-right of your screen. Follow the textboxes and press the button.

If this is a new account, you will arrive at the page where you enter information. If you have already entered information, you'll be directed straight to the buy Chad Shirts page. Enter your information. Make sure that your information is valid! My program validates the credit card number you enter, so make sure that is valid as well. 

**SECURITY NOTE:** You will have to enter a credit card number to proceed. This number is only stored in the database in the project file you downloaded. No one else has access to it. That being said, if you share the project folder and you have entered information into the database, people who open the database will have access to your credit card information. ***Be ultra careful with this!***

After you have entered information, you will receive an automated email from *kristoffersenmatthew@gmail.com* saying that you have registered. It might take a little bit to receive the email. You will then be directed to the Buy page. If you would like to view your information, press the **Your Information** button on the top left of your screen. If you would like to update your information, press the button at the bottom of your screen. Your credit card information is censored on this page for your protection.

Anyway, sooner or later you will want to buy a Chad Shirt of your own. Press **Buy Chad Shirts** at the top of your screen. Scroll down and you will see the picture of the shirt as well as information about it and its price before taxes or shipping. Summed up, the price of a Chad Shirt is around $23.

Select the desired size and press the button on the bottom of your screen.

**You don't have to do a single thing after this point! Just sit tight and wait. It takes a good 10 seconds for the bot to do everything it needs to do.**

Use this time to call your mother. I'm sure she misses you. Or don't. I'm not the boss of you, just buy a Chad Shirt.

If everything is successful, you will receive an automated email from *chadshirtsbot@gmail.com* saying that it succeeded and you will be redirected to a success page with a gif of my hero, Lil Uzi Vert. Isn't he awesome? You will also receive an email from ChadShirts saying that you have successfully purchased a shirt. 

**SUPER IMPORTANT NOTE:** You have ***for realsies*** purchased a Chad Shirt. Your card ***will*** be charged however much it costs. And in about 2 weeks, you will receive your very own Chad Shirt in whatever size you chose! In testing this app, I bought more shirts than I care to admit. If you are just testing the app and **do not desire** a Chad Shirt, enter in a valid but inaccurate credit card number, or change your expiration date. I am not responsible for any bank issues stemming from invalid information.

# Quitting the app

To stop the program, go to your terminal of choice. Hold the *control* key and press **C**. The program is now stopped, and if you refresh the web page, Chrome will give you an error.

To open it again, or upon any changes to application.py that you would like reflected in the webpage, enter this in your terminal of choice:

~~~
$ export FLASK_APP=application.py
$ flask run
~~~

or:

~~~
$ export FLASK_APP=application.py flask run
~~~
Either will do.

# Image Gallery

To save you the money (and the time), I have included screenshots that I had the Chrome bot take at various steps in the process. I bought a Chad Shirt successfully using my bot, so these images will show you what it looks like when everything works. 

[Follow this link for the images!](https://imgur.com/a/Nt145z1)

Please note that my information has been blacked out for my own protection. Please don't use my credit card information!!! Please.

The last image is a screenshot from my mail client with the confirmation of my order. The name is "Matt Kristoffersen Matt Kristoffersen" due to a bug that I have since worked out. If I were to take new screenshots, I'd be out another $23. I can't afford that, so I apologize in advance.



# Contact the Author

If for any reason you are having problems with the project or need additional clarification, here is my contact information:

Phone Number: (909) 331-6761

Email: matthew.kristoffersen@yale.edu OR kristoffersenmatthew@gmail.com

Mailing Address: PO Box 201872 New Haven, CT 06520

Github: mattkristoffersen

Instagram: matt.kristoffersen

Twitter: @mattkristoffers


Feel free to email, call, text me, DM me, mail me, etc. at any time and I will do my best to respond within 1 hour. If you urgently need me, calling me is your best bet.

**Thank you for reading! Please look at DESIGN.md to see what I did and why I did it.**