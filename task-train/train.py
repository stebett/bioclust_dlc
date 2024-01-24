import deeplabcut

config_path = "automatically filled, do not change"

deeplabcut.create_training_dataset(config_path, augmenter_type='imgaug')
deeplabcut.train_network(config_path)
