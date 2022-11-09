#!/usr/bin/python3
import os
import argparse
import subprocess
from typing import List
import math

# Assumed fps of videos
C_FPS = 20


class Frame:
    def __init__(self, lines: List[str]):
        for line in lines:
            line = line.split("=")
            if "pts_time" in line[0]:
                self.pts_time = float(line[1])
            elif line[0] == "key_frame":
                self.key_frame = bool(int(line[1]))
            elif line[0] == "pict_type":
                self.pict_type = line[1]


def get_frames(output: str) -> List[Frame]:
    """
    Given the stdout of ffprobe, make a list of frames.
    """
    all_frames = []
    frame = []
    for line in output.splitlines():
        if not line:
            continue
        # Start of a new frame, reset frame list.
        if line == "[FRAME]":
            frame = []
        # End of a frame, parse into the class
        elif line == "[/FRAME]":
            all_frames += [Frame(frame)]
        # Accumulating frame data
        else:
            frame += [line]

    return all_frames


def frame_breakdown(all_frames: List[Frame]):
    """
    Print I, P, B frames present
    """

    i_frames = len([x for x in all_frames if x.pict_type == "I"])
    p_frames = len([x for x in all_frames if x.pict_type == "P"])
    b_frames = len([x for x in all_frames if x.pict_type == "B"])

    print(
        f"Total frames: {i_frames + p_frames + b_frames}, I frames: {i_frames}, P Frames: {p_frames}, B frames: {b_frames}"
    )


def skipped_frames(all_frames: List[Frame]):
    """
    Looks for skipped and out of order frames
    """
    num_out_of_order = 0
    num_skipped_frames = 0
    last_frame = all_frames[0]
    for frame in all_frames[1:]:
        # Frame out of order
        if frame.pts_time < last_frame.pts_time:
            num_out_of_order += 1
        # Gap in frames
        elif (frame.pts_time - last_frame.pts_time) > (1 / C_FPS):
            num_skipped_frames += min(
                math.ceil((frame.pts_time - last_frame.pts_time) * C_FPS) - 1, 0
            )
        last_frame = frame
    if num_out_of_order > 0:
        print(f"Out of order frames: {num_out_of_order}")
    if num_skipped_frames > 0:
        print(f"Skipped frames: {num_skipped_frames}")


def get_video_stats(video: str):
    """Given the name of a video, get general stats"""
    s = subprocess.run(["ffprobe", "-i", video], capture_output=True, text=True)
    # Note that output comes in stderr instead of stdout
    for line in s.stderr.splitlines():
        if "Duration" in line:
            duration = line.split(",")[0].strip()
            bitrate = line.split(",")[2].strip()
        if "Stream" in line:
            fps = line.split(",")[5].strip()

    print(f"{duration}, {bitrate}, {fps}")


def analyze_video(video: str):
    """
    Analyzes a single video
    """
    assert os.path.exists(video), f"{video} doesn't exist"
    assert os.path.isfile(video), "Not a file"

    print(f"\nAnalyzing: {video}")

    # Run ffprobe to get frame info
    s = subprocess.run(
        ["ffprobe", video, "-show_frames"], capture_output=True, text=True
    )
    # Extract frames
    all_frames = get_frames(s.stdout)

    # Analyze video as a whole
    get_video_stats(video)
    frame_breakdown(all_frames)
    skipped_frames(all_frames)


def main():
    """
    Analyzes a video or a folder of videos using ffmpeg
    """
    parser = argparse.ArgumentParser("Analyzes a video using ffmpeg.")
    parser.add_argument("video", help="Video or directory of videos to check")
    args = parser.parse_args()
    dir = args.video

    if os.path.isfile(dir):
        analyze_video(dir)
    else:
        for f in os.listdir(dir):
            video = os.path.join(dir, f)
            if os.path.isfile(video):
                analyze_video(video)


main()
