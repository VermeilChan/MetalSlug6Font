# Metal Slug Font

Generate images with the iconic Metal Slug font style! Write text using the distinctive font from the Metal Slug arcade game series. This tool allows you to create images of your text with custom spacing and supports characters, numbers, and symbols.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- - [Installing Python on Linux](#installing-python-on-linux)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Features

- Convert text into images with the Metal Slug font style.
- Customize spacing between characters for creative layouts.
- Support for (A to Z), numbers (1 to 9), exclamation (!), and question marks (?).

## Examples

Input: `I Love Cats!`

Generated Image:

![Metal Slug Font Image](image/Example.png)

## Requirements

Make sure you have Python installed. You can download Python from the official Python website:

- [Python Downloads](https://www.python.org/downloads/)

## Installing Python on Linux

- [Installing Python 3 on Linux](https://docs.python-guide.org/starting/install3/linux/)

## Getting Started

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/VermeilChan/MetalSlugFont.git
   
   cd MetalSlugFont
   ```

2. Install the required Python packages:

   ```bash
   pip install Flask Pillow
   ```

3. Place your character images (A.png, B.png, ..., question.png, exclamation.png) in the `static` directory.

4. Start the Flask web app:

   ```bash
   python app.py
   ```

5. Access the web app in your browser at `http://127.0.0.1:5000/`.

## Usage

1. Enter the desired text in the input box.
2. Press the "Generate" button to create an image with the custom font based on the provided character images.
3. The generated image will be displayed, showcasing the input text in the custom font.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

- [GussPrint](https://www.spriters-resource.com/submitter/Gussprint/)
