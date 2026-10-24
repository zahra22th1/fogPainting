<img width="1500" height="364" alt="Foggy Glass Drawing Interface-100kb (1)" src="https://github.com/user-attachments/assets/1516723f-9c28-46d3-9687-707bca9671b7" />


# Foggy Glass 💧

A virtual foggy glass experience built with Python, OpenCV, and MediaPipe. Use your hand gestures to wipe away fog, reveal the webcam image, and restore the fog like drawing on a misty window.

## Features

- Wipe away fog using hand gestures.
- Restore fog using hand gestures.
- Adjust brush thickness while running.
- Reset the screen at any time.
- Simulated fog texture, water droplets, and glass streaks.

## Requirements

- Python 3.12
- A working webcam
- OpenCV
- NumPy
- MediaPipe

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Or download the project and open its folder.

### 2. Create a virtual environment

```bash
py -3.12 -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**or cmd:**
```
.venv\Scripts\activate.bat
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install mediapipe==0.10.21 opencv-python numpy
```

## Usage

Run the application:

```bash
python virtual_paint.py
```

Allow access to your webcam if prompted.

### Hand Controls

| Gesture | Action |
|---|---|
| Raise your index finger | Wipe away fog |
| Raise your pinky finger | Restore fog |

Keep your index finger raised and your pinky lowered when wiping the fog.

### Keyboard Controls

| Key | Action |
|---|---|
| `+` or `=` | Increase brush thickness |
| `-` | Decrease brush thickness |
| `C` | Cover the screen with fog again |
| `Q` | Quit the application |

## Troubleshooting

- **Webcam not detected:** Make sure your camera is connected and available to other applications.
- **Module not found:** Activate the virtual environment and install the dependencies.
- **MediaPipe installation issues:** Make sure you are using Python 3.12 and the specified MediaPipe version.

## License

This project is for learning and personal use. Add a license file if you plan to distribute it publicly.
