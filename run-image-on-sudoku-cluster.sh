#!/bin/bash
echo "Logon first with 'ibmcloud login -a cloud.ibm.com -r us-east --sso'"
echo "then 'ibmcloud ks cluster-config --cluster sudoku'"
echo "'bx ks cluster-get sudoku | grep Ingress' will provide external hostname and TLS secret'"
echo "Then to get access, 'export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/sudoku/kube-config-wdc07-sudoku.yml'"
echo "then 'kubectl get nodes'"

export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/sudoku/kube-config-wdc07-sudoku.yml

kubectl delete service exposed-sudoku-service
kubectl delete pod sudoku-service
kubectl run sudoku-service --image=us.icr.io/sudoku/sudoku-main --generator=run-pod/v1 --port=80 --replicas=2
kubectl expose pod sudoku-service --port=80 --target-port=5000 --type=NodePort --name exposed-sudoku-service
kubectl describe pod sudoku-service
echo "Public port (nodeport)..."
kubectl describe service exposed-sudoku-service
echo "Public IP address..."
ibmcloud ks workers sudoku

kubectl apply -f sudoku-ingress.yaml
kubectl describe ingress sudoku-ingress
