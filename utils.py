import logging
import os.path as osp
import numpy as np
from hydra.utils import get_original_cwd

from omegaconf import OmegaConf


def get_logger(name):
    hydra_conf = OmegaConf.load(".hydra/hydra.yaml")
    dict_config = OmegaConf.to_container(hydra_conf.hydra.job_logging, resolve=True)
    logging.config.dictConfig(
        dict_config
    )

    logger = logging.getLogger(name)

    return logger

def load_stopwords():
    stopwords_set = set()
    cwd = get_original_cwd()
    with open(osp.join(cwd, "stopwords.txt"), "r", encoding="utf-8") as f:
        for word in f:
            word = word.replace("\n", "").replace("\r\n", "")
            stopwords_set.add(word)

    return list(stopwords_set)

def norm(data:np.array, dim:int):
    data /= (np.sum(data, axis=dim, keepdims=True) + 1e-8)
    return data
