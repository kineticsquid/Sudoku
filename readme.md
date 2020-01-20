## Sudoku

Info on deploying to kubernetes: https://cloud.ibm.com/docs/containers?topic=containers-ingress


1. Logon first with `ibmcloud login -a cloud.ibm.com -r us-east -g 'JKs Resource Group' --sso`
1. Then `ibmcloud ks cluster config --cluster boif5mdw0btjak7g2d90`
1. Then to get access, `export KUBECONFIG=/Users/jk/.bluemix/plugins/container-service/clusters/boif5mdw0btjak7g2d90/kube-config-wdc07-sudoku.yml`
1. Use `ibmcloud ks cluster get --cluster boif5mdw0btjak7g2d90 | grep Ingress` to get ingress and secret
1. Test access with `kubectl get nodes`
1. URL Shortening: https://snip.innovate.ibm.com/

Deployment short URL: https://ibm.biz/Bdqxwt