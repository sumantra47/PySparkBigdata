#!/bin/bash
set -e

DB_USERNAME=$(gcloud secrets versions access latest --secret=db-username)
DB_PASSWORD=$(gcloud secrets versions access latest --secret=db-password)

# Store in a secure, non-world-readable env file
echo "export DB_USERNAME='$DB_USERNAME'" >> /etc/profile.d/db-env.sh
echo "export DB_PASSWORD='$DB_PASSWORD'" >> /etc/profile.d/db-env.sh

chmod 600 /etc/profile.d/db-env.sh