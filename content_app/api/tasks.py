import subprocess
from pathlib import Path
from django.conf import settings

def convert_video_to_hls(source, video_id):
    """
    Convert a video file to HLS (HTTP Live Streaming) format at 720p resolution.

    Args:
        source (str or Path): Path to the source video file.
        video_id (str): Unique identifier for the output directory/manifest.

    Returns:
        Path: Path to the generated HLS manifest (.m3u8) file.
    """
    source_path = Path(source)
    output_dir = Path(settings.MEDIA_ROOT) / "videos" / str(video_id) / "720p"
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = output_dir / "index.m3u8"
    segment_path = output_dir / "000.ts"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(source_path),
        "-s", "hd720",
        "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-ar", "48000",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", str(segment_path),
        str(manifest_path),
    ]

    subprocess.run(cmd, capture_output=True)

    return manifest_path

def thumbnail_video(source, video_id):
    """
    Generate a thumbnail from a video file using FFmpeg.

    Args:
        source (str or Path): Path to the source video.
        video_id (str): Identifier for the output filename.

    Returns:
        Path: Path to the generated thumbnail image.
    """
    source_path = Path(source)
    output_dir = Path(settings.MEDIA_ROOT) / "thumbnails"
    output_dir.mkdir(parents=True, exist_ok=True)

    thumbnail_path = output_dir / f"{video_id}_thumbnail.jpg"

    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:01.000",
        "-i", str(source_path),
        "-vframes", "1",
        str(thumbnail_path),
    ]

    subprocess.run(cmd, capture_output=True)

    return thumbnail_path
