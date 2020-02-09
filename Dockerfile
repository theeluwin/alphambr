# opencv
FROM jjanzic/docker-python3-opencv:latest
LABEL maintainer="Jamie Seol <theeluwin@gmail.com>"

# init
RUN mkdir -p /workspace
WORKDIR /workspace

# install packages
RUN pip3 install numpy argparse tqdm scikit-image

# run
ENTRYPOINT []
CMD ["python3", "example.py"]
