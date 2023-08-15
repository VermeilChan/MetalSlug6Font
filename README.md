# Metal Slug Font

Generate images with the iconic Metal Slug font style! Write text using the distinctive font from the Metal Slug arcade game series. This tool allows you to create images of your text with custom spacing and supports characters, numbers, and symbols.

**Important Note:** This version of the software is still in its developmental phase and operates within a terminal-based interface. Please be aware that it might require certain adjustments to ensure proper functionality across various operating systems, including Linux and macOS. Given its early stage of development, there are currently several bugs present within the system. It is highly recommended to exercise caution and refrain from trying out this version until further refinements have been made. Alternatively, you can continue to utilize the web application until the official website becomes accessible. In case the website isn't available, you have the option to host the application on your own computer. Detailed instructions can be found in the README.md file on the master branch for additional information.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- - [Installing Python](#installing-python)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Converting to Executable](#converting-to-executable)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Features

- Convert text into images with the Metal Slug font style.
- Customize spacing between characters for creative layouts.
- Support for uppercase and lowercase alphabets (A-Z, a-z), numbers (1-9), exclamation (!), and question marks (?).

## Examples

Input: `I Love Cats!`

Generated Image:

![Metal Slug Font Image](image/Example.png)

## Requirements

Make sure you have Python installed. You can download Python from the official Python website:

- [Python Downloads](https://www.python.org/downloads/)

## Installing Python On Linux

- [Installing Python On Linux](https://docs.python-guide.org/starting/install3/linux/)

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/VermeilChan/MetalSlugFont.git
   ```
   ```
   cd MetalSlugFont
   ```

2. Install the required Python packages:

   ```bash
   pip install Flask Pillow pyinstaller
   ```

3. Run the Metal Slug Font:

   ```bash
   python app.py
   ```

4. Follow the on-screen instructions to generate Metal Slug font images.

## Usage

1. Enter the desired text to convert into Metal Slug font style.
2. The generated image will be saved in the `Assets/Generated_Images` folder.

## Converting to Executable

If you want to convert the terminal-based script into an executable (.exe) for Windows, you might want to consider using Wine. Wine allows you to run Windows applications on Linux.

Here are guides for installing and setting up Wine on various Linux distributions:

- Ubuntu: [WineHQ Ubuntu Guide](https://wiki.winehq.org/Ubuntu)
- Debian: [WineHQ Debian Guide](https://wiki.winehq.org/Debian)
- Fedora: [WineHQ Fedora Guide](https://wiki.winehq.org/Fedora)

Please note that Wine might have limitations and not all Windows applications work flawlessly under it. Be sure to test your executable thoroughly.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

- [GussPrint](https://www.spriters-resource.com/submitter/Gussprint/)
