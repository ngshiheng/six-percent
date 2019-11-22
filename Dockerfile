FROM ubuntu:18.04
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv python3-pip 

# Installing chromedriver
RUN apt-get install -y chromium-chromedriver

# Handling emojis (or other Unicode characters)
RUN apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Virtual environment
ENV VIRTUAL_ENV=./venv-six-percent
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
COPY . .
RUN ls -al
RUN pip3 install -r requirements.txt

# Run the application
CMD ["./run.sh"]