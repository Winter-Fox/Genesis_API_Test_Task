from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests

import smtplib, ssl

import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#Function which gets tickers of given coins to given currency
def getTickers(coins = ['btc'], currency = ['uah']):
    url = "https://api.kuna.io/v3/tickers?symbols="
    #Create url with all coin-currency pairs
    for coin in coins:
        for curr in currency:
            url += (coin + curr + ',')
    url = url[:-1]
        
    r = requests.get(url)
    return r.json()

class Rate(Resource):
    def get(self):
        try:
            tickers = getTickers()
            print(tickers)
            return {"200" : tickers[0][1]}
        except Exception as e:
            print(e)
            return {"400" : "Invalid status value"}

class Subscription(Resource):
    def post(self):
        email = request.args.get('email')
        if not checkEmail(email): return {"400" : "Email has incorrect format. Enter a valid email."}
        if not email: return {"400" : "No email provided."}
        email += "\n"
        # Add email to the file
        emails_file = open("emails.txt", 'r+')
        Lines = emails_file.readlines()
        for line in Lines:
            if line == email:
                return {"400" : "Email already exists"}
        emails_file.write(email)
        emails_file.close()
        return {"200" : "Email has been succefully added"}

class Sender(Resource):
    def post(self):
        tickers = getTickers()

        #smtp setup
        port = 465  # For SSL
        context = ssl.create_default_context()
        password = "hclhisvdwezkasuo"
        smtp_server = "smtp.gmail.com"
        sender_email = "devtest.24.101@gmail.com"  
        message = """\
Subject: Bitcoin price in UAH


"""
        message += ("One Bitcoin = " + str(tickers[0][1]) + " uah")
        emails_file = open("emails.txt", 'r')
        Lines = emails_file.readlines()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            try:
                server.login(sender_email, password)
            except Exception as e:
                print(e)
                return {"400" : "Error occured while logging into smtp server"}
            for line in Lines:
                receiver_email = line[:-1]
                try:
                    server.sendmail(sender_email, receiver_email, message)
                except Exception as e:
                    print(e)
        return {"200" : "E-mailʼи відправлено"}



app = Flask(__name__)
api = Api(app)

api.add_resource(Rate, "/rate")
api.add_resource(Subscription, "/subscribe")
api.add_resource(Sender, "/sendEmails")

if __name__ == "__main__":
    app.run()