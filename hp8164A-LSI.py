from typing import Union
from lib.hp816x_driver import (
    Hp816xDriver,
    Hp816xModel,
    Hp816xSweepSpeed,
    Hp816xPowerUnit,
    Hp816xOpticalOutputMode,
    Hp816xNumberOfScans,
)


class Hp8164A_LSI:
    def __init__(
        self,
        hp_addr: str,
        n77_addr: Union[str, None] = None,
        reset=False,
        forceTrans=True,
        autoErrorCheck=True,
    ):
        self.__driver = Hp816xDriver(Hp816xModel.HP8164AB, hp_addr, True, reset)
        self.__driver.forceTransaction(forceTrans)
        self.__driver.errorQueryDetect(autoErrorCheck)
        self.__driver.registerMainframe(self.__driver.handle)
        if n77_addr is not None:
            n77_handle = self.__driver.init(n77_addr, True, reset)
            self.__driver.registerMainframe(n77_handle)

    def getSlotInfo(self):
        return self.__driver.getSlotInformation_Q()

    def sweep(self):
        self.__driver.setSweepSpeed(Hp816xSweepSpeed.hp816x_SPEED_5NM)
        num_dp, num_chan = self.__driver.prepareMfLambdaScan(
            Hp816xPowerUnit.hp816x_PU_DBM,
            0,
            Hp816xOpticalOutputMode.hp816x_HIGHPOW,
            Hp816xNumberOfScans.hp816x_NO_OF_SCANS_1,
            len(self.getSlotInfo()),
            1520e-9,
            1570e-9,
            0.008e-9,
        )
        print(num_dp, num_chan)
        self.__driver.executeMfLambdaScan(num_dp)
        print(self.__driver.getLambdaScanResult(0, True, -100, num_dp)[0])


if __name__ == "__main__":
    hp8164a = Hp8164A_LSI("GPIB0::20::INSTR", "TCPIP0::100.65.11.185::5025::SOCKET")
    hp8164a.sweep()
