import os.path as osp
import hydra
from hydra.utils import get_original_cwd

from data_builder import Corpus
from plsa import PlsaModel
from utils import load_stopwords


@hydra.main(config_path=".", config_name="config")
def main(cfg):
    cwd = get_original_cwd()

    stopwords = load_stopwords()
    corpus = Corpus(osp.join(cwd, cfg.data_dir, "*.txt"), stopwords)

    if cfg.topic_model_name == "plsa":
        model = PlsaModel(corpus, cfg.number_of_topics, cfg.max_iters)

    model.fit()
    model.show_result()


if __name__ == "__main__":
    main()