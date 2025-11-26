#!/bin/bash
set -eux

# Update packages
sudo apt-get update -y

# Install Python MySQL connector
pip install --upgrade pip
pip install mysql-connector-python

# Correct JDBC Connector URL
MYSQL_JAR_URL="https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar"

# Download JDBC driver to Spark jars directory
sudo wget -O /usr/lib/spark/jars/mysql-connector.jar "$MYSQL_JAR_URL"

echo "MySQL JDBC + Python connector installed successfully."
