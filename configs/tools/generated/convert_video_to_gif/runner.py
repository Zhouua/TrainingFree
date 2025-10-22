import subprocess
from pathlib import Path


class ConvertVideoToGif:
    def convert_video_to_gif(self, input_path: str, output_path: str = None) -> str:
        """Convert a video file to GIF format

        Args:
            input_path (str): Path to the input video file
            output_path (str, optional): Path to save the output GIF. Defaults to None.
        """
        if not Path(input_path).exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if output_path is None:
            output_path = Path(input_path).with_suffix(".gif")

        try:
            cmd = ["ffmpeg", "-i", input_path, "-vf", "fps=10,scale=320:-1:flags=lanczos", "-c:v", "gif", output_path]
            subprocess.run(cmd, check=True, capture_output=True)
            return f"Converted video to GIF: {output_path}"
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}") from e
