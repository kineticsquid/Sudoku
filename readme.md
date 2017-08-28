## Folders with sources for OpenWhisk Actions

Twilio:
https://support.twilio.com/hc/en-us/articles/223134127-Receive-SMS-messages-without-Responding

Creating custom packages:
http://jamesthom.as/blog/2017/04/27/python-packages-in-openwhisk/

Conversation OpenWhisk integration:
https://github.ibm.com/watson-engagement-advisor/convo-flexible-bot

DevOps for OpenWhisk:
https://www.ibm.com/blogs/bluemix/2016/11/automate-deployment-openwhisk-actions/

1. Open Preferences and select Project Interpreter
1. Click on the settings (gear icon) and select to create a virtualenv
1. Select appropriate runtime. Not sure what including global site packages does
1. Set this as runtime for the project
1. Some pre-reqs will likely fail now. Let Pycharm fix this by adding them to the virtualenv.
1. Invoke the Whisk action from the dev environment with the following. This will cause the dictionary to be sent as input, but when the code is deployed in Whisk, this code is not executed. 

    `if __name__ == '__main__':
        main({"message": "Hi", "number": "+19195787993"})`