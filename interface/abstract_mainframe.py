from abc import abstractmethod, ABC
from typing import Tuple


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

    @abstractmethod
    def sweep(self, *args, **kwargs) -> Tuple[list[list[float]], list[float]]:
        """_summary_

        Returns:
            Tuple[list[list[float]], list[float]]: 2D array of wavelength with first index of channel and 1D array of power
        """
        pass
