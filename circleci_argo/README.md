# CirecleCI Project
## Git Repo
- Create a Git repo with your source code.
## Create A CircleCI Pipeline
- [Create account](https://app.circleci.com/home/)
- Create an organization.
- Create a project (I used Github).
- Connect your Github account and choose a repository.
- Create a configuration file in the repository and save the path in a configuration source in the CircleCI.
- Create a Trigger in the CircleCI and connect it in the CircleCI to the configuration source.
### Example Basic Pipeline
```yaml
version: 2.1

orbs:
  discord: antonioned/discord@0.1.0

# Define the jobs we want to run for this project
jobs:
  build:
    docker:
      - image: cimg/base:2023.03
    steps:
      - checkout
      - run: echo "This is a build stage"
  test:
    docker:
      - image: cimg/base:2023.03
    steps:
      - checkout
      - run: echo "This is a test stage"
# Orchestrate our job run sequence
workflows:
  build_and_test:
    jobs:
      - build
      - test
```
## Build
- Add a setup_remote_docker step.
- Use either docker build or docker compose to build the image.
## Test
- Add the test files to your docker image.
- Add a curl installation stage to the Dockerfile:
    ```Dockerfile
    RUN apk update && apk add --no-cache curl
    ```
## Send Notification to Discord
- Add a Discord Orb:
    ```yaml
    orbs:
        discord: antonioned/discord@0.1.0
    ```
- Add the following stage to your pipeline:
    ```yaml
    - discord/status:
        fail_only: false
        failure_message: "**${CIRCLE_USERNAME}**'s build: **${CIRCLE_JOB}** failed."
        success_message: "**${CIRCLE_USERNAME}** Success."
        webhook: "$DISCORD_WEBHOOK"
    ```
- Create a discord webhook and save it as a secret in the environment variables.
## Upload the images to Gitlab Registry
- [Create a Gitlab account](https://about.gitlab.com/)
- Create a repository.
- Go to Deploy -> Container Registry.
- Create and Access Token.
- Create Secrets in CircleCI of both your username and access token.
- Add the following stage to the pipeline:
    ```yaml
    - run:
        name: "Gitlab login and push"
        command: |
                echo "$GITLAB_TOKEN" | docker login registry.gitlab.com -u $GITLAB_USER --password-stdin
                docker tag weather-app-app registry.gitlab.com barminz1209/circleci-weather:$(git rev-parse --short HEAD)
                docker push registry.gitlab.com/barminz1209/circleci-weather:$(git rev-parse --short HEAD)
                docker tag weather-app-app registry.gitlab.com/barminz1209/circleci-weather:latest
                docker push registry.gitlab.com/barminz1209/circleci-weather:latest
    ```
- [Gitlab Registry](https://docs.gitlab.com/ee/user/packages/container_registry/)
- [login syntax](https://docs.gitlab.com/ee/user/packages/container_registry/authenticate_with_container_registry.html)
## Check Terraform files with Checkov
- Download Checkov:
    ```bash
    pip3 install checkov
    ```
- Run: 
    ```bash 
    checkov -f PATH/TO/DIR/*.tf 
    ```
    OR
    ```bash
    terraform init
    terraform plan --out tfplan.binary
    terraform show -json tfplan.binary | jq > tfplan.json

    checkov -f tfplan.json
    ```
## Check Terraform files with Terratest
### Running Locally
- [Download GO](https://go.dev/doc/install)
- Run go mod init <project name>.
- Run go mod tidy.
  * Both in the terraform folder.
- Inside of the terraform folder create a test folder.
- Inside it create a go file ending in "_test.go".
- run the test with ``` go test -v -timeout 30m ``` from the test folder.
### Running On Pipeline
- Add 2 orbs:
  > aws-eks: circleci/aws-eks@1.0.0

  > kubernetes: circleci/kubernetes@0.11.1
- Add the following environment variables to Circleci:
  > ```AWS_ACCESS_KEY_ID```

  > ```AWS_DEFAULT_REGION```

  > ```AWS_SECRET_ACCESS_KEY```
- Change working dir to the terraform dir and run ```go mod init <project name>``` and ```go mod tidy```.
- Change working dir to the test folder and run the test with ```go test -v -timeout 30m```.
## Deploying the eks cluster
- Clone the repo in a new job using ```docker.mirror.hashicorp.services/hashicorp/terraform:light``` as the runner image.
- Run ```terraform init```.
- Run ```terraform apply --auto-aprove```.