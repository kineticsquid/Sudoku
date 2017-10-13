from twilio.rest import Client
import json

def main(input_dict):

    # Twilio credentials
    account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
    auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

    try:
        print(json.dumps(input_dict, indent=4))
        message = input_dict.get('message', None)
        number = input_dict.get('number', None)
        media_url = input_dict.get('media_url', None)
        if message is None or number is None:
            raise Exception("Need message and number inputs.")
        if media_url is None:
            media_url = "https://c1.staticflickr.com/3/2899/14341091933_1e92e62d12_b.jpg"

        client = Client(account_sid, auth_token)

        sms=client.messages.create(
            to=number,
            from_="+14243895429",
            body=message,
            media_url=media_url)
        print(sms.sid)
        return {"sid": str(sms.sid)}
    except Exception as error:
        print(str(error))
        return {"error": str(error)}

# This invocation does not happen in Whisk, only outside
if __name__ == '__main__':
    main({"message": "Hi", "number": "+19192446142"})