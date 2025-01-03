[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


# 📚 qrcode-lego
Generate an image of a lego qr code for your WiFi network

## 🚀 Table of Contents
1. [About the Project](#-about-the-project)
2. [Installation](#-installation)
3. [Usage](#-usage)
4. [Arguments](#-arguments)
5. [Examples](#-examples)
6. [Sample Output](#-sample-output)
7. [Contributing](#-contributing)
8. [License](#-license)

## 📝 About the Project

This project doesn't do a great deal really, except combine my love of being a nerd with my love of lego.

It's quite simple really, you tell it your WiFi details, it'll give you an image with the qrcode in lego and a list of pieces needed.

The list of pieces is broken down into black and white. Strictly the white pieces aren't necessary, but I think it looks better.

Obviously, feel free to use any 2 contrasting colours, but note that I make no assurances about how readable it will be to a scanner.

## ⚙️ Installation
Ensure you have Python installed (>=3.8). Then, clone the repository and install the dependencies:

```bash
git clone https://github.com/jgfh2/qrcode-lego.git
cd qrcode-lego
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Usage

```bash
python qrcode.py -s MySSID -p MyPassword -S WPA -H -o output.png
```


## 📊 Arguments
| Argument | Short | Description | Default |
| -------- | ----- | ----------- | ------- |
| --ssid | -s | SSID of the WiFi network |  |
| --password | -p | WiFi password |  |
| --security | -S | Security type (WEP, WPA, nopass) | WPA |
| --hidden | -H | Indicates if the network is hidden | False |
| --output | -o | Output file name (must be an image file) | Required |
| --help | -h | Display help message |  |

## 🧩 Examples
Basic Example:

```bash
python qrcode.py -s MyNetwork -p SecretPass123 -o MyOutput.png
```

Advanced Example:

```bash
python qrcode.py -s MyNetwork -p SecretPass123 -S WEP -H -o output.jpg
```

## 📸 Sample Output

![Sample Output](sample.png)

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add some feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for details.