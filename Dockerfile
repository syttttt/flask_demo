FROM openkbs/jdk-mvn-py3
USER root
WORKDIR /app
#COPY * /app/
#COPY ./record /app/record
RUN pwd
USER root
RUN ls -a
#RUN mkdir /temp
#RUN ls -a
