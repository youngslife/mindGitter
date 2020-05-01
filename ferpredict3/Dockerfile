FROM continuumio/miniconda3
COPY . /app
ADD environment.yml /tmp/environment.yml
Add patch/backend.py /tmp/backend.py

EXPOSE 8000

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN apt install -y default-jre
RUN apt install -y default-jdk
RUN conda env create -f /tmp/environment.yml

# Create the environment:
RUN echo "source activate myenv" > ~/.bashrc
ENV PATH /opt/conda/envs/myenv/bin:$PATH

RUN cp -f /tmp/backend.py /opt/conda/envs/myenv/lib/python3.7/site-packages/tensorflow_core/python/keras/backend.py

WORKDIR /app
RUN chmod 755 start
ENTRYPOINT ["/app/start"]
