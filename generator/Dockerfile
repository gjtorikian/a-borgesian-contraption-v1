FROM tensorflow/tensorflow:2.1.0-gpu-py3

RUN apt-get -y update && apt-get -y install gcc

WORKDIR /
COPY pytorch /pytorch

# Make changes to the requirements/app here.
RUN pip3 --no-cache-dir install transformers==2.8.0 torch==1.4 starlette uvicorn ujson
COPY server.py /
COPY variables.py /
COPY prompts.txt /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENTRYPOINT ["python3", "-X", "utf8", "server.py"]
