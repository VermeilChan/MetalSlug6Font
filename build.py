import subprocess

def build_metal_slug_font():
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--console",
        "--icon", "Assets/Sv-001.ico",
        "--name", "MetalSlugFont",
        "--add-data", "color.py;.",
        "--add-data", "main.py;.",
        "--add-data", "Assets;Assets/",
        "terminal.py"
    ]

    try:
        subprocess.run(cmd, check=True)
        print("Build successful.")
    except subprocess.CalledProcessError:
        print("Build failed.")

if __name__ == "__main__":
    build_metal_slug_font()
