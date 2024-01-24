import deeplabcut
import datetime
from pathlib import Path

config_path = "automatically filled, do not change"

subject = "sb007"
cam = "cam_1"

start = datetime.datetime.strptime("2022-11-16", "%Y-%m-%d")
end = datetime.datetime.strptime("2022-12-12", "%Y-%m-%d")
date_all = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
ephys_root = Path("/import/kg_nbcws28/bettani/sb007")



block_all = []
for date_unformatted in date_all:
    date = date_unformatted.strftime("%Y-%m-%d")
    session = "_".join([subject, date])
    block_generator = (ephys_root / session).glob("block_*")
    for block in block_generator:
        block_all.append(block)

videos_nested = list([list((block / "video" / "preprocess").glob("*cam_1_*.mp4")) for block in block_all])
videos = [str(item) for sublist in videos_nested for item in sublist]


# deeplabcut.analyze_videos(config_path, videos, save_as_csv=True)
deeplabcut.filterpredictions(config_path, videos, videotype='.mp4',filtertype= 'arima',ARdegree=5,MAdegree=2)
deeplabcut.plot_trajectories(config_path, videos)
