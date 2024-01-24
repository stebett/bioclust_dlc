import deeplabcut


config_path = "automatically filled, do not change"
video_name = "fill this with the video name (not the full path)"

video_path  = Path(config_path).parent / "videos" / video_name

deeplabcut.create_labeled_video(config_path, video_path, filtered=True, save_frames = True, trailpoints=0)
