import deeplabcut
import pathlib


config_path = "automatically filled, do not change"
videos  = str(Path(config_path).parent / "videos")

deeplabcut.filterpredictions(config_path, videos, videotype='.mp4',filtertype= 'arima',ARdegree=5,MAdegree=2)
