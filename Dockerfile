# Base image selection
FROM ubuntu:latest

# Turn off interactive mode during the initial building
ENV DEBIAN_FRONTEND noninteractive

# General user settings
ENV USER=cs348
ENV HOME=/home/${USER}

ENV MYSQL_DATABASE=testDB
ENV MYSQL_USER=group8
ENV MYSQL_PASSWORD=Password0!

# Install python 3.10 and pip
RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt

# Install MySQL
RUN apt-get install -y mysql-server mysql-client

# Install vim editor
RUN apt-get install -y vim

# Install Python-MySql db setup dep
RUN apt-get install -y libmysqlclient-dev

# Set home directory
WORKDIR ${HOME}

# Add MySQL service initialization script for interactive mode
RUN echo "service mysql start 1> /dev/null 2> /dev/null" >> ${HOME}/.bashrc

# Start MySQL service
RUN service mysql start&& \
    mysql -e "CREATE DATABASE $MYSQL_DATABASE;" && \
    mysql -e "CREATE USER '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD';" && \
    mysql -e "GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost';" && \
    mysql -e "ALTER USER '$MYSQL_USER'@'localhost' IDENTIFIED WITH mysql_native_password BY '$MYSQL_PASSWORD';"

# Expose MySQL port
EXPOSE 3306 5000

# Copy requirements first (for caching)
COPY requirements.txt requirements.txt

# Install virtualenv
RUN pip install virtualenv

# Create venv
RUN virtualenv venv

# activate virtualenv and install requirements
RUN . venv/bin/activate && pip install -r requirements.txt && \
    pip install mysqlclient

# Copy scripts
COPY scripts/setup.sh scripts/setup.sh

# Run project setup script
RUN chmod a+x ${HOME}/scripts/setup.sh
RUN echo "source ${HOME}/scripts/setup.sh" >> ${HOME}/.bashrc

# Copy every files
COPY . .

# Set the entrypoint to bash
ENTRYPOINT ["bash"]

# # Set CMD
# CMD ["python3.10", "-m", "flask", "run", "--host=0.0.0.0"]