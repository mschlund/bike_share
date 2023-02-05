import logging
import pathlib

def get_logger():
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='mylog.log', mode='a')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.INFO)
    return logger

def get_data_path():
    return pathlib.Path(pathlib.Path(__file__).parent.resolve() / ".." / "data/")
