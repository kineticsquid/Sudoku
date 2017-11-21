import json
import re
import math
import requests
import sys

# Both of these URLs seem to work, not sure of the difference
# SOLVE_URL = 'https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve.json'
SOLVE_URL = 'https://openwhisk.ng.bluemix.net/api/v1/web/kellrman%40us.ibm.com_dev/sudoku/solve'

def extractMatrix(input):
    matrix = []
    digit_re = re.compile('\d')
    results = digit_re.findall(input)
    rows = int(math.sqrt(len(results)))
    if rows != math.sqrt(len(results)):
        raise Exception('Input error: matrix must be square.')
    else:
        new_row = []
        for i in results:
            new_row.append(int(i))
            if len(new_row) == rows:
                matrix.append(new_row)
                new_row = []
    return(matrix)


def main(input_dict):

    try:
        print("input dictionary:")
        print(json.dumps(input_dict))
        account_sid = "ACefa1096c033ccd122b24a0480cfb21c5"
        auth_token = "4d965a0c6fd26c27070ccf849f817ac4"

        incoming_number = input_dict.get('From', None)
        incoming_message = input_dict.get('Body', None)

        if incoming_message is None or incoming_number is None:
            raise Exception('Input error, no incoming number or message.')
        else:
            print("From: %s: %s" % (incoming_number, incoming_message))
            matrix = extractMatrix(incoming_message)
            print(str(matrix))
            # We need to dump the json to string otherwise a 400 error about malformed JSON results
            data = json.dumps({"matrix": str(matrix)})
            headers = {"content-type": "application/json"}
            response = requests.post(SOLVE_URL, data=data, headers=headers)
            # Not sure why, but sometimes the cloud function returns a 204 status code when successful
            if response.status_code >= 200 and response.status_code < 300:
                result_content = json.loads(response.content)
                function_code = result_content['statusCode']
                function_results = result_content['body']
                if function_code != 200:
                    raise Exception(function_results)
            else:
                raise Exception('Error invoking solve function: %s - %s' % (response.status_code, response.content))
            return_results = {"number": incoming_number, "message" : str(function_results)}
            print("return:")
            print(return_results)
        return return_results
    except Exception as error:
        error = {"statusCode": 500, "body": str(error)}
        print(error)
        return error

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main({"From": sys.argv[1], "Body": sys.argv[2]})
    else:
        raise Exception('Input error, no incoming number or message.')