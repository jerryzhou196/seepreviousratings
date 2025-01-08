#!/bin/zsh

# Name of the addon package
ADDON_NAME="seepreviousratings"

# Clean up any existing addon file
if [ -f "${ADDON_NAME}.ankiaddon" ]; then
    rm "${ADDON_NAME}.ankiaddon"
fi

# Required files for the addon
FILES=(
    "manifest.json"
    "config.json"
    "config.md"
    "__init__.py"
)

# Check if all required files exist
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "Error: Required file '$file' not found!"
        exit 1
    fi
done

# Create the addon package
zip "${ADDON_NAME}.ankiaddon" "${FILES[@]}"

# Check if zip was successful
if [ $? -eq 0 ]; then
    echo "Successfully created ${ADDON_NAME}.ankiaddon"
else
    echo "Error: Failed to create addon package"
    exit 1
fi 
