#!/bin/bash

# Check if iconutil is available
if ! command -v iconutil &> /dev/null; then
    echo "iconutil command not found. Please ensure you are running on macOS."
    exit 1
fi

# Check if the input ICO file exists
if [ ! -f "icon.ico" ]; then
    echo "Input ICO file 'icon.ico' not found in the current directory."
    exit 1
fi

# Create an icon.iconset directory
mkdir -p icon.iconset

# Convert the ICO file to PNG
sips -s format png icon.ico --out icon.iconset/icon_16x16.png
sips -s format png icon.ico --out icon.iconset/icon_32x32.png
sips -s format png icon.ico --out icon.iconset/icon_128x128.png
sips -s format png icon.ico --out icon.iconset/icon_256x256.png
sips -s format png icon.ico --out icon.iconset/icon_512x512.png

# Create the icon.icns file from the icon.iconset directory
iconutil -c icns -o icon.icns icon.iconset

# Clean up the temporary icon.iconset directory
rm -rf icon.iconset

echo "Conversion completed: icon.icns created."
