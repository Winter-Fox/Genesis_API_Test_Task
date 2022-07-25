from flask import Flask
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


api.add_resource(Rate, "/rate")


if __name__ == "__main__":
    app.run()