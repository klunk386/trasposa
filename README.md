# Trasposa

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)
![Made with Luna](https://img.shields.io/badge/Made_with-Luna-magenta)
![Version](https://img.shields.io/badge/version-1.0.0-orange)
[![Tests](https://github.com/your-username/trasposa/actions/workflows/tests.yml/badge.svg)](https://github.com/your-username/trasposa/actions)
[![PyPI](https://img.shields.io/pypi/v/trasposa.svg)](https://pypi.org/project/trasposa/)

**Trasposa** is a lightweight Python tool that allows users to modify the pitch
and playback speed of audio files without affecting audio quality. It also
includes volume normalization and the ability to play the result directly from
the command line, with support for real-time interruption.

Trasposa is designed for musicians, educators, language learners, and anyone
working with audio who needs flexible, high-quality pitch and speed control.

---

## Features

- Pitch shifting in semitones (up or down)
- Time-stretching (speed up or slow down without pitch change)
- Volume normalization to prevent loudness issues
- Direct audio playback with the ability to stop with a keypress
- Command-line interface and callable Python function
- Cross-platform (Linux, macOS, Windows)

---

## Installation

Python 3.7 or higher is required.

### Using pip (recommended for end users)

```bash
pip install git+https://github.com/your-username/trasposa.git
```

### From source

Clone this repository and install with pip:

```bash
git clone https://github.com/your-username/trasposa.git
cd trasposa
pip install .
```

---

## Usage

### From the command line

```bash
trasposa input.mp3 -s -2 -v 0.9
```

**Arguments:**

- `input.mp3`: input audio file (WAV or MP3)
- `-s, --semitones`: number of semitones to transpose (e.g., `-2`)
- `-v, --speed`: playback speed factor (e.g., `0.9` slows down)
- `-o, --output`: path to output file (if omitted, plays the result)
- `--no-normalize`: disables volume normalization

**Example:**

Save the modified file:
```bash
trasposa song.mp3 -s -3 -v 1.1 -o modified.wav
```

Play the modified file directly:
```bash
trasposa song.mp3 -s 2
```

During playback, press **Q** to stop the audio.

> On macOS, you may need to grant Accessibility permissions to your terminal
> in System Settings → Privacy & Security → Accessibility.

---

## As a Python module

You can also use Trasposa in your own Python code or Jupyter notebooks:

```python
from trasposa import trasposa

# Apply pitch shift and speed change, then play the result
trasposa("song.mp3", semitones=-1, speed=0.95)
```

---

## License

This project is licensed under the **GNU General Public License v3.0**  
See the [LICENSE](LICENSE) file for details.

---

## Author

Valerio Poggi  
with development support from **Luna**
