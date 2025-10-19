# Void Trace

Void Trace is an advanced OSINT and reconnaissance tool built in Python. It is a continuation and evolution of the [DevilEye](https://github.com/kbzx3/devileye-osint-in-developement-will-receive-updates-) project, designed to provide a more user-friendly interface, additional features, and regular updates for tracking emails, phone numbers, and more.

---

## Features

- **Email Tracking** – Quickly gather information about emails and their associated accounts.
- **Phone Lookup** – Parse and validate phone numbers using the `phonenumbers` library.
- **Website Scraping** – Collect public information from websites with `BeautifulSoup`.
- **Terminal Enhancements** – Colorful outputs with `colorama`, ASCII banners with `pyfiglet`, and colored text with `termcolor`.
- **Cross-Platform** – Works on Windows, macOS, and Linux with Python 3.x.
- New features will be added soon

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/kbzx3/void-trace.git
cd void-trace
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the main script:

```bash
python main.py
```

The tool will display a terminal interface with options to perform email tracking, phone lookup, and other reconnaissance features.

---

## Addon Development

Please ensure the name of the main function is the same as the file, for example is the name of thefunction that runs the module is reversesearch then file must be named reversesearch.py .

## Relation to DevilEye

Void Trace is a **continuation of the DevilEye project**. It retains the core OSINT capabilities of DevilEye while adding:

- Better terminal visuals
- Phone number parsing functionality
- Regular updates and bug fixes
- Improved modular code structure

This ensures users can continue leveraging the power of DevilEye with enhanced features and stability.

---

## Updates

Void Trace will receive **regular updates** to include:

- New OSINT modules and tools
- Bug fixes and performance improvements
- Compatibility updates with Python versions
- Security patches for safe usage

Stay tuned by following the repository or checking the [Releases](https://github.com/kbzx3/void-trace/releases) section.

---

## Contributing

Contributions are welcome! You can:

1. Fork the repository
2. Create a new branch for your feature or fix
3. Submit a pull request with your improvements

Please ensure all code follows Python 3 conventions and maintains compatibility with the current modules.

---

## License

Void Trace inherits its license from DevilEye and is **open source under the MIT License**. You are free to use, modify, and distribute it responsibly.

---

## Disclaimer

This tool is intended for **educational and ethical purposes only**. Do not use Void Trace to invade privacy or perform illegal activities. The developers are **not responsible for misuse**.
