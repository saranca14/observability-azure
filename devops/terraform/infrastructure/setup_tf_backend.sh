#!/bin/bash

# Set variables
RESOURCE_GROUP="monitoring-bench"
LOCATION="westeurope"
STORAGE_ACCOUNT="gftoteltfstate2025"  # Must be globally unique
CONTAINER_NAME="tfstatestore"
TABLE_NAME="tfstatelock"
BACKEND_FILE="backend.tf"

# Function to check if a resource exists
resource_exists() {
    local result=$($1)
    if [[ -z "$result" || "$result" == "null" ]]; then
        return 1  # Resource does not exist
    else
        return 0  # Resource exists
    fi
}

# Log in to Azure if not already logged in
echo "Checking Azure login..."
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Not logged in. Logging in now..."
    az login --output none
fi

# Check & Create Resource Group
echo "Checking resource group: $RESOURCE_GROUP ..."
resource_exists "az group show --name $RESOURCE_GROUP --query name --output tsv"
if [ $? -ne 0 ]; then
    echo "Creating resource group: $RESOURCE_GROUP ..."
    az group create --name $RESOURCE_GROUP --location $LOCATION --output none
else
    echo "Resource group already exists."
fi

# Check & Create Storage Account
echo "Checking storage account: $STORAGE_ACCOUNT ..."
resource_exists "az storage account show --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query name --output tsv"
if [ $? -ne 0 ]; then
    echo "Creating storage account: $STORAGE_ACCOUNT ..."
    az storage account create \
      --name $STORAGE_ACCOUNT \
      --resource-group $RESOURCE_GROUP \
      --location $LOCATION \
      --sku Standard_LRS \
      --encryption-services blob \
      --allow-blob-public-access false \
      --output none
else
    echo "Storage account already exists."
fi

# Get Storage Account Key
echo "Fetching storage account key..."
STORAGE_KEY=$(az storage account keys list \
  --resource-group $RESOURCE_GROUP \
  --account-name $STORAGE_ACCOUNT \
  --query '[0].value' --output tsv)

# Check & Create Storage Container with Azure AD login
echo "Checking storage container: $CONTAINER_NAME ..."
resource_exists "az storage container show --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --auth-mode login --query name --output tsv"
if [ $? -ne 0 ]; then
    echo "Creating storage container: $CONTAINER_NAME ..."
    az storage container create \
      --name $CONTAINER_NAME \
      --account-name $STORAGE_ACCOUNT \
      --auth-mode login \
      --output none
else
    echo "Storage container already exists."
fi

# Check & Create Table for Terraform State Locking with Azure AD login
echo "Checking storage table: $TABLE_NAME ..."
TABLE_EXISTS=$(az storage table list \
  --account-name $STORAGE_ACCOUNT \
  --auth-mode login \
  --query "[?name=='$TABLE_NAME'].name" --output tsv)

if [ -z "$TABLE_EXISTS" ]; then
    echo "Creating state locking table: $TABLE_NAME ..."
    az storage table create \
      --name $TABLE_NAME \
      --account-name $STORAGE_ACCOUNT \
      --auth-mode login \
      --output none
else
    echo "State locking table already exists."
fi

# Create the backend.tf file with the correct configuration
echo "Generating backend configuration in $BACKEND_FILE..."

cat <<EOL > $BACKEND_FILE
terraform {
  backend "azurerm" {
    resource_group_name   = "$RESOURCE_GROUP"
    storage_account_name  = "$STORAGE_ACCOUNT"
    container_name        = "$CONTAINER_NAME"
    key                   = "terraform.tfstate"
  }
}
EOL

# Output the contents of the backend.tf file
echo "Terraform backend configuration generated in $BACKEND_FILE:"
cat $BACKEND_FILE

echo "Terraform backend setup complete."
