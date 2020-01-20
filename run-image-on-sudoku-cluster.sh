#!/bin/bash
echo "URL: https://ibm.biz/Bdqxwt"

export KUBECONFIG=/Users/$USER/.bluemix/plugins/container-service/clusters/boif5mdw0btjak7g2d90/kube-config-wdc07-sudoku.yml

echo "KUBECONFIG="$KUBECONFIG

kubectl delete deployment sudoku-solver-deployment
kubectl delete service sudoku-solver-service
kubectl delete ingress sudoku-solver-ingress

kubectl apply -f sudoku-deployment.yaml

echo "Deployment:"
kubectl describe deployment sudoku-solver-deployment

echo "Service:"
kubectl describe service sudoku-solver-service

echo "Ingress:"
kubectl describe ingress sudoku-solver-ingress

