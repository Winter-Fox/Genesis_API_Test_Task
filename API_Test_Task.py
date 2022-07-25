from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import requests

app = Flask(__name__)
api = Api(app)

class Rate(Resource):
    def getTickers(self, coins = ['btc'], currency = ['uah']):
        url = "https://api.kuna.io/v3/tickers?symbols="

        #Create url with all coin-currency pairs
        for coin in coins:
            for curr in currency:
                url += (coin + curr + ',')
        url = url[:-1]
        
        r = requests.get(url)
        return r.json()

    def get(self):
        try:
            response = self.getTickers()
            print(response)
            return {"200" : response[0][1]}
        except Exception as e:
            print(e)
            return {"400" : "Invalid status value"}

class Subscription(Resource):
    def post(self):
        email = request.args.get('email')
        if not email: return {"400" : "No email provided"}
        email += "\n"
        # Add email to the file
        emails_file = open("emails.txt", 'r+')
        Lines = emails_file.readlines()
        for line in Lines:
            if line == email:
                return {"400" : "Email already exists"}
        emails_file.write(email + '\n')
        emails_file.close()
        return {"200" : "Email has been succefully added"}

api.add_resource(Rate, "/rate")
api.add_resource(Subscription, "/subscribe")


if __name__ == "__main__":
    app.run()