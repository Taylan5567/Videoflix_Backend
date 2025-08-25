import subprocess
from pathlib import Path
from django.conf import settings

import subprocess
from pathlib import Path
from django.conf import settings

def convert_video_to_hls(source, video_id):
    """
    Convert a video into HLS at 480p, 720p, and 1080p and write a master playlist.

    The outputs are written under:
        MEDIA_ROOT/videos/<video_id>/{480p,720p,1080p}/index.m3u8
        MEDIA_ROOT/videos/<video_id>/master.m3u8

    Parameters
    ----------
    source : str | Path
        Absolute path to the input video file.
    video_id : int
        Identifier used for the output directory.

    Returns
    -------
    Dict[str, Path]
        Mapping of resolution folder names (e.g., "480p") and "master" to the
        corresponding filesystem paths of the generated playlists.

    Raises
    ------
    RuntimeError
        If ffmpeg fails for any rendition.
    """
    source_path = Path(source)
    base_output_dir = Path(settings.MEDIA_ROOT) / "videos" / str(video_id)

    resolutions = {
        "480p": "480",
        "720p": "720",
        "1080p": "1080",
    }

    manifest_paths = {}

    for folder_name, height in resolutions.items():
        output_dir = base_output_dir / folder_name
        output_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = output_dir / "index.m3u8"
        segment_pattern = output_dir / "segment_%03d.ts"

        cmd = [
            "ffmpeg", "-y",
            "-i", str(source_path),
            "-vf", f"scale=-2:{height}",
            "-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-ar", "48000",
            "-hls_time", "4",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", str(segment_pattern),
            str(manifest_path),
        ]

        subprocess.run(cmd, capture_output=True)
        manifest_paths[folder_name] = manifest_path

    master_path = base_output_dir / "master.m3u8"
    with open(master_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")

        f.write('#EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=854x480\n')
        f.write("480p/index.m3u8\n")
        f.write('#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\n')
        f.write("720p/index.m3u8\n")
        f.write('#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n')
        f.write("1080p/index.m3u8\n")

    manifest_paths["master"] = master_path
    return manifest_paths


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
