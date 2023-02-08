import logging
import pathlib

# https://stackoverflow.com/questions/18786912/get-output-from-the-logging-module-in-ipython-notebook

def get_logger():
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='bike_share.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    return logger

def get_data_path():
    return pathlib.Path(pathlib.Path(__file__).parent.resolve() / ".." / "data/")
