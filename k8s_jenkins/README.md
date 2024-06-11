# Kubernetes + Jenkins Project
## Dependencies
### Agent Dependencies:
* yq
* java
* docker
* docker-compose
* git
* aws cli
* kubectl
    > There is another option of using 2 different agents from different AMI's, one for each pipeline each with its own dependencies.
### Secrets Required:
* gitlab credentials
* dockerhub credentials

### Jenkins Plugins:
* GitLub
* git
* Amazon EC2
* Slack Notification
* configuration as code
* Publish Over SSH

## The app
I used a python app that I created as the deployed app, it provides the client with a weekly forecast using flask and an external api, provided back to the client through gunicorn and nginx.

## deployment.yaml
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: weather-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: weather
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 1
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: weather
    spec:
      containers:
      - name: weather
        image: barminz/weather_k8s:1
        ports:
        - containerPort: 9090
```
Used to deploy the app on a kubernetes cluster.

## ingress.yaml
```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  namespace: default
spec:
  ingressClassName: nginx
  rules:
  - host: a51bf195e55044294b10e0203cfbc9fd-1831477577.eu-north-1.elb.amazonaws.com # Change to the ingress name
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: weather-service
            port:
              number: 9090
```
Used to deploy an ingress.

## Jenkinsfile & Jenkinsfile_deployment
2 Pipelines for the app, one for building the app's image and delivering it, and one for deploying it on the cluster.
