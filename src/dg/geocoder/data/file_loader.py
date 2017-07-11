from abc import abstractmethod


class DataLoader:

    @abstractmethod
    def build_data_frame(self):
        pass
