import json
import re
import math
import requests

SOLVE_URL = 'https://openwhisk.ng.bluemix.net/api/v1/namespaces/kellrman%40us.ibm.com_dev/actions/sudoku/solve'

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
        print("input Dictionary")
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
            data= {"input" : str(matrix)}
            response = requests.post(SOLVE_URL, data=data)
            if response.status_code == 200:
                results = response.content
            else:
                raise Exception('Error invoking solve function: %s' % response.status_code)
        return {"number" : incoming_number,
            "message" : str(results) }
    except Exception as error:
        return {"error": str(error)}

if __name__ == '__main__':
    main({"From" : "+19192446142", "Body": "[1,2,3,4]"})