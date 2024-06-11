# Initiate the cluster with terraform
```
    terraform init
    
    terraform apply --auto-approve
```
* deploy cluster with 2 nodes t3.medium

# Update the context
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    
    chmod +x kubectl
    
    sudo mv kubectl /usr/local/bin/
    
    aws eks update-kubeconfig --name pc-eks --region eu-north-1

## Install ingress controller
    kubectl apply -f https://raw.githubusercontent.com/nginxinc/kubernetes-ingress/v3.5.0/deploy/crds.yaml
    
    helm install my-release oci://ghcr.io/nginxinc/charts/nginx-ingress --version 1.2.0

## Update nlb address and deploy ingress object
    kubectl apply -f ingress.yaml

# Install persistent volume controller
    kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"

## deploy kafka and zookeeper files
    kubectl apply -f kafka/.

## install mongodb with helm chart
    helm install mongodb-release bitnami/mongodb --version 15.6.0

## deploy front and back files
    kubectl apply -f app.yaml