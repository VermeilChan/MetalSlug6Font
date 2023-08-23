#!/bin/bash
pyinstaller --noconfirm --onedir --console --icon "Assets/Sv-001.ico" --name "MetalSlugFont" --add-data "color.py" --add-data "main.py" --add-data "Assets;Assets/"  "terminal.py"
