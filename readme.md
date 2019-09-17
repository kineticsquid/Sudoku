### Overview

#### Resources
https://developer.ibm.com/tutorials/scalable-python-app-with-kubernetes/
https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-ingress-guide-nginx-example.html
https://kubernetes.github.io/ingress-nginx/deploy/

#### To Build and Run
1. Start Docker daemon
1. Build and deploy cloud solver function by running `/Solver-Cloud-Function/build-and-deploy-function.sh`
1. Test the cloud function by running `/Solver-Cloud-Function/test-function.sh`
1. Build base docker image by running `/Base-Docker-Image/build-base-docker-image.sh`
1. Build application docker image by running `build-main-app-image.sh`
1. Run docker image locally with `run-app-locally.sh`
1. Test docker image locally with `test-app-local.sh`
1. To list running containers: `docker ps`
1. Stop with `docker kill [container name]`
1. Deploy app to Bluemix...

#### Deploying to Bluemix
_One Time Steps_
1. Create a Bluemix Kube service instance
1. Create a Bluemiux Container Registry service instance
1. Login: `ibmcloud login --sso`
1. Install container service plugin: `ibmcloud plugin install container-service -r Bluemix`
    - Update plugin: `ibmcloud plugin update container-service`
1. Use `ibmcloud cs init` to validate installation
1. Install container registry plugin: `ibmcloud plugin install container-registry -r Bluemix`
1. Use `ibmcloud plugin show container-registry` to validate installation
1. Install IBM Containers plugin: `ibmcloud plugin install IBM-Containers -r Bluemix`
1. Install `kubectl` command line: `brew install kubernetes-cli`
1. Set region: `ibmcloud cs region-set us-east`
1. Create a namespace: `cr namespace-add kellrman`
1. To show images: `ibmcloud cr images`
1. To show namespaces: `ibmcloud cr namespaces`
1. Get the registry URL with: `ibmcloud cr region`
1. Tag local image with `docker tag [imagename] [registry URL]/[namespace]/[imagename]:latest`. E.g. `docker tag sudoku-main registry.ng.bluemix.net/sudoku/sudoku-main:latest`
1. List local images to validate tag: `docker images`
1. Configure cluster for use with Kube command line: `ibmcloud cs cluster-config <cluster_name_or_id>`. E.g. `ibmcloud cs cluster-config sudoku`
1. Copy and execute the `export` command that is output from the command.
1. Create a YAML file to describe the deployment.
1. Run command `kubectl apply -f [deployment_script_location]`. This will create the pod.

#### Deploying to Bluemix Each time
1. Start the docker daemon.
1. Build the image - see above
1. Login to container registry with `ibmcloud cr login`
1. Delete old Sudoku pod on kube if one exists.
1. List clusters: `ibmcloud cs clusters`
1. Configure cluster for use with Kube command line: `ibmcloud cs cluster-config sudoku`
1. Copy and execute the `export` command that is output from the command.
1. Run `kubectl proxy` to start dashboard app locally.
1. Browse the displayed url with `ui` added. E.g. `http://127.0.0.1:8001/ui`
1. `kubectl run sudoku --image=registry.ng.bluemix.net/sudoku/sudoku-main:latest --port=80`
1. `kubectl expose deployment sudoku --port=80 --target-port=5000 --type=NodePort`
1. Run `ibmcloud cs workers kellrman` to get pubic IP address
1. Run `kubectl describe service sudoku` to get port (Nodeport)
1. Wait. Large docker files take a while to load

To Terminte
1. to list deployments: `kubectl get deployments`, `kubectl get pods`
1. `kubectl delete deployment sudoku`
1. `kubectl delete service sudoku`


### Other commands
  - Stop a container. Name comes from `docker ps` command.
`docker stop [name]`
  - List all exited containers:
`docker ps -a -f status=exited`
  - Remove all exited containers:
`docker rm $(docker ps -a -f status=exited -q)`
  - List all images:
`docker images -a`
  - List dangling images: `docker images -f dangling=true`
  - Remove dangling images: `docker rmi $(docker images -f dangling=true -q)`
  - Remove all images: `docker rmi $(docker images -a -q)`
  - see storage use `ibmcloud cr quota`
  - list images in registry `ibmcloud cr images`
  - remove an image from the registry `ibmcloud cr image-rm [image]`
 

### Additional Information

Kube dashboard (run `kubectl proxy` command first):
http://localhost:8001/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy/#!/overview?namespace=default

Blluemix container info:
https://console.bluemix.net/docs/containers/cs_cluster.html#cs_cluster
https://developer.ibm.com/recipes/tutorials/deploying-ibm-containers-in-kebernetes-on-ibm-bluemix/

Twilio:
https://support.twilio.com/hc/en-us/articles/223134127-Receive-SMS-messages-without-Responding

Creating custom packages:
http://jamesthom.as/blog/2017/04/27/python-packages-in-openwhisk/

Conversation OpenWhisk integration:
https://github.ibm.com/watson-engagement-advisor/convo-flexible-bot

DevOps for OpenWhisk:
https://www.ibm.com/blogs/bluemix/2016/11/automate-deployment-openwhisk-actions/

Accessing Bluemix Kube cluster:
https://console.bluemix.net/containers-kubernetes/clusters/11be094024ea48bda0807ea4cd81ca14/access?region=ibm:yp:eu-de

Setting up Kubectl command line:
https://kubernetes.io/docs/tasks/tools/install-kubectl/

OCR:
https://github.com/tesseract-ocr/tesseract
https://gist.github.com/henrik/1967035

tesseract IMG_1054.JPG stdout -c tessedit_char_whitelist=123456789 --psm 6
