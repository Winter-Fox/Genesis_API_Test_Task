from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests

import smtplib, ssl

import re
 
#Valid email checker
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

#Function which gets tickers of given coins to given currency
#Povered by Kuna.io API
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
                return {"409" : "Email already exists"}
        emails_file.write(email)
        emails_file.close()
        return {"200" : "E-mail додано"}

class Sender(Resource):
    port = 465  # For SSL
    password = "hclhisvdwezkasuo"
    smtp_server = "smtp.gmail.com"
    sender_email = "devtest.24.101@gmail.com" 
    def post(self):
        tickers = getTickers()
        #smtp setup
        context = ssl.create_default_context() 
        message = """\
Subject: Bitcoin price in UAH


"""
        message += ("One Bitcoin = " + str(tickers[0][1]) + " uah")
        emails_file = open("emails.txt", 'r')
        Lines = emails_file.readlines()

        #Send email via Gmail smtp 
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                try:
                    server.login(self.sender_email, self.password)
                except Exception as e:
                    print(e)
                    return {"400" : "Error occured while logging into smtp server"}
                for line in Lines:
                    receiver_email = line[:-1]
                    try:
                        server.sendmail(self.sender_email, receiver_email, message)
                    except Exception as e:
                        print(e)
            return {"200" : "E-mailʼи відправлено"}
        except Exception as e:
            print(e)
            return {"400" : "An error occured while SMTP_SSL connection."}

    def put(self):
        smtp_server = request.args.get('smtp_server')
        if not smtp_server: return {"400" : "No smtp_server provided."}
        if not checkEmail(smtp_server): return {"400" : "You provided incorrect email for the smtp_server."}
        password = request.args.get('password')
        if not password: return {"400" : "No password provided."}
        self.smtp_server = smtp_server
        self.password = password
        return {"200" : "smtp_server was succefully updated."}




app = Flask(__name__)
api = Api(app)

api.add_resource(Rate, "/api/rate")
api.add_resource(Subscription, "/api/subscribe")
api.add_resource(Sender, "/api/sendEmails")

if __name__ == "__main__":
    app.run()