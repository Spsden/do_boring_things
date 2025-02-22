import argparse
from ffmpeg_utils import  ScreenRecorder
from datetime import datetime
from config import SCREEN_FPS
import threading


def generate_filename():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"recordings/screen_recording_{timestamp}.mp4"

def main():
    parser = argparse.ArgumentParser(description="Desktop Recording CLI")
    parser.add_argument("--record", action="store_true", help="Record the desktop screen")
    parser.add_argument("--convert", type=str, help="Convert video format (e.g., avi, mkv)")
    parser.add_argument("--extract-audio", action="store_true", help="Extract audio from video")

    args = parser.parse_args()

    if args.record:
        print("Recording screen...")
        try:
            recorder = ScreenRecorder()
            file_name = generate_filename()
            print("Recording: "+ file_name)
            recorder.record_screen("recordings/output2.mp4", SCREEN_FPS)



            input("Press Enter to stop recording...\n")
            recorder.stop_recording()

        except Exception as e:
            print(f"Recording failed: {str(e)}")

    # if args.convert:
    #     print(f"Converting video to {args.convert} format...")
    #     convert_video("recordings/screen_capture.mp4", f"recordings/output.{args.convert}")
    #
    # if args.extract_audio:
    #     print("Extracting audio...")
    #     extract_audio("recordings/screen_capture.mp4", "recordings/audio.mp3")

if __name__ == "__main__":
    main()
