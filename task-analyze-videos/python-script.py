import deeplabcut
from pathlib import Path

config_path = "automatically filled, do not change"

videos = str(Path(config_path).parent / "videos")

deeplabcut.analyze_videos(config_path, videos, dynamic=(True,.5,10), save_as_csv=True)
deeplabcut.filterpredictions(config_path, videos)
deeplabcut.plot_trajectories(config_path, videos)
