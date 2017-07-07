FROM anapsix/alpine-java:8
MAINTAINER David Turanski <dturanski@pivotal.io>


#Install dependencies
RUN apk update && apk add bzip2 wget

#Install conda
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.3.21-Linux-x86_64.sh -O ~/miniconda.sh
RUN /bin/bash ~/miniconda.sh -b -p /opt/conda
RUN rm ~/miniconda.sh

#Install springcloudstream package - Temporary for now

COPY lib/springcloudstream-1.1.0-py2.py3-none-any.whl ./python-lib
COPY *.jar ./
COPY *.py ./
COPY environment.yml ./

ENV PYTHONPATH=./python-lib:$PYTHONPATH
ENV PATH=/opt/conda/bin:$PATH
RUN conda env create -f environment.yml -n default && /bin/bash -c 'source activate default'

VOLUME /tmp

ENTRYPOINT [ "java", "-jar", "python-local-processor-rabbit-1.2.1.BUILD-SNAPSHOT.jar" ]