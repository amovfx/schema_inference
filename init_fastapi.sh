#!/bin/bash

# Define the base directory
BASE_DIR="./"

# Create the app structure
mkdir -p "${BASE_DIR}/app/api/v1/endpoints"
mkdir -p "${BASE_DIR}/app/core"
mkdir -p "${BASE_DIR}/app/models"
mkdir -p "${BASE_DIR}/app/schemas"
mkdir -p "${BASE_DIR}/app/services"
mkdir -p "${BASE_DIR}/app/db"
mkdir -p "${BASE_DIR}/tests/api"

# Create __init__.py files to make Python treat directories as modules
find "${BASE_DIR}" -type d -exec touch {}/__init__.py \;

# Create other Python files
# touch "${BASE_DIR}/app/api/v1/endpoints/users.py"
# touch "${BASE_DIR}/app/api/v1/endpoints/items.py"
# touch "${BASE_DIR}/app/core/config.py"
# touch "${BASE_DIR}/app/models/user.py"
# touch "${BASE_DIR}/app/models/item.py"
# touch "${BASE_DIR}/app/schemas/user.py"
# touch "${BASE_DIR}/app/schemas/item.py"
# touch "${BASE_DIR}/app/services/user_service.py"
# touch "${BASE_DIR}/app/services/item_service.py"
# touch "${BASE_DIR}/app/db/database.py"
# touch "${BASE_DIR}/tests/api/test_users.py"
# touch "${BASE_DIR}/tests/api/test_items.py"

# Create main.py and requirements.txt at the root of the app
touch "${BASE_DIR}/main.py"
touch "${BASE_DIR}/requirements.txt"

echo "FastAPI project structure created in ${BASE_DIR}"