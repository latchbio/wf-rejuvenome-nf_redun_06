FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

RUN apt-get install -y curl unzip git

RUN apt-get install -y default-jre-headless
RUN curl -s https://get.nextflow.io | bash \
    && mv nextflow /usr/bin/

RUN apt-get install procps -y
RUN python3 -m pip install cutadapt

RUN curl -L https://github.com/bwa-mem2/bwa-mem2/releases/download/v2.2.1/bwa-mem2-2.2.1_x64-linux.tar.bz2 -o bwa-mem2-2.2.1_x64-linux.tar.bz2 &&\
    tar -xjvf bwa-mem2-2.2.1_x64-linux.tar.bz2 &&\
    mv bwa-mem2-2.2.1_x64-linux/* /usr/bin  &&\
    rm -rf bwa-mem2-2.2.1_x64-linux/

RUN curl -L https://github.com/broadinstitute/gatk/releases/download/4.2.6.1/gatk-4.2.6.1.zip -o gatk-4.2.6.1.zip &&\
    unzip gatk-4.2.6.1.zip &&\
    mv gatk-4.2.6.1/gatk /usr/bin &&\
    mv gatk-4.2.6.1/gatk-package-4.2.6.1-local.jar /root/ &&\
    rm -rf gatk-4.2.6.1.zip gatk-4.2.6.1

ENV GATK_LOCAL_JAR "/root/gatk-package-4.2.6.1-local.jar"

RUN apt-get install libz-dev libncurses-dev libbz2-dev liblzma-dev libcurl4-openssl-dev -y
RUN curl -L https://github.com/samtools/samtools/releases/download/1.15.1/samtools-1.15.1.tar.bz2 -o samtools-1.15.1.tar.bz2 &&\
    tar -xjvf samtools-1.15.1.tar.bz2 &&\
    cd samtools-1.15.1 &&\
    make &&\
    mv samtools /usr/bin &&\
    cd ~ &&\
    rm -rf samtools-1.15.1

RUN curl -L https://github.com/broadinstitute/picard/releases/download/2.26.10/picard.jar -o /root/picard.jar
RUN apt-get install r-base -y

COPY nf-redun-06 /root/nf-redun-06

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
