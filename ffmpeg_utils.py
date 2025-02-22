import subprocess
import signal
import os
import threading
from config import FFMPEG_PATH,SCREEN_FPS
from input_logger import EventLogger


class ScreenRecorder:
    def __init__(self, ffmpeg_path=FFMPEG_PATH):
        self.ffmpeg_path = ffmpeg_path
        self.process = None
        self.logger = EventLogger()
        self._stop_flag = threading.Event()

    def get_screen_capture_format(self):
        return 'gdigrab' if os.name == 'nt' else 'x11grab'

    def get_screen_input_source(self):
        return 'desktop' if os.name == 'nt' else ':0.0'

    def record_screen(self, output_file, fps=30):
        self._stop_flag.clear()

        command = [
            self.ffmpeg_path,
            "-y",
            "-f", self.get_screen_capture_format(),
            "-framerate", str(fps),
            "-i", self.get_screen_input_source(),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-pix_fmt", "yuv420p",
            output_file
        ]

        try :
            # Start FFmpeg process
            self.process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            threading.Timer(1,self.check_recording_status).start()
        except Exception as e:
            print(f"❌ Error starting recording: {e}")



    def stop_recording(self):
        if self.process:
            print("Stopping recording...")

            if os.name == 'nt':
                # Windows: Send Ctrl+Break to the process group
                os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)
            else:
                # Linux/macOS: Send SIGINT (Ctrl+C)
                self.process.send_signal(signal.SIGINT)

            self.process.wait(timeout=5)  # Wait for FFmpeg to exit
            print("✅ Recording stopped successfully!")
            self.logger.stop_logging()
            print("✅ Logger stopped successfully!")

    def is_recording(self):
        return self.process and self.process.poll() is None

    def check_recording_status(self):
        if self.is_recording():
            print("🎥 Recording started successfully! Logger can begin.")
            self.logger.start_logging()
            print("🎥 Logger started successfully!")

        else:
            print("❌ Recording failed to start. Please check FFmpeg configuration.")




# # Example Usage
# recorder = ScreenRecorder()
#
#
# recorder.record_screen("recordings/output.mp4",SCREEN_FPS)
#
# input("Press Enter to stop recording...\n")
# recorder.stop_recording()
