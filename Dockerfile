## Golang image for some modules
FROM golang:1.18.1-bullseye as go-build
       
# Install packages
RUN go install github.com/lc/gau/v2/cmd/gau@latest \
    && go install github.com/tomnomnom/waybackurls@latest\
    && go install github.com/tomnomnom/qsreplace@latest\
    && go install github.com/takshal/freq@latest\
    && cp $GOPATH/bin/* /usr/local/bin/
 

## Pull official base image
FROM python:3.8.11-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install packages
RUN apt-get update \
    && apt-get -y install --no-install-recommends software-properties-common libpq5 python3-dev musl-dev git\
    netcat-traditional golang nmap openvpn freerdp2-x11 tigervnc-viewer apt-utils ca-certificates vim \
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /usr/src/redteam_toolkit/

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/redteam_toolkit/entrypoint.sh
RUN chmod +x /usr/src/redteam_toolkit/entrypoint.sh

# copy project
COPY . .
COPY --from=go-build /usr/local/bin/gau /usr/local/bin/ /usr/local/bin/waybackurls /usr/local/bin/qsreplace /usr/local/bin/freq\
 /usr/src/redteam_toolkit/toolkit/scripts/webapp/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/redteam_toolkit/entrypoint.sh"]
