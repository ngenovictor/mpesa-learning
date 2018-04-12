import requests
from requests.auth import HTTPBasicAuth
import json
import base64
import datetime
import keys

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
my_phone_no = keys.phone_number


class Mpesa(object):
    def authenticate(self):
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?" \
              "grant_type=client_credentials"

        response = requests.get(url, auth=HTTPBasicAuth(consumer_key,
                                                        consumer_secret))
        json1_data = json.loads(response.text)
        return json1_data

    def lipa_na_mpesa(self):
        access_token = self.authenticate()["access_token"]
        date = datetime.datetime.now()
        time_stamp = "{}{:02d}{:02d}{:02d}{:02d}{:02d}".format(
            date.year, date.month, date.day, date.hour, date.minute, date.second)
        short_code = "174379"
        pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        password = base64.b64encode("{}{}{}".format(
            short_code, pass_key, time_stamp).encode("utf-8")).decode("utf-8")

        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        query_string = {
            "BusinessShortCode": short_code,
            "Password": password,
            "Timestamp": time_stamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "10",
            "PartyA": my_phone_no,
            "PartyB": short_code,
            "PhoneNumber": my_phone_no,
            "CallBackURL": "http://mpesa-requestbin.herokuapp.com/z96k52z9",
            "AccountReference": "vcbnskl11223",
            "TransactionDesc": "lipa man"
        }
        response = requests.post(api_url, json=query_string, headers=headers)

        print(response.text)


if __name__ == "__main__":
    mine = Mpesa()
    mine.lipa_na_mpesa()