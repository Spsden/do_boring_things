from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
RECORDINGS_DIR = BASE_DIR / "recordings"
LOGS_DIR = BASE_DIR / "logs"

# Ensure directories exist
RECORDINGS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# FFmpeg Config
FFMPEG_PATH = r"C:\Users\prata\Downloads\ffmpeg-7.1-essentials_build\bin\ffmpeg.exe"
SCREEN_FPS = 30
OUTPUT_FILE = RECORDINGS_DIR / "screen_recording.mp4"

# Logging Config
LOG_FILE = LOGS_DIR / "user_actions.json"

RECORDING_FPS = 30
RECORDING_DURATION = 10

