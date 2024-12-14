FROM ubuntu:latest
LABEL authors="luca.martins"


ENV MONGODB_URI="mongodb+srv://waterwise-api:vLBYy1nJLViOfDdN@waterwise-cluster.l5ctm.mongodb.net/?retryWrites=true&w=majority&appName=WaterWise-Cluster"

ENTRYPOINT ["top", "-b"]