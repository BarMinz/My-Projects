# Python MongoDB and Kafka project
## Run mongodb container
```
docker run -d -p 27017:27017 --name mongo mongo:latest
```
### Enter mongo's CLI
```
docker exec -it example-mongo mongosh --port 27017
```
## Run zookeeper container
```
docker run -d --name zookeeper -p 2181:2181 zookeeper
```
## Run Kafka container
```
docker run -d --name kafka -p 9092:9092   --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181   --env KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092   --env KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092   --link zookeeper:zookeeper   wurstmeister/kafka
```
## Create venv's for the frontend and backend of the app
* backend
```
python -m venv venv-client 
```
* frontend
```
python -m venv venv-api
```

## Install env's dependencies
```
source venv-client/bin/activate 
pip install flask kafka-python requests

source venv-api/bin/activate
pip install flask pymongo kafka-python
```
## Run both python files in the relevant environments


* Ignore the nginx folder, not in use at the moment
