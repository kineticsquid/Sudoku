#
#
# main() will be invoked when you Run This Action
#
# @param OpenWhisk actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import os


def main(dict):
    e = os.environ
    output = {"Input dictionary" : dict}
    print("Input Dictionaery: %s\n\n" % dict)
    print("Environment:")
    for key in e.keys():
        output[key] = e[key]
        print("\t%s" % e[key])
    return output


# This invocation does not happen in Whisk, only outside
if __name__ == '__main__':
    main({"input": "Goes here"})