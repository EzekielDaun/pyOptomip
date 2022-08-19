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
    Hp816xPWMRangeMode,
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
        reset=True,
        forceTrans=True,
        autoErrorCheck=True,
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

        # other initialization settings
        for s, c in self.__sensor_map:
            self.__driver.set_PWM_powerRange(
                s, c, Hp816xPWMRangeMode.hp816x_PWM_RANGE_AUTO, 0.0
            )
            self.__driver.set_PWM_powerUnit(s, c, Hp816xPowerUnit.hp816x_PU_DBM)
        if self.__with_n77:
            for s, c in self.__n77_sensor_map:
                self.__n77_driver.set_PWM_powerRange(
                    s, c, Hp816xPWMRangeMode.hp816x_PWM_RANGE_AUTO, 0.0
                )
                self.__n77_driver.set_PWM_powerUnit(s, c, Hp816xPowerUnit.hp816x_PU_DBM)

    def __del__(self):
        self.__driver.unregisterMainframe(self.__driver.handle)
        if self.__with_n77:
            self.__n77_driver.unregisterMainframe(self.__n77_driver.handle)

    # properties and methods for the abstract mainframe base class
    @property
    def detector_names(self):
        """
        returns how many detectors in this setup
        """
        ret = [f"HP8164 Slot {i} Channel {c.name[-1]}" for i, c in self.__sensor_map]
        if self.__with_n77:
            ret += [
                f"N7744 Slot {i} Channel {c.name[-1]}" for i, c in self.__n77_sensor_map
            ]
        return ret

    def read(self, index: int) -> float:
        if index >= len(self.detector_names):
            raise RuntimeError(
                f"Index {index} out of range. There are only {len(self.detector_names)} detectors."
            )
        elif index >= len(self.__sensor_map):
            return self.__n77_driver.PWM_readValue(
                *self.__n77_sensor_map[index - len(self.__sensor_map)]
            )
        else:
            return self.__driver.PWM_readValue(*self.__sensor_map[index])

    def enable_laser(self, on: bool):
        self.__driver.set_TLS_laserState(0, bool(on))

    def sweep(
        self,
        power: float,
        start_nm: int,
        end_nm: int,
        step_nm: float,
        speed: Hp816xSweepSpeed,
    ) -> tuple[list[list[float]], list[float]]:
        self.__driver.setSweepSpeed(speed)
        num_dp, num_chan = self.__driver.prepareMfLambdaScan(
            Hp816xPowerUnit.hp816x_PU_DBM,
            float(power),
            Hp816xOpticalOutputMode.hp816x_HIGHPOW,
            Hp816xNumberOfScans.hp816x_NO_OF_SCANS_1,
            len(self.detector_names),
            int(start_nm) * 1e-9,
            int(end_nm) * 1e-9,
            float(step_nm) * 1e-9,
        )
        self.__driver.executeMfLambdaScan(num_dp)
        return [
            self.__driver.getLambdaScanResult(x, True, -100, num_dp)[0]
            for x in range(len(self.detector_names))
        ], self.__driver.getLambdaScanResult(0, True, -100, num_dp)[1]

    # normal member methods


if __name__ == "__main__":
    import numpy as np
    from matplotlib import pyplot as plt

    cband_setup = LSIMainframe(
        "GPIB0::20::INSTR", "TCPIP0::100.65.11.185::5025::SOCKET", reset=True
    )

    cband_setup.enable_laser(True)
    result = cband_setup.sweep(0, 1564, 1580, 0.008, Hp816xSweepSpeed.hp816x_SPEED_5NM)

    power = np.array(result[0])
    wavelength = np.array(result[1])
    print([i for i in power[0][:100]])
    plt.plot(power[0])
    plt.show()
    print(power.shape)
    # print(wavelength.shape)
    cband_setup.enable_laser(False)
