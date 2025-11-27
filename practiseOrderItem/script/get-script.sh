#!/bin/bash

DB_USER=$(gcloud secrets versions access latest --secret=db-username)
DB_PASS=$(gcloud secrets versions access latest --secret=db-password)

echo "DB_USERNAME=$DB_USER" | sudo tee /etc/secrets.env
echo "DB_PASSWORD=$DB_PASS" | sudo tee -a /etc/secrets.env

sudo chmod 755 /etc/secrets.env