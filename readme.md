### Overview
This is a set of scripts that implement OpenWhisk (Bluemix Could Functions). Structure is one action per folder. 
 
Becasue these scripts have Python dependencies that are not included in the Python3 runtime provided, we need to build an environment and deploy it with the code implementing the script.

Do this manually using PyCharm:
1. Open Preferences and select Project Interpreter
1. Click on the settings (gear icon) and select to create a virtualenv
1. Select appropriate runtime. Not sure what including global site packages does
1. Set this as runtime for the project
1. Some pre-reqs will likely fail now. Let Pycharm fix this by adding them to the virtualenv.

Or, there is a `build_virtual_env.sh` script for this. 

Note, building this as part of the Bluemix DevOps pipeline doesn't work because `virtualenv` is not part of the deployment pipeline runtime. 

DevOps pipeline then invokes the `deploy.sh` and `test.sh` scripts

For these scripts to work they need to authorize via API key. Create one from the Bluemix console and then pass it in to the deployment script as an environment variable.

Invoke the Whisk action from the dev environment with the following. This will cause the dictionary to be sent as input, but when the code is deployed in Whisk, this code is not executed. 

    `if __name__ == '__main__':
        main({"message": "Hi", "number": "+19195787993"})`

### Additional Information

Twilio:
https://support.twilio.com/hc/en-us/articles/223134127-Receive-SMS-messages-without-Responding

Creating custom packages:
http://jamesthom.as/blog/2017/04/27/python-packages-in-openwhisk/

Conversation OpenWhisk integration:
https://github.ibm.com/watson-engagement-advisor/convo-flexible-bot

DevOps for OpenWhisk:
https://www.ibm.com/blogs/bluemix/2016/11/automate-deployment-openwhisk-actions/
