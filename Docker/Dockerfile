FROM python:3.10 AS build-stage

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev \
    python3-pip

WORKDIR /AddressVerification
ADD . /AddressVerification

RUN pip3 install -r requirements.txt

FROM python:3.10-slim as run-time
ARG TAG=dev
ENV BUILD_TAG=$TAG

RUN apt update -y && apt upgrade -y && apt install -y \
    build-essential \
    libffi-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev \
    python3-httptools
COPY --from=build-stage /AddressVerification /AddressVerification
WORKDIR /AddressVerification
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
