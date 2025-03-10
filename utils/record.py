import sounddevice as sd
import wave

from utils.api_client import APIClient
class Recording:
    def __init__(self, api_client: APIClient, filename="output/output.wav", sample_rate=44100, channels=1):
        """
        Initializes the Recording object with audio parameters.

        Args:
            filename (str): Name of the output WAV file.
            sample_rate (int): Audio sample rate (default is 44100 Hz).
            channels (int): Number of audio channels (default is 1 for mono).
        """
        self.api_client = api_client
        self.filename = filename
        self.sample_rate = sample_rate
        self.channels = channels
        self.is_recording = False
        self.frames = []
        self.stream = None

    def start_recording(self):
        """Starts the recording process."""
        print("Recording started. Press 'Ctrl + Alt + R' again to stop.")
        self.is_recording = True
        self.frames = []  # Clear frames for a new recording

        # Callback to collect audio chunks
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.tobytes())

        # Open the audio stream
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback,
            dtype="int16"
        )
        self.stream.start()

    def stop_recording(self)->str:
        """Stops the recording process and saves the audio to a file."""
        print("Stopping recording...")
        self.is_recording = False
        self.stream.stop()
        self.stream.close()
        self.stream = None

        # Save the recording to a WAV file
        try:
            with wave.open(self.filename, "wb") as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 2 bytes for 'int16'
                wf.setframerate(self.sample_rate)
                wf.writeframes(b"".join(self.frames))
            print(f"Audio saved as {self.filename}")
            return self.api_client.transcribe_audio(self.filename)

        except Exception as e:
            print(f"Error saving audio: {e}")
            return "Error saving or transcribing the audio!"