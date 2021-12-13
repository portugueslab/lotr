from lotr.file_utils import get_figures_location, get_nb_name
import configparser
from lotr.default_vals import RESULTS_LOG_FILE
from datetime import datetime
from lotr import dataset_folders


class ResultsLogger:
    def __init__(self, log_filename=None):
        if log_filename is None:
            log_filename = get_figures_location() / RESULTS_LOG_FILE

        self.log_filename = log_filename

        self.create_reslog_file()

    @property
    def dataset(self):
        return set([d.name for d in dataset_folders])

    def get_config_parser(self):
        configparser_obj = configparser.ConfigParser()
        configparser_obj.read(self.log_filename)
        return configparser_obj

    def create_reslog_file(self):
        config = configparser.ConfigParser()
        config['log_info'] = {"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                              "dataset": self.dataset}
        if not self.log_filename.exists():
            with open(self.log_filename, 'w') as configfile:
                config.write(configfile)

    def check_dataset_consistency(self, dataset_to_check):
        return all([d in self.dataset for d in dataset_to_check])

    def add_entry(self, name, value, interval, fids, n_items=None):
        cfgparser = self.get_config_parser()
        if name not in cfgparser.sections():
            cfgparser.add_section(name)

        cfgparser.set(name, "value", str(value))
        cfgparser.set(name, "interval", str(interval))
        cfgparser.set(name, "n_fish", str(len(fids)))
        if n_items is not None:
            cfgparser.set(name, "n_items", n_items)
        cfgparser.set(name, "fids", str(fids))

        with open(self.log_filename, 'w') as configfile:
            cfgparser.write(configfile)


if __name__ == "__main__":
    print(dataset_folders)
    logger = ResultsLogger()
    logger.add_entry("pca", 5, (-1, 1), ["a", "b"])