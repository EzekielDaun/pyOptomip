from typing import Optional

from interface.abstract_mainframe import MainframeBase
from lib.hp816x_driver import (
    Hp816xDriver,
    Hp816xModel,
    Hp816xSweepSpeed,
    Hp816xPowerUnit,
    Hp816xOpticalOutputMode,
    Hp816xNumberOfScans,
    Hp816xSlot,
    Hp816xChan,
)

import logging

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class LSIMainframe(MainframeBase):
    def __init__(
        self,
        mainframe_addr: str,
        n77_addr: Optional[str] = None,
        reset=False,
        forceTrans=True,
        autoErrorCheck=True,
        powerUnit=Hp816xPowerUnit.hp816x_PU_DBM,
    ):
        logger.info(f"Initializing mainframe at {mainframe_addr}, N77 at {n77_addr}")
        temp: str = Hp816xDriver.getInstrumentId_Q(mainframe_addr)
        mainframe_id = temp.split(",")[1]
        mainframe_model = None  # type: ignore
        for m in list(Hp816xModel):
            if mainframe_id[:-1] in m.name:
                mainframe_model = m
                break
        if mainframe_model is None:
            raise RuntimeError(f"Unknown mainframe model: {mainframe_id}")

        # drivers and sensor maps
        self.__driver = Hp816xDriver(mainframe_model, mainframe_addr, True, reset)
        self.__driver.forceTransaction(forceTrans)
        self.__driver.errorQueryDetect(autoErrorCheck)
        self.__driver.registerMainframe(self.__driver.handle)

        self.__sensor_map: list[tuple[int, Hp816xChan]] = []
        for i, slot in enumerate(self.__driver.getSlotInformation_Q()):
            if slot == Hp816xSlot.hp816x_SINGLE_SENSOR:
                self.__sensor_map.append((i, Hp816xChan.hp816x_CHAN_1))
            elif slot == Hp816xSlot.hp816x_DUAL_SENSOR:
                self.__sensor_map.append((i, Hp816xChan.hp816x_CHAN_1))
                self.__sensor_map.append((i, Hp816xChan.hp816x_CHAN_2))

        self.__with_n77 = True if n77_addr is not None else False
        if self.__with_n77:
            logger.info(f"Initializing N77 Detector at {n77_addr}")
            self.__n77_driver = Hp816xDriver(
                Hp816xModel.N7744xA, str(n77_addr), True, reset
            )
            self.__n77_driver.registerMainframe(self.__n77_driver.handle)
            self.__n77_sensor_map = [
                (i + 1, Hp816xChan.hp816x_CHAN_1)
                for i, _ in enumerate(self.__n77_driver.getSlotInformation_Q())
            ]

        # general settings
        self.__power_unit = powerUnit

    # properties and methods for the abstract mainframe base class
    @property
    def detector_number(self):
        """
        returns how many detectors in this setup
        """
        if self.__with_n77:
            return len(self.__sensor_map) + len(self.__n77_sensor_map)
        else:
            return len(self.__sensor_map)

    def read(self, index: int) -> float:
        if index >= self.detector_number:
            raise RuntimeError(
                f"Index {index} out of range. There are only {self.detector_number} detectors."
            )
        elif index >= len(self.__sensor_map):
            return self.__n77_driver.PWM_readValue(
                *self.__n77_sensor_map[index - len(self.__sensor_map)]
            )
        else:
            return self.__driver.PWM_readValue(*self.__sensor_map[index])

    def enable_laser(self, on: bool):
        self.__driver.set_TLS_laserState(0, bool(on))

    # normal member methods
    def sweep(self):
        self.__driver.setSweepSpeed(Hp816xSweepSpeed.hp816x_SPEED_5NM)

        num_dp, num_chan = self.__driver.prepareMfLambdaScan(
            self.__power_unit,
            0,
            Hp816xOpticalOutputMode.hp816x_HIGHPOW,
            Hp816xNumberOfScans.hp816x_NO_OF_SCANS_1,
            self.detector_number,
            1520e-9,
            1570e-9,
            0.008e-9,
        )
        print(num_dp, num_chan)
        self.__driver.executeMfLambdaScan(num_dp)

        return [
            self.__driver.getLambdaScanResult(x, True, -100, num_dp)[0]
            for x in range(self.detector_number)
        ]


if __name__ == "__main__":
    import numpy as np

    cband_setup = LSIMainframe(
        "GPIB0::20::INSTR", "TCPIP0::100.65.11.185::5025::SOCKET", reset=True
    )
    cband_setup.enable_laser(True)
    # for i in range(cband_setup.detector_number):
    #     print(cband_setup.read(i))
    result = np.array(cband_setup.sweep())
    print(result.shape)
    cband_setup.enable_laser(False)
