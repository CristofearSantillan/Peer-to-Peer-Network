# creates a python image
FROM python:latest

# uncomment RUN command below to use scapy
# RUN pip install scapy

# adds the python file to the working directory
ADD main.py .

# the working directory
WORKDIR .