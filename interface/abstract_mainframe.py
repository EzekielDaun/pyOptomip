from abc import abstractmethod, ABC


class MainframeBase(ABC):
    @property
    @abstractmethod
    def detector_number(self) -> int:
        pass

    @abstractmethod
    def read(self, index: int) -> float:
        pass

    @abstractmethod
    def enable_laser(self, on: bool):
        pass
