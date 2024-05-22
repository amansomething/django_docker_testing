#!/bin/bash

# Function to generate a 64-character password. Newline, $, and = characters are removed.
# The result is enclosed in double quotes.
generate_password() {
  var_name=$1
  echo "$var_name=\"$(openssl rand -base64 64 | tr -d '\n$=' | cut -c -64)\""
}

# List of required password variables
required_pw_vars=(\
"DJANGO_SECRET_KEY"
"ANOTHER_SECRET_KEY"
"YET_ANOTHER_SECRET_KEY"
)

# List of other required variables
required_vars=(
"DATABASE_URL"
"REDIS_URL"
"SOME_OTHER_VAR"
)

# Create .env file if it doesn't exist
touch .env

# Check and generate required password variables if not already present
for var in "${required_pw_vars[@]}"; do
  if ! grep -q "^$var=" .env || [ "$(grep "^$var=" .env | cut -d '=' -f 2 | wc -c)" -lt 64 ]; then
    echo "Generating $var"
    sed -i "/^$var=/d" .env
    echo $(generate_password $var) >> .env
  fi
done

# Boolean to track if missing required variables
missing_vars=false

# Check if other required variables exist and have values
for var in "${required_vars[@]}"; do
  if ! grep -q "^$var=" .env || [ -z "$(grep "^$var=" .env | cut -d '=' -f 2)" ]; then
    echo "Error: $var is not set or has no value in .env"
    missing_vars=true
  fi
done

# Check if there were any errors
if [ "$missing_vars" = true ]; then
  echo "Missing required variables in the .env file. Stopping..."
  exit 1
else
  echo "All required variables are set."
fi

echo "Starting the application..."

# Execute the command passed to the entrypoint script
exec "$@"
