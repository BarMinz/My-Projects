FROM maven:3.8.4 as maven

ARG SONARQUBE_TOKEN
ARG SONARQUBE_HOST

COPY . .

# Running SonarQube
RUN mvn package sonar:sonar -Dsonar.login=$SONARQUBE_TOKEN -Dsonar.host.url=$SONARQUBE_HOST


FROM releases-docker.jfrog.io/jfrog/jfrog-cli-v2-jf  as jfrog

ARG JF_HOST
ARG USER_NAME
ARG USER_PASS

COPY --from=maven ./target/Calculator-1.0-SNAPSHOT.jar .

RUN jf rt u --url=$JF_HOST --user=$USER_NAME --password=$USER_PASS Calculator-1.0-SNAPSHOT.jar libs-snapshot-local


FROM openjdk:11-jre-slim as java

COPY --from=jfrog ./Calculator-1.0-SNAPSHOT.jar .

CMD java -jar Calculator-1.0-SNAPSHOT.jar


# Run the following command in the pipeline:
# sh 'docker build --build-arg SONARQUBE_TOKEN=$SONARQUBE_TOKEN  --build-arg SONARQUBE_HOST=$SONARQUBE_HOST  --build-arg JF_HOST=$JF_HOST
#--build-arg USER_NAME=$USER_NAME --build-arg USER_PASS=$USER_PASS -t image:$BUILD_NUMBER .'
