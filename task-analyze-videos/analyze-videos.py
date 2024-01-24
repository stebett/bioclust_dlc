import deeplabcut

config_path = "automatically filled, do not change"

videos = "/import/kg_nbcws28/bettani/deeplabcut/5_points_tracking_cam_2-sb007-2023-02-28/videos"

deeplabcut.analyze_videos(config_path, videos, save_as_csv=True)
deeplabcut.filterpredictions(config_path, videos)
deeplabcut.plot_trajectories(config_path, videos)
