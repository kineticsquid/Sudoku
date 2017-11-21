from twilio.rest import Client
import json
import sys

def main(input_dict):

    # Twilio credentials
    account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
    auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

    try:
        print("input dictionary:")
        print(json.dumps(input_dict))
        message = input_dict.get('message', None)
        number = input_dict.get('number', None)
        media_url = input_dict.get('media_url', None)
        if message is None or number is None:
            raise Exception("Need message and number inputs.")
        client = Client(account_sid, auth_token)

        if media_url is None:
            sms=client.messages.create(
                to=number,
                from_="+14243895429",
                body=message)
        else:
            sms=client.messages.create(
                to=number,
                from_="+14243895429",
                body=message,
                media_url=media_url)
        return_results = {"code": 200, "body": str(sms.sid)}
        print("return:")
        print(return_results)
        return return_results
    except Exception as error:
        error = {"code": 500, "body": str(error)}
        print(error)
        return error

# This invocation does not happen in Whisk, only outside
if __name__ == '__main__':
    if len(sys.argv) == 3:
        main({"number": sys.argv[1], "message": sys.argv[2]})
    else:
        raise Exception("Need message and number inputs.")
