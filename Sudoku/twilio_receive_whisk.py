from twilio.twiml.messaging_response import MessagingResponse
import AppExceptions
import json

def main(input_dict):

    try:
        print(json.dumps(input_dict, indent=4))
        # put your own credentials here
        account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
        auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

        resp = MessagingResponse()

        # Add a message
        resp.message("The Robots are coming! Head for the hills!")

        return {"response": str(resp)}
    except AppExceptions as error:
        return {"error": error.message}
    except Exception as error:
        return {"error": str(error)}

if __name__ == '__main__':
    main({})