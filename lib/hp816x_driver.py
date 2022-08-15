import os
import platform
from typing import cast
from ctypes import (
    POINTER,
    byref,
    WinDLL,
    c_char_p,
    c_uint8,
    c_uint16,
    c_uint32,
    c_int,
    c_int8,
    c_int16,
    c_int32,
    c_long,
    c_char,
    c_ubyte,
    c_float,
    c_double,
    c_void_p,
)
from enum import IntEnum, auto


# Buffer sizes
ERROR_MSG_BUFFER_SIZE = 256
DEFAULT_MSG_BUFFER_SIZE = 256


# VI Definitions, copied from visatype.h and hp816x.pdf
VI_SUCCESS = c_long(0)
VI_ERROR = c_long(0x80000000)

VI_NULL = c_int(0)
VI_TRUE = c_int(1)
VI_FALSE = c_int(0)

# Mainframe model info
class Hp816xModel(IntEnum):
    HP8163AB = auto()
    HP8164AB = auto()
    HP8166AB = auto()


# Slot info
class Hp816xSlot(IntEnum):
    hp816x_UNDEF = 0
    hp816x_SINGLE_SENSOR = 1
    hp816x_DUAL_SENSOR = 2
    hp816x_FIXED_SINGLE_SOURCE = 3
    hp816x_FIXED_DUAL_SOURCE = 4
    hp816x_TUNABLE_SOURCE = 5
    hp816x_RETURN_LOSS = 6
    hp816x_RETURN_LOSS_COMBO = 7


class Hp816xTriggerConfiguration(IntEnum):
    hp816x_TRIG_DISABLED = 0
    hp816x_TRIG_DEFAULT = 1
    hp816x_TRIG_PASSTHROUGH = 2
    hp816x_TRIG_LOOPBACK = 3
    hp816x_TRIG_CUSTOM = 4


class Hp816xNode(IntEnum):
    hp816x_NODE_A = 0
    hp816x_NODE_B = 1


class Hp816xSelect(IntEnum):
    hp816x_SELECT_MIN = 0
    hp816x_SELECT_MAX = 1
    hp816x_SELECT_DEF = 2
    hp816x_SELECT_MANUAL = 3


class Hp816xPowerUnit(IntEnum):
    hp816x_PU_DBM = 0
    hp816x_PU_WATT = 1


class Hp816xChan(IntEnum):
    hp816x_CHAN_1 = 0
    hp816x_CHAN_2 = 1


class Hp816xPWMTrigIn(IntEnum):
    hp816x_PWM_TRIGIN_IGN = 0
    hp816x_PWM_TRIGIN_SME = 1
    hp816x_PWM_TRIGIN_CME = 2


class Hp816xPWMTrigOut(IntEnum):
    hp816x_PWM_TRIGOUT_NONE = 0
    hp816x_PWM_TRIGOUT_AVG = 1
    hp816x_PWM_TRIGOUT_MEAS = 2


class Hp816xPWMRangeMode(IntEnum):
    hp816x_PWM_RANGE_AUTO = 1
    hp816x_PWM_RANGE_MANUAL = 0


class Hp816xPWMTrigger(IntEnum):
    hp816x_PWM_CONTINUOUS = 1
    hp816x_PWM_IMMEDIATE = 0


class Hp816xPWMMeasureMode(IntEnum):
    hp816x_PWM_REF_RELATIV = 1
    hp816x_PWM_REF_ABSOLUTE = 0


class Hp816xPWMReferenceSource(IntEnum):
    hp816x_PWM_TO_REF = 0
    hp816x_PWM_TO_MOD = 1


class Hp816xMinMaxMode(IntEnum):
    hp816x_MM_CONT = 0
    hp816x_MM_WIN = 1
    hp816x_MM_REFRESH = 2


class Hp816xSource(IntEnum):
    hp816x_LOWER_SRC = 0
    hp816x_UPPER_SRC = 1
    hp816x_BOTH_SRC = 2


class Hp816xModulationSource(IntEnum):
    hp816x_AM_OFF = 0
    hp816x_AM_INT = 1
    hp816x_AM_CC = 2


class Hp816xModulationFrequency(IntEnum):
    hp816x_AM_MIN = 0
    hp816x_AM_MAX = 1
    hp816x_AM_DEFAULT = 2
    hp816x_AM_MANUAL = 3


class Hp816xSwitchInput(IntEnum):
    hp816x_SWT_INP_A = 0
    hp816x_SWT_INP_B = 1


class Hp816xSwitchOutput(IntEnum):
    hp816x_SWT_OUT_1 = 0
    hp816x_SWT_OUT_2 = 2
    hp816x_SWT_OUT_3 = 2
    hp816x_SWT_OUT_4 = 3
    hp816x_SWT_OUT_5 = 4
    hp816x_SWT_OUT_6 = 5
    hp816x_SWT_OUT_7 = 6
    hp816x_SWT_OUT_8 = 7


class Hp816xRLMInternalTrigger(IntEnum):
    hp816x_RLM_IMMEDIATE = 0
    hp816x_RLM_CONTINUOUS = 1


class Hp816xRLMTriggerIn(IntEnum):
    hp816x_RLM_TRIGIN_IGN = 0
    hp816x_RLM_TRIGIN_SME = 1
    hp816x_RLM_TRIGIN_CME = 2


class Hp816xRLMTriggerOut(IntEnum):
    hp816x_RLM_TRIGOUT_NONE = 0
    hp816x_RLM_TRIGOUT_AVG = 1


class Hp816xCAL(IntEnum):
    hp816x_CAL_REFL = 0
    hp816x_CAL_TERM = 1
    hp816x_CAL_FACTORY = 2


class Hp816xOpticalOutputMode(IntEnum):
    hp816x_HIGHPOW = 0
    hp816x_LOWSSE = 1
    hp816x_BHR = 2
    hp816x_BLR = 3


class Hp816xInputType(IntEnum):
    hp816x_INP_MIN = 0
    hp816x_INP_DEF = 1
    hp816x_INP_MAX = 2
    hp816x_INP_MAN = 3


class Hp816xTLSTriggerIn(IntEnum):
    hp816x_TLS_TRIGIN_IGN = 0
    hp816x_TLS_TRIGIN_NEXTSTEP = 1
    hp816x_TLS_TRIGIN_SWEEPSTART = 2


class Hp816xTLSTriggerOut(IntEnum):
    hp816x_TLS_TRIGOUT_DISABLED = 0
    hp816x_TLS_TRIGOUT_MOD = 1
    hp816x_TLS_TRIGOUT_STEPEND = 2
    hp816x_TLS_TRIGOUT_SWSTART = 3
    hp816x_TLS_TRIGOUT_SWEND = 4


class Hp816xPowerMode(IntEnum):
    hp816x_POWER_MANUAL = 0
    hp816x_POWER_AUTO = 1


class Hp816xSweepMode(IntEnum):
    hp816x_SWEEP_STEP = 0
    hp816x_SWEEP_MAN = 1
    hp816x_SWEEP_CONT = 2


class Hp816xRepeatMode(IntEnum):
    hp816x_ONEWAY = 0
    hp816x_TWOWAY = 1


class Hp816xSweepCommand(IntEnum):
    hp816x_SW_CMD_STOP = 0
    hp816x_SW_CMD_START = 1
    hp816x_SW_CMD_PAUSE = 2
    hp816x_SW_CMD_CONT = 3


class Hp816xModulationType(IntEnum):
    hp816x_MOD_INT = 0
    hp816x_MOD_CC = 1
    hp816x_MOD_AEXT = 2
    hp816x_MOD_DEXT = 3
    hp816x_MOD_VWLOCK = 4
    hp816x_MOD_BACKPL = 5


class Hp816xModulationOutput(IntEnum):
    hp816x_MOD_ALWAYS = 0
    hp816x_MOD_LREADY = 1


class Hp816xBNCOutput(IntEnum):
    hp816x_BNC_MOD = 0
    hp816x_BNC_VPP = 1


class Hp816xNumberOfScans(IntEnum):
    hp816x_NO_OF_SCANS_1 = 0
    hp816x_NO_OF_SCANS_2 = 1
    hp816x_NO_OF_SCANS_3 = 2


class Hp816xSweepSpeed(IntEnum):
    hp816x_SPEED_80NM = -1
    hp816x_SPEED_40NM = 0
    hp816x_SPEED_20NM = 1
    hp816x_SPEED_10NM = 2
    hp816x_SPEED_5NM = 3
    hp816x_SPEED_05NM = 4
    hp816x_SPEED_AUTO = 5


class ViUInt32(c_uint32):
    pass


ViPUInt32 = POINTER(ViUInt32)
ViAUInt32 = POINTER(ViUInt32)


class ViInt32(c_int32):
    pass


ViPInt32 = POINTER(ViInt32)
ViAInt32 = POINTER(ViInt32)


class ViUInt16(c_uint16):
    pass


ViPUInt16 = POINTER(ViUInt16)
ViAUInt16 = POINTER(ViUInt16)


class ViInt16(c_int16):
    pass


ViPInt16 = POINTER(ViInt16)
ViAInt16 = POINTER(ViInt16)


class ViUInt8(c_uint8):
    pass


ViPUInt8 = POINTER(ViUInt8)
ViAUInt8 = POINTER(ViUInt8)


class ViInt8(c_int8):
    pass


ViPInt8 = POINTER(ViInt8)
ViAInt8 = POINTER(ViInt8)


class ViChar(c_char):
    pass


ViPChar = POINTER(ViChar)
ViAChar = POINTER(ViChar)


class ViByte(c_ubyte):
    pass


ViPByte = POINTER(ViByte)
ViAByte = POINTER(ViByte)


class ViAddr(c_void_p):
    pass


ViPAddr = POINTER(ViAddr)
ViAAddr = POINTER(ViAddr)


class ViReal32(c_float):
    pass


ViPReal32 = POINTER(ViReal32)
ViAReal32 = POINTER(ViReal32)


class ViReal64(c_double):
    pass


ViPReal64 = POINTER(ViReal64)
ViAReal64 = POINTER(ViReal64)


class ViBuf(c_ubyte):
    pass


ViPBuf = POINTER(ViBuf)
ViABuf = POINTER(POINTER(ViBuf))


class ViString(c_char_p):
    pass


class ViPString(c_char_p):
    pass


ViAString = POINTER(ViString)


class ViRsrc(ViString):
    pass


class ViPRsrc(ViPString):
    pass


ViARsrc = POINTER(ViRsrc)


class ViBoolean(c_uint16):
    pass


ViPBoolean = POINTER(ViBoolean)
ViABoolean = POINTER(ViBoolean)


class ViStatus(c_uint32):
    pass


ViPStatus = POINTER(ViStatus)
ViAStatus = POINTER(ViStatus)


class ViVersion(c_uint32):
    pass


ViPVersion = POINTER(ViVersion)
ViAVersion = POINTER(ViVersion)


class ViObject(c_uint32):
    pass


ViPObject = POINTER(ViObject)
ViAObject = POINTER(ViObject)


class ViSession(c_uint32):
    pass


ViPSession = POINTER(ViSession)
ViASession = POINTER(ViSession)


class InstrumentError(RuntimeError):
    def __init__(self, message: str):
        super().__init__(f"InstrumentError: {message}")


class Hp816xDriver(object):

    # Load hp816x_32.dll/hp816x_64.dll
    if not platform.system() == "Windows":
        raise NotImplementedError("This module support Windows only")

    __dll = WinDLL(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                f"hp816x_{int(platform.architecture()[0][0:2])}.dll",
            )
        )
    )

    # Function prototype declarations
    # Output string are ViAChar, input strings are ViString
    __dll.hp816x_init.argtypes = [
        ViRsrc,
        ViBoolean,
        ViBoolean,
        ViPSession,
    ]
    __dll.hp816x_init.restype = ViStatus

    __dll.hp816x_close.argtypes = [ViSession]
    __dll.hp816x_close.restype = ViStatus

    __dll.hp816x_error_message.argtypes = [ViSession, ViStatus, ViString]
    __dll.hp816x_error_message.restype = ViStatus

    # The above are the most basic functions
    # Functions below start at page 41 of hp816x.pdf

    __dll.hp816x_getHandle.argtypes = [ViSession, ViPSession]
    __dll.hp816x_getHandle.restype = ViStatus

    __dll.hp816x_revision_Q.argtypes = [ViSession, ViAChar, ViAChar]
    __dll.hp816x_revision_Q.restype = ViStatus

    __dll.hp816x_self_test.argtypes = [ViSession, ViPInt16, ViAChar]
    __dll.hp816x_self_test.restype = ViStatus

    __dll.hp816x_timeOut.argtypes = [ViSession, ViInt32]
    __dll.hp816x_timeOut.restype = ViStatus

    __dll.hp816x_timeOut_Q.argtypes = [ViSession, ViPInt32]
    __dll.hp816x_timeOut_Q.restype = ViStatus

    __dll.hp816x_getInstrumentId_Q.argtypes = [ViString, ViAChar]
    __dll.hp816x_getInstrumentId_Q.restype = ViStatus

    __dll.hp816x_listVisa_Q.argtypes = [ViInt32, ViBoolean, ViPInt32, ViAChar]
    __dll.hp816x_listVisa_Q.restype = ViStatus

    __dll.hp816x_setBaudrate.argtypes = [ViRsrc, ViUInt32]
    __dll.hp816x_setBaudrate.restype = ViStatus

    __dll.hp816x_dcl.argtypes = [ViSession]
    __dll.hp816x_dcl.restype = ViStatus

    __dll.hp816x_error_query.argtypes = [ViSession, ViPInt32, ViPChar]
    __dll.hp816x_error_query.restype = ViStatus

    __dll.hp816x_errorQueryDetect.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_errorQueryDetect.restype = ViStatus

    __dll.hp816x_dbmToWatt.argtypes = [ViSession, ViReal64, ViPReal64]
    __dll.hp816x_dbmToWatt.restype = ViStatus

    __dll.hp816x_WattToDBm.argtypes = [ViSession, ViReal64, ViPReal64]
    __dll.hp816x_WattToDBm.restype = ViStatus

    __dll.hp816x_setDate.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_setDate.restype = ViStatus

    __dll.hp816x_getDate.argtypes = [ViSession, ViPInt32, ViPInt32, ViPInt32]
    __dll.hp816x_getDate.restype = ViStatus

    __dll.hp816x_setTime.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_setTime.restype = ViStatus

    __dll.hp816x_getTime.argtypes = [ViSession, ViPInt32, ViPInt32, ViPInt32]
    __dll.hp816x_getTime.restype = ViStatus

    __dll.hp816x_cls.argtypes = [ViSession]
    __dll.hp816x_cls.restype = ViStatus

    __dll.hp816x_forceTransaction.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_forceTransaction.restype = ViStatus

    __dll.hp816x_driverLogg.argtypes = [ViSession, ViString, ViBoolean, ViBoolean]
    __dll.hp816x_driverLogg.restype = ViStatus

    __dll.hp816x_cmd.argtypes = [ViSession, ViAChar]
    __dll.hp816x_cmd.restype = ViStatus

    __dll.hp816x_cmdString_Q.argtypes = [ViSession, ViString, ViInt16, ViAChar]
    __dll.hp816x_cmdString_Q.restype = ViStatus

    __dll.hp816x_cmdInt.argtypes = [ViSession, ViString, ViInt32]
    __dll.hp816x_cmdInt.restype = ViStatus

    __dll.hp816x_cmdInt32_Q.argtypes = [ViSession, ViString, ViPInt32]
    __dll.hp816x_cmdInt32_Q.restype = ViStatus

    __dll.hp816x_cmdReal.argtypes = [ViSession, ViString, ViReal64]
    __dll.hp816x_cmdReal.restype = ViStatus

    __dll.hp816x_cmdReal64_Q.argtypes = [ViSession, ViString, ViPReal64]
    __dll.hp816x_cmdReal64_Q.restype = ViStatus

    __dll.hp816x_reset.argtypes = [ViSession]
    __dll.hp816x_reset.restype = ViStatus

    __dll.hp816x_preset.argtypes = [ViSession]
    __dll.hp816x_preset.restype = ViStatus

    __dll.hp816x_mainframeSelftest.argtypes = [ViSession, ViPInt16, ViAChar]
    __dll.hp816x_mainframeSelftest.restype = ViStatus

    __dll.hp816x_moduleSelftest.argtypes = [ViSession, ViInt32, ViPInt16, ViAChar]
    __dll.hp816x_moduleSelftest.restype = ViStatus

    __dll.hp816x_revision_query.argtypes = [ViSession, ViAChar, ViAChar]
    __dll.hp816x_revision_query.restype = ViStatus

    __dll.hp816x_opc_Q.argtypes = [ViSession, ViPBoolean]
    __dll.hp816x_opc_Q.restype = ViStatus

    __dll.hp816x_lockUnlockInstrument.argtypes = [ViSession, ViBoolean, ViString]
    __dll.hp816x_lockUnlockInstrument.restype = ViStatus

    __dll.hp816x_getLockState.argtypes = [ViSession]
    __dll.hp816x_getLockState.restype = ViStatus

    __dll.hp816x_enableDisableDisplay.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_enableDisableDisplay.restype = ViStatus

    __dll.hp816x_getSlotInformation_Q.argtypes = [ViSession, ViInt32, ViAInt32]
    __dll.hp816x_getSlotInformation_Q.restype = ViStatus

    __dll.hp816x_getModuleStatus_Q.argtypes = [
        ViSession,
        ViPBoolean,
        ViAInt32,
        ViPInt32,
    ]
    __dll.hp816x_getModuleStatus_Q.restype = ViStatus

    __dll.hp816x_convertQuestionableStatus_Q.argtypes = [ViSession, ViInt32, ViAChar]
    __dll.hp816x_convertQuestionableStatus_Q.restype = ViStatus

    __dll.hp816x_standardTriggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViUInt32,
        ViUInt32,
        ViUInt32,
    ]
    __dll.hp816x_standardTriggerConfiguration.restype = ViStatus

    __dll.hp816x_standardTriggerConfiguration_Q.argtypes = [
        ViSession,
        ViPInt32,
        ViPUInt32,
        ViPUInt32,
        ViPUInt32,
    ]
    __dll.hp816x_standardTriggerConfiguration_Q.restype = ViStatus

    __dll.hp816x_generateTrigger.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_generateTrigger.restype = ViStatus

    __dll.hp816x_nodeInputConfiguration.argtypes = [
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViUInt32,
        ViUInt32,
    ]
    __dll.hp816x_standardTriggerConfiguration.restype = ViStatus

    __dll.hp816x_trigOutConfiguration.argtypes = [
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViPUInt32,
    ]
    __dll.hp816x_trigOutConfiguration.restype = ViStatus

    __dll.hp816x_set_ATT_attenuation.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
        ViBoolean,
    ]
    __dll.hp816x_set_ATT_attenuation.restype = ViStatus

    __dll.hp816x_get_ATT_attenuation.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_attenuation_Q.restype = ViStatus

    __dll.hp816x_set_ATT_attenuationOffset.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViInt32,
    ]
    __dll.hp816x_set_ATT_attenuationOffset.restype = ViStatus

    __dll.hp816x_get_ATT_attenuationOffset_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_attenuationOffset_Q.restype = ViStatus

    __dll.hp816x_set_ATT_attenuatorSpeed.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_ATT_attenuatorSpeed.restype = ViStatus

    __dll.hp816x_get_ATT_attenuatorSpeed_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_attenuatorSpeed_Q.restype = ViStatus

    __dll.hp816x_ATT_displayToOffset.argtypes = [ViSession, ViInt32]
    __dll.hp816x_ATT_displayToOffset.restype = ViStatus

    __dll.hp816x_set_ATT_wavelength.argtypes = [ViSession, ViInt32, ViInt32, ViReal64]
    __dll.hp816x_set_ATT_wavelength.restype = ViStatus

    __dll.hp816x_get_ATT_wavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_wavelength_Q.restype = ViStatus

    __dll.hp816x_set_ATT_powerUnit.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_ATT_powerUnit.restype = ViStatus

    __dll.hp816x_get_ATT_powerUnit_Q.argtypes = [ViSession, ViPBoolean, ViInt32]
    __dll.hp816x_get_ATT_powerUnit_Q.restype = ViStatus

    __dll.hp816x_set_ATT_absPowerMode.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_ATT_absPowerMode.restype = ViStatus

    __dll.hp816x_get_ATT_absPowerMode_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_ATT_absPowerMode_Q.restype = ViStatus

    __dll.hp816x_set_ATT_power.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_ATT_power.restype = ViStatus

    __dll.hp816x_get_ATT_power_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
        ViPBoolean,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_power_Q.restype = ViStatus

    __dll.hp816x_cp_ATT_refFromExtPM.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_cp_ATT_refFromExtPM.restype = ViStatus

    __dll.hp816x_set_ATT_powerReference.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_ATT_powerReference.restype = ViStatus

    __dll.hp816x_get_ATT_powerReference_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_powerReference_Q.restype = ViStatus

    __dll.hp816x_set_ATT_shutterState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_ATT_shutterState.restype = ViStatus

    __dll.hp816x_get_ATT_shutterState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_ATT_shutterState_Q.restype = ViStatus

    __dll.hp816x_set_ATT_shutterAtPowerOn.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_ATT_shutterAtPowerOn.restype = ViStatus

    __dll.hp816x_get_ATT_shutterAtPowerOn_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_ATT_shutterAtPowerOn_Q.restype = ViStatus

    __dll.hp816x_get_ATT_operStatus.argtypes = [ViSession, ViInt32, ViPUInt32, ViAChar]
    __dll.hp816x_get_ATT_operStatus.restype = ViStatus

    __dll.hp816x_set_ATT_wlOffsRefPowermeter.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
    ]
    __dll.hp816x_set_ATT_wlOffsRefPowermeter.restype = ViStatus

    __dll.hp816x_get_ATT_wlOffsRefPowermeter_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPInt32,
    ]
    __dll.hp816x_get_ATT_wlOffsRefPowermeter_Q.restype = ViStatus

    __dll.hp816x_set_ATT_wavelengthOffsetState.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
    ]
    __dll.hp816x_set_ATT_wavelengthOffsetState.restype = ViStatus

    __dll.hp816x_get_ATT_wavelengthOffsetState_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
    ]
    __dll.hp816x_get_ATT_wavelengthOffsetState_Q.restype = ViStatus

    __dll.hp816x_set_ATT_wavelengthOffset.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_set_ATT_wavelengthOffset.restype = ViStatus

    __dll.hp816x_get_ATT_wavelengthOffsetIndex_Q.argtypes = [
        ViSession,
        ViInt32,
        ViUInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_wavelengthOffsetIndex_Q.restype = ViStatus

    __dll.hp816x_get_ATT_offsetFromWavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_offsetFromWavelength_Q.restype = ViStatus

    __dll.hp816x_delete_ATT_offsetTblEntries.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_delete_ATT_offsetTblEntries.restype = ViStatus

    __dll.hp816x_get_ATT_offsetTable_Q.argtypes = [
        ViSession,
        ViInt32,
        ViAReal64,
        ViAReal64,
    ]
    __dll.hp816x_get_ATT_offsetTable_Q.restype = ViStatus

    __dll.hp816x_get_ATT_offsetTblSize_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPUInt32,
        ViPUInt32,
    ]
    __dll.hp816x_get_ATT_offsetTblSize_Q.restype = ViStatus

    __dll.hp816x_read_ATT_outputPower.argtypes = [ViSession, ViInt32, ViAReal64]
    __dll.hp816x_read_ATT_outputPower.restype = ViStatus

    __dll.hp816x_fetch_ATT_outputPower.argtypes = [ViSession, ViInt32, ViAReal64]
    __dll.hp816x_fetch_ATT_outputPower.restype = ViStatus

    __dll.hp816x_set_ATT_powerOffset.argtypes = [ViSession, ViInt32, ViInt32, ViReal64]
    __dll.hp816x_set_ATT_powerOffset.restype = ViStatus

    __dll.hp816x_get_ATT_powerOffset_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_ATT_powerOffset_Q.restype = ViStatus

    __dll.hp816x_set_ATT_pwrOffsRefPM.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_set_ATT_pwrOffsRefPM.restype = ViStatus

    __dll.hp816x_set_ATT_offsByRefPM.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_set_ATT_offsByRefPM.restype = ViStatus

    __dll.hp816x_set_ATT_controlLoopState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_ATT_controlLoopState.restype = ViStatus

    __dll.hp816x_get_ATT_controlLoopState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_ATT_controlLoopState_Q.restype = ViStatus

    __dll.hp816x_set_ATT_avTime.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_ATT_avTime.restype = ViStatus

    __dll.hp816x_get_ATT_avTime_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_ATT_avTime_Q.restype = ViStatus

    __dll.hp816x_set_ATT_TriggerConfig.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_set_ATT_TriggerConfig.restype = ViStatus

    __dll.hp816x_get_ATT_TriggerConfig_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_ATT_TriggerConfig_Q.restype = ViStatus

    __dll.hp816x_zero_ATT_powermeter.argtypes = [ViSession, ViInt32]
    __dll.hp816x_zero_ATT_powermeter.restype = ViStatus

    __dll.hp816x_get_ATT_zeroResult_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_ATT_zeroResult_Q.restype = ViStatus

    __dll.hp816x_zero_ATT_all.argtypes = [ViSession]
    __dll.hp816x_zero_ATT_all.restype = ViStatus

    __dll.hp816x_spectralCalibration.argtypes = [
        ViSession,
        ViInt32,
        ViUInt32,
        ViAReal64,
        ViAReal64,
        ViPReal64,
        ViAChar,
    ]
    __dll.hp816x_spectralCalibration.restype = ViStatus

    __dll.hp816x_getWlRespTblSize.argtypes = [ViSession, ViInt32, ViPUInt32, ViPUInt32]
    __dll.hp816x_getWlRespTblSize.restype = ViStatus

    __dll.hp816x_readWlRespTable.argtypes = [ViSession, ViInt32, ViAReal64, ViAReal64]
    __dll.hp816x_readWlRespTable.restype = ViStatus

    __dll.hp816x_readWlRepTblCSV.argtypes = [ViSession, ViInt32, ViAChar]
    __dll.hp816x_readWlRepTblCSV.restype = ViStatus

    __dll.hp816x_PWM_slaveChannelCheck.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_PWM_slaveChannelCheck.restype = ViStatus

    __dll.hp816x_set_PWM_parameters.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViBoolean,
        ViReal64,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_PWM_parameters.restype = ViStatus

    __dll.hp816x_get_PWM_parameters_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPBoolean,
        ViPBoolean,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_parameters_Q.restype = ViStatus

    __dll.hp816x_set_PWM_averagingTime.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_PWM_averagingTime.restype = ViStatus

    __dll.hp816x_get_PWM_averagingTime_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_averagingTime_Q.restype = ViStatus

    __dll.hp816x_set_PWM_wavelength.argtypes = [ViSession, ViInt32, ViInt32, ViReal64]
    __dll.hp816x_set_PWM_wavelength.restype = ViStatus

    __dll.hp816x_get_PWM_wavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_wavelength_Q.restype = ViStatus

    __dll.hp816x_set_PWM_calibration.argtypes = [ViSession, ViInt32, ViInt32, ViReal64]
    __dll.hp816x_set_PWM_calibration.restype = ViStatus

    __dll.hp816x_get_PWM_calibration_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_calibration_Q.restype = ViStatus

    __dll.hp816x_set_PWM_powerRange.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_set_PWM_powerRange.restype = ViStatus

    __dll.hp816x_get_PWM_powerRange_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPBoolean,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_powerRange_Q.restype = ViStatus

    __dll.hp816x_set_PWM_powerUnit.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_set_PWM_powerUnit.restype = ViStatus

    __dll.hp816x_get_PWM_powerUnit_Q.argtypes = [ViSession, ViInt32, ViInt32, ViPInt32]
    __dll.hp816x_get_PWM_powerUnit_Q.restype = ViStatus

    __dll.hp816x_set_PWM_referenceSource.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViInt32,
        ViInt32,
        ViInt32,
    ]
    __dll.hp816x_set_PWM_referenceSource.restype = ViStatus

    __dll.hp816x_get_PWM_referenceSource_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPInt32,
        ViPInt32,
        ViPInt32,
        ViPInt32,
    ]
    __dll.hp816x_get_PWM_referenceSource_Q.restype = ViStatus

    __dll.hp816x_set_PWM_referenceValue.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_PWM_referenceValue.restype = ViStatus

    __dll.hp816x_get_PWM_referenceValue_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_referenceValue_Q.restype = ViStatus

    __dll.hp816x_set_PWM_triggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
    ]
    __dll.hp816x_set_PWM_triggerConfiguration.restype = ViStatus

    __dll.hp816x_get_PWM_triggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPInt32,
    ]
    __dll.hp816x_get_PWM_triggerConfiguration.restype = ViStatus

    __dll.hp816x_PWM_displayToReference.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_PWM_displayToReference.restype = ViStatus

    __dll.hp816x_set_PWM_internalTrigger.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
    ]
    __dll.hp816x_set_PWM_internalTrigger.restype = ViStatus

    __dll.hp816x_start_PWM_internalTrigger.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_start_PWM_internalTrigger.restype = ViStatus

    __dll.hp816x_PWM_readValue.argtypes = [ViSession, ViInt32, ViUInt32, ViPReal64]
    __dll.hp816x_PWM_readValue.restype = ViStatus

    __dll.hp816x_PWM_fetchValue.argtypes = [ViSession, ViInt32, ViUInt32, ViPReal64]
    __dll.hp816x_PWM_fetchValue.restype = ViStatus

    __dll.hp816x_readAll.argtypes = [
        ViSession,
        ViPUInt32,
        ViAInt32,
        ViAInt32,
        ViAReal64,
    ]
    __dll.hp816x_readAll.restype = ViStatus

    __dll.hp816x_PWM_zeroing.argtypes = [ViSession, ViPInt32, ViInt32, ViInt32]
    __dll.hp816x_PWM_zeroing.restype = ViStatus

    __dll.hp816x_PWM_zeroingAll.argtypes = [ViSession, ViPInt32]
    __dll.hp816x_PWM_zeroingAll.restype = ViStatus

    __dll.hp816x_PWM_ignoreError.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViInt32,
    ]
    __dll.hp816x_PWM_ignoreError.restype = ViStatus

    __dll.hp816x_set_PWM_logging.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
        ViInt32,
        ViPInt32,
    ]
    __dll.hp816x_set_PWM_logging.restype = ViStatus

    __dll.hp816x_get_PWM_loggingResults_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViPBoolean,
        ViAReal64,
    ]
    __dll.hp816x_get_PWM_loggingResults_Q.restype = ViStatus

    __dll.hp816x_set_PWM_stability.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViPUInt32,
    ]
    __dll.hp816x_set_PWM_stability.restype = ViStatus

    __dll.hp816x_get_PWM_stability_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViPBoolean,
        ViAReal64,
    ]
    __dll.hp816x_get_PWM_stability_Q.restype = ViStatus

    __dll.hp816x_set_PWM_minMax.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViInt32,
        ViUInt32,
    ]
    __dll.hp816x_set_PWM_minMax.restype = ViStatus

    __dll.hp816x_get_PWM_minMaxResults_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_PWM_minMaxResults_Q.restype = ViStatus

    __dll.hp816x_PWM_functionStop.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_PWM_functionStop.restype = ViStatus

    __dll.hp816x_spectralCalibrationEx.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViUInt32,
        ViAReal64,
        ViAReal64,
        ViPReal64,
        ViAChar,
    ]
    __dll.hp816x_spectralCalibrationEx.restype = ViStatus

    __dll.hp816x_getWlRespTblSizeEx.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPUInt32,
        ViPUInt32,
    ]
    __dll.hp816x_getWlRespTblSizeEx.restype = ViStatus

    __dll.hp816x_readWlRespTableEx.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViAReal64,
        ViAReal64,
    ]
    __dll.hp816x_readWlRespTableEx.restype = ViStatus

    __dll.hp816x_readWlRepTblCSV_Ex.argtypes = [ViSession, ViInt32, ViInt32, ViAChar]
    __dll.hp816x_readWlRepTblCSV_Ex.restype = ViStatus

    __dll.hp816x_set_FLS_parameters.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViInt32,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_FLS_parameters.restype = ViStatus

    __dll.hp816x_get_FLS_parameters_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPBoolean,
        ViPInt32,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_FLS_parameters_Q.restype = ViStatus

    __dll.hp816x_set_FLS_modulation.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_FLS_modulation.restype = ViStatus

    __dll.hp816x_get_FLS_modulation_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViPBoolean,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_FLS_modulation_Q.restype = ViStatus

    __dll.hp816x_set_FLS_laserSource.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_set_FLS_laserSource.restype = ViStatus

    __dll.hp816x_get_FLS_laserSource_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_FLS_laserSource_Q.restype = ViStatus

    __dll.hp816x_get_FLS_wavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_FLS_wavelength_Q.restype = ViStatus

    __dll.hp816x_set_FLS_attenuation.argtypes = [ViSession, ViInt32, ViReal64, ViReal64]
    __dll.hp816x_set_FLS_attenuation.restype = ViStatus

    __dll.hp816x_get_FLS_attenuation_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_FLS_attenuation_Q.restype = ViStatus

    __dll.hp816x_set_FLS_triggerState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_FLS_triggerState.restype = ViStatus

    __dll.hp816x_get_FLS_laserState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_FLS_laserState_Q.restype = ViStatus

    __dll.hp816x_get_FLS_power.argtypes = [ViSession, ViInt32, ViInt32, ViPReal64]
    __dll.hp816x_get_FLS_power.restype = ViStatus

    __dll.hp816x_set_FLS_laserState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_FLS_laserState.restype = ViStatus

    __dll.hp816x_get_FLS_laserState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_FLS_laserState_Q.restype = ViStatus

    __dll.hp816x_get_SWT_type.argtypes = [ViSession, ViInt32, ViPInt32, ViAChar]
    __dll.hp816x_get_SWT_type.restype = ViStatus

    __dll.hp816x_set_SWT_route.argtypes = [ViSession, ViInt32, ViInt32, ViInt32]
    __dll.hp816x_set_SWT_route.restype = ViStatus

    __dll.hp816x_get_SWT_route.argtypes = [ViSession, ViInt32, ViInt32, ViPInt32]
    __dll.hp816x_get_SWT_route.restype = ViStatus

    __dll.hp816x_get_SWT_routeTable.argtypes = [ViSession, ViInt32, ViAChar]
    __dll.hp816x_get_SWT_routeTable.restype = ViStatus

    __dll.hp816x_set_RLM_parameters.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
        ViReal64,
        ViBoolean,
        ViBoolean,
    ]
    __dll.hp816x_set_RLM_parameters.restype = ViStatus

    __dll.hp816x_get_RLM_parameters_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPBoolean,
        ViPBoolean,
    ]
    __dll.hp816x_get_RLM_parameters_Q.restype = ViStatus

    __dll.hp816x_set_RLM_internalTrigger.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_RLM_internalTrigger.restype = ViStatus

    __dll.hp816x_set_RLM_averagingTime.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_RLM_averagingTime.restype = ViStatus

    __dll.hp816x_get_RLM_averagingTime_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_RLM_averagingTime_Q.restype = ViStatus

    __dll.hp816x_set_RLM_wavelength.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_RLM_wavelength.restype = ViStatus

    __dll.hp816x_get_RLM_wavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_wavelength_Q.restype = ViStatus

    __dll.hp816x_set_RLM_powerRange.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_RLM_powerRange.restype = ViStatus

    __dll.hp816x_get_RLM_powerRange_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_powerRange_Q.restype = ViStatus

    __dll.hp816x_set_RLM_triggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
    ]
    __dll.hp816x_set_RLM_triggerConfiguration.restype = ViStatus

    __dll.hp816x_start_RLM_internalTrigger.argtypes = [ViSession, ViInt32]
    __dll.hp816x_start_RLM_internalTrigger.restype = ViStatus

    __dll.hp816x_RLM_readReturnLoss.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_RLM_readReturnLoss.restype = ViStatus

    __dll.hp816x_RLM_fetchReturnLoss.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_RLM_fetchReturnLoss.restype = ViStatus

    __dll.hp816x_RLM_readValue.argtypes = [ViSession, ViInt32, ViBoolean, ViPReal64]
    __dll.hp816x_RLM_readValue.restype = ViStatus

    __dll.hp816x_RLM_fetchValue.argtypes = [ViSession, ViInt32, ViBoolean, ViPReal64]
    __dll.hp816x_RLM_fetchValue.restype = ViStatus

    __dll.hp816x_set_RLM_flReference.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_RLM_flReference.restype = ViStatus

    __dll.hp816x_get_RLM_flReference_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_RLM_flReference_Q.restype = ViStatus

    __dll.hp816x_set_RLM_FPDelta.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_RLM_FPDelta.restype = ViStatus

    __dll.hp816x_get_RLM_FPDelta_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_RLM_FPDelta_Q.restype = ViStatus

    __dll.hp816x_calibrate_RLM.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_calibrate_RLM.restype = ViStatus

    __dll.hp816x_RLM_zeroing.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_RLM_zeroing.restype = ViStatus

    __dll.hp816x_RLM_zeroingAll.argtypes = [ViSession, ViPInt32]
    __dll.hp816x_RLM_zeroingAll.restype = ViStatus

    __dll.hp816x_enable_RLM_sweep.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_enable_RLM_sweep.restype = ViStatus

    __dll.hp816x_get_RLM_reflectanceValues_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_reflectanceValues_Q.restype = ViStatus

    __dll.hp816x_get_RLM_terminationValues_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_terminationValues_Q.restype = ViStatus

    __dll.hp816x_get_RLM_dutValues_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_dutValues_Q.restype = ViStatus

    __dll.hp816x_calculate_RL.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_calculate_RL.restype = ViStatus

    __dll.hp816x_get_RLM_srcWavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_srcWavelength_Q.restype = ViStatus

    __dll.hp816x_set_RLM_laserSourceParameters.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
    ]
    __dll.hp816x_set_RLM_laserSourceParameters.restype = ViStatus

    __dll.hp816x_get_RLM_laserSourceParameters_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPBoolean,
    ]
    __dll.hp816x_get_RLM_laserSourceParameters_Q.restype = ViStatus

    __dll.hp816x_set_RLM_modulationState.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViBoolean,
    ]
    __dll.hp816x_set_RLM_modulationState.restype = ViStatus

    __dll.hp816x_get_RLM_modulationState_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPBoolean,
    ]
    __dll.hp816x_get_RLM_modulationState_Q.restype = ViStatus

    __dll.hp816x_set_RLM_laserState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_RLM_laserState.restype = ViStatus

    __dll.hp816x_get_RLM_laserState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_RLM_laserState_Q.restype = ViStatus

    __dll.hp816x_set_RLM_logging.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViInt32,
        ViPInt32,
    ]
    __dll.hp816x_set_RLM_logging.restype = ViStatus

    __dll.hp816x_get_RLM_loggingResults_Q.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViPBoolean,
        ViAReal64,
    ]
    __dll.hp816x_get_RLM_loggingResults_Q.restype = ViStatus

    __dll.hp816x_set_RLM_stability.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViPInt32,
    ]
    __dll.hp816x_set_RLM_stability.restype = ViStatus

    __dll.hp816x_get_RLM_stabilityResults_Q.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViPBoolean,
        ViAReal64,
    ]
    __dll.hp816x_get_RLM_stabilityResults_Q.restype = ViStatus

    __dll.hp816x_set_RLM_minMax.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViUInt32,
    ]
    __dll.hp816x_set_RLM_minMax.restype = ViStatus

    __dll.hp816x_get_RLM_minMaxResults_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_RLM_minMaxResults_Q.restype = ViStatus

    __dll.hp816x_RLM_functionStop.argtypes = [ViSession, ViInt32]
    __dll.hp816x_RLM_functionStop.restype = ViStatus

    __dll.hp816x_WaitForOPC.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_WaitForOPC.restype = ViStatus

    __dll.hp816x_set_TLS_parameters.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViReal64,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_parameters.restype = ViStatus

    __dll.hp816x_get_TLS_parameters_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPBoolean,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_parameters_Q.restype = ViStatus

    __dll.hp816x_set_TLS_wavelength.argtypes = [ViSession, ViInt32, ViInt32, ViReal64]
    __dll.hp816x_set_TLS_wavelength.restype = ViStatus

    __dll.hp816x_get_TLS_wavelength_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_wavelength_Q.restype = ViStatus

    __dll.hp816x_set_TLS_power.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_power.restype = ViStatus

    __dll.hp816x_get_TLS_power_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_power_Q.restype = ViStatus

    __dll.hp816x_set_TLS_opticalOutput.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_set_TLS_opticalOutput.restype = ViStatus

    __dll.hp816x_get_TLS_opticalOutput_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_opticalOutput_Q.restype = ViStatus

    __dll.hp816x_get_TLS_powerMaxInRange_Q.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_powerMaxInRange_Q.restype = ViStatus

    __dll.hp816x_set_TLS_laserState.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_TLS_laserState.restype = ViStatus

    __dll.hp816x_get_TLS_laserState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_TLS_laserState_Q.restype = ViStatus

    __dll.hp816x_set_TLSlaserRiseTime.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_TLSlaserRiseTime.restype = ViStatus

    __dll.hp816x_get_TLS_laserRiseTime.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_TLS_laserRiseTime.restype = ViStatus

    __dll.hp816x_set_TLS_triggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
    ]
    __dll.hp816x_set_TLS_triggerConfiguration.restype = ViStatus

    __dll.hp816x_get_TLS_triggerConfiguration.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPInt32,
    ]
    __dll.hp816x_get_TLS_triggerConfiguration.restype = ViStatus

    __dll.hp816x_set_TLS_attenuation.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_attenuation.restype = ViStatus

    __dll.hp816x_get_TLS_attenuationSettings_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
        ViPBoolean,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_attenuationSettings_Q.restype = ViStatus

    __dll.hp816x_set_TLS_dark.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_TLS_dark.restype = ViStatus

    __dll.hp816x_get_TLS_darkState_Q.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_TLS_darkState_Q.restype = ViStatus

    __dll.hp816x_get_TLS_temperatures.argtypes = [
        ViSession,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_temperatures.restype = ViStatus

    __dll.hp816x_get_TLS_temperaturesEx.argtypes = [
        ViSession,
        ViInt32,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_temperaturesEx.restype = ViStatus

    __dll.hp816x_TLS_zeroing.argtypes = [ViSession]
    __dll.hp816x_TLS_zeroing.restype = ViStatus

    __dll.hp816x_TLS_zeroingAll.argtypes = [ViSession]
    __dll.hp816x_TLS_zeroingAll.restype = ViStatus

    __dll.hp816x_TLS_zeroingEx.argtypes = [ViSession, ViInt32]
    __dll.hp816x_TLS_zeroingEx.restype = ViStatus

    __dll.hp816x_set_TLS_autoCalibration.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_TLS_autoCalibration.restype = ViStatus

    __dll.hp816x_get_TLS_autoCalState.argtypes = [ViSession, ViInt32, ViPBoolean]
    __dll.hp816x_get_TLS_autoCalState.restype = ViStatus

    __dll.hp816x_get_TLS_accClass.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_accClass.restype = ViStatus

    __dll.hp816x_displayToLambdaZero.argtypes = [ViSession, ViInt32]
    __dll.hp816x_displayToLambdaZero.restype = ViStatus

    __dll.hp816x_get_TLS_lambdaZero_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_TLS_lambdaZero_Q.restype = ViStatus

    __dll.hp816x_set_TLS_frequencyOffset.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_TLS_frequencyOffset.restype = ViStatus

    __dll.hp816x_get_TLS_frequencyOffset_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_TLS_frequencyOffset_Q.restype = ViStatus

    __dll.hp816x_set_TLS_sweep.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViUInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_sweep.restype = ViStatus

    __dll.hp816x_TLS_sweepControl.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_TLS_sweepControl.restype = ViStatus

    __dll.hp816x_get_TLS_sweepState_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_sweepState_Q.restype = ViStatus

    __dll.hp816x_TLS_sweepNextStep.argtypes = [ViSession, ViInt32]
    __dll.hp816x_TLS_sweepNextStep.restype = ViStatus

    __dll.hp816x_TLS_sweepPreviousStep.argtypes = [ViSession, ViInt32]
    __dll.hp816x_TLS_sweepPreviousStep.restype = ViStatus

    __dll.hp816x_TLS_sweepWait.argtypes = [ViSession, ViInt32]
    __dll.hp816x_TLS_sweepWait.restype = ViStatus

    __dll.hp816x_set_TLS_modulation.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViInt32,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_modulation.restype = ViStatus

    __dll.hp816x_get_TLS_modulationSettings_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPBoolean,
        ViPBoolean,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_modulationSettings_Q.restype = ViStatus

    __dll.hp816x_TLS_configureBNC.argtypes = [ViSession, ViInt32, ViInt32]
    __dll.hp816x_TLS_configureBNC.restype = ViStatus

    __dll.hp816x_get_TLS_BNC_config_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_BNC_config_Q.restype = ViStatus

    __dll.hp816x_set_TLS_ccLevel.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_TLS_ccLevel.restype = ViStatus

    __dll.hp816x_get_TLS_ccLevel_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_TLS_ccLevel_Q.restype = ViStatus

    __dll.hp816x_set_TLS_SBSLevel.argtypes = [ViSession, ViInt32, ViReal64]
    __dll.hp816x_set_TLS_SBSLevel.restype = ViStatus

    __dll.hp816x_get_TLS_SBSLevel_Q.argtypes = [ViSession, ViInt32, ViPReal64]
    __dll.hp816x_get_TLS_SBSLevel_Q.restype = ViStatus

    __dll.hp816x_set_TLS_SBS_control.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
    ]
    __dll.hp816x_set_TLS_SBS_control.restype = ViStatus

    __dll.hp816x_get_TLS_SBS_control_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
        ViPReal64,
    ]
    __dll.hp816x_get_TLS_SBS_control_Q.restype = ViStatus

    __dll.hp816x_get_TLS_powerPoints_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_powerPoints_Q.restype = ViStatus

    __dll.hp816x_get_TLS_powerData_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViAReal64,
        ViAReal64,
    ]
    __dll.hp816x_get_TLS_powerData_Q.restype = ViStatus

    __dll.hp816x_set_TLS_lambdaLoggingState.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_set_TLS_lambdaLoggingState.restype = ViStatus

    __dll.hp816x_get_TLS_lambdaLoggingState_Q.argtypes = [ViSession, ViPBoolean]
    __dll.hp816x_get_TLS_lambdaLoggingState_Q.restype = ViStatus

    __dll.hp816x_set_TLS_lambdaLOggingStateEx.argtypes = [ViSession, ViInt32, ViBoolean]
    __dll.hp816x_set_TLS_lambdaLOggingStateEx.restype = ViStatus

    __dll.hp816x_get_TLS_lambdaLOggingStateEx_Q.argtypes = [
        ViSession,
        ViInt32,
        ViPBoolean,
    ]
    __dll.hp816x_get_TLS_lambdaLOggingStateEx_Q.restype = ViStatus

    __dll.hp816x_get_TLS_wavelengthPoints_Q.argtypes = [ViSession, ViPInt32]
    __dll.hp816x_get_TLS_wavelengthPoints_Q.restype = ViStatus

    __dll.hp816x_get_TLS_wavelengthPointsEx_Q.argtypes = [ViSession, ViInt32, ViPInt32]
    __dll.hp816x_get_TLS_wavelengthPointsEx_Q.restype = ViStatus

    __dll.hp816x_get_TLS_wavelengthData_Q.argtypes = [ViSession, ViInt32, ViAReal64]
    __dll.hp816x_get_TLS_wavelengthData_Q.restype = ViStatus

    __dll.hp816x_get_TLS_wavelengthDataEx_Q.argtypes = [
        ViSession,
        ViInt32,
        ViInt32,
        ViAReal64,
    ]
    __dll.hp816x_get_TLS_wavelengthDataEx_Q.restype = ViStatus

    __dll.hp816x_set_LambdaScan_wavelength.argtypes = [ViSession, ViReal64]
    __dll.hp816x_set_LambdaScan_wavelength.restype = ViStatus

    __dll.hp816x_enableHighSweepSpeed.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_enableHighSweepSpeed.restype = ViStatus

    __dll.hp816x_prepareLambdaScan.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViInt32,
        ViInt32,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViPUInt32,
        ViPUInt32,
    ]
    __dll.hp816x_prepareLambdaScan.restype = ViStatus

    __dll.hp816x_getLambdaScanParameters_Q.argtypes = [
        ViSession,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_getLambdaScanParameters_Q.restype = ViStatus

    __dll.hp816x_executeLambdaScan.argtypes = [
        ViSession,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
        ViAReal64,
    ]
    __dll.hp816x_executeLambdaScan.restype = ViStatus

    __dll.hp816x_returnEquidistantData.argtypes = [ViSession, ViBoolean]
    __dll.hp816x_returnEquidistantData.restype = ViStatus

    __dll.hp816x_registerMainframe.argtypes = [ViSession]
    __dll.hp816x_registerMainframe.restype = ViStatus

    __dll.hp816x_unregisterMainframe.argtypes = [ViSession]
    __dll.hp816x_unregisterMainframe.restype = ViStatus

    __dll.hp816x_setSweepSpeed.argtypes = [ViSession, ViInt32]
    __dll.hp816x_setSweepSpeed.restype = ViStatus

    __dll.hp816x_prepareMfLambdaScan.argtypes = [
        ViSession,
        ViInt32,
        ViReal64,
        ViInt32,
        ViInt32,
        ViInt32,
        ViReal64,
        ViReal64,
        ViReal64,
        ViPUInt32,
        ViPUInt32,
    ]
    __dll.hp816x_prepareMfLambdaScan.restype = ViStatus

    __dll.hp816x_getMFLambdaScanParameters_Q.argtypes = [
        ViSession,
        ViPReal64,
        ViPReal64,
        ViPReal64,
        ViPReal64,
    ]
    __dll.hp816x_getMFLambdaScanParameters_Q.restype = ViStatus

    __dll.hp816x_executeMFLambdaScan.argtypes = [ViSession, ViAReal64]
    __dll.hp816x_executeMFLambdaScan.restype = ViStatus

    __dll.hp816x_getLambdaScanResult.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
        ViAReal64,
        ViAReal64,
    ]
    __dll.hp816x_getLambdaScanResult.restype = ViStatus

    __dll.getNoOfRegPWMChannels_Q.argtypes = [ViSession, ViPUInt32]
    __dll.getNoOfRegPWMChannels_Q.restype = ViStatus

    __dll.getChannelLocation.argtypes = [
        ViSession,
        ViInt32,
        ViPInt32,
        ViPInt32,
        ViPInt32,
    ]
    __dll.getChannelLocation.restype = ViStatus

    __dll.hp816x_excludeChannel.argtypes = [ViSession, ViInt32]
    __dll.hp816x_excludeChannel.restype = ViStatus

    __dll.hp816x_setInitialRangeParams.argtypes = [
        ViSession,
        ViInt32,
        ViBoolean,
        ViReal64,
        ViReal64,
    ]
    __dll.hp816x_setInitialRangeParams.restype = ViStatus

    __dll.hp816x_setScanAttenuation.argtypes = [ViSession, ViReal64]
    __dll.hp816x_setScanAttenuation.restype = ViStatus

    def __init__(
        self, model_name: Hp816xModel, resourceName: str, IDQuery: bool, reset: bool
    ):
        self.__model_name = model_name

        self.__handle = ViSession()
        self.__check_error(
            self.__dll.hp816x_init(
                resourceName.encode("ascii"), IDQuery, reset, byref(self.__handle)
            )
        )

    def close(self):
        self.__check_error(self.__dll.hp816x_close(self.__handle))

    def error_message(self, errorCode: ViStatus) -> str:
        errorMessage = (ViChar * ERROR_MSG_BUFFER_SIZE)()
        self.__dll.hp816x_error_message(self.__handle, errorCode, errorMessage)
        return errorMessage.value.decode("ascii")

    def __del__(self):
        self.close()

    def __check_error(self, status: ViStatus, additional_info: str = ""):
        if status.value != VI_SUCCESS.value:
            raise InstrumentError(f"{self.error_message(status)};{additional_info}")

    def getHandle(self):
        Instrument_Handle = ViSession()
        self.__check_error(
            self.__dll.hp816x_getHandle(self.__handle, byref(Instrument_Handle))
        )
        return Instrument_Handle

    def revision_Q(self):
        driverRevision = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        firmwareRevision = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_revision_Q(
                self.__handle, driverRevision, firmwareRevision
            )
        )
        return driverRevision.value.decode("ascii"), firmwareRevision.value.decode(
            "ascii"
        )

    def self_test(self):
        self_testResult = ViInt16()
        self_test_Message = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_self_test(
                self.__handle, byref(self_testResult), self_test_Message
            )
        )
        return self_testResult.value, self_test_Message.value.decode("ascii")

    def timeOut(self, timeout: int):
        self.__check_error(
            self.__dll.hp816x_timeOut(self.__handle, cast(ViInt32, timeout))
        )

    def timeOut_Q(self):
        timeout = ViInt32()
        self.__check_error(self.__dll.hp816x_timeOut_Q(self.__handle, byref(timeout)))
        return timeout.value

    @classmethod
    def getInstrumentId_Q(cls, busAddress: str):
        IDNString = (ViChar * 256)()
        cls.__dll.hp816x_getInstrumentId_Q(busAddress.encode("ascii"), IDNString)
        return IDNString.value.decode("ascii")

    @classmethod
    def listVisa_Q(cls, interface: int, select: bool):
        """
        interface:
            * 0: GPIB
            * 1: Serial
            * 2: All

        select:
            * 1: 816x
            * 0: All
        """
        numberOfDevices = ViInt32()
        listofAddresses = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        cls.__dll.hp816x_listVisa_Q(
            interface % 3, select, byref(numberOfDevices), listofAddresses
        )
        return numberOfDevices.value, listofAddresses.value.decode("ascii")

    @classmethod
    def setBaudrate(cls, interfaceIdentifier: str, baudrate: int):
        """
        baudrate:
        * 0: 9600
        * 1: 19200
        * 2: 38400
        """
        cls.__dll.hp816x_set_Baudrate(interfaceIdentifier.encode("ascii"), baudrate)

    def dcl(self):
        self.__check_error(self.__dll.hp816x_dcl(self.__handle))

    def error_query(self):
        instrumentErrorCode = ViInt32()
        errorMessage = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_error_query(
                self.__handle, byref(instrumentErrorCode), errorMessage
            )
        )
        return instrumentErrorCode.value, errorMessage.value.decode("ascii")

    def errorQueryDetect(self, automaticErrorDetection: bool):
        self.__check_error(
            self.__dll.hp816x_errorQueryDetect(
                self.__handle, cast(ViBoolean, automaticErrorDetection)
            )
        )

    def dbmToWatt(self, dbm: float):
        watt = ViReal64()
        self.__check_error(self.__dll.hp816x_dbmToWatt(self.__handle, dbm, byref(watt)))
        return watt.value

    def WattToDBm(self, watt: float):
        dbm = ViReal64()
        self.__check_error(self.__dll.hp816x_WattToDBm(self.__handle, watt, byref(dbm)))
        return dbm.value

    def setDate(self, year: int, month: int, day: int):
        self.__check_error(self.__dll.hp816x_setDate(self.__handle, year, month, day))

    def getDate(self):
        year, month, day = ViInt32(), ViInt32(), ViInt32()
        self.__check_error(
            self.__dll.hp816x_getDate(
                self.__handle, byref(year), byref(month), byref(day)
            )
        )
        return year.value, month.value, day.value

    def setTime(self, hour: int, minute: int, second: int):
        self.__check_error(
            self.__dll.hp816x_setTime(self.__handle, hour, minute, second)
        )

    def getTime(self):
        hour, minute, second = ViInt32(), ViInt32(), ViInt32()
        self.__check_error(
            self.__dll.hp816x_getTime(
                self.__handle, byref(hour), byref(minute), byref(second)
            )
        )
        return hour.value, minute.value, second.value

    def cls_(self):
        self.__check_error(self.__dll.hp816x_cls(self.__handle))

    def forceTransaction(self, forceTransaction: bool):
        self.__check_error(
            self.__dll.hp816x_forceTransaction(self.__handle, forceTransaction)
        )

    def driverLogg(self, filename: str, logging: bool, includeReplies: bool):
        self.__check_error(
            self.__dll.hp816x_driverLogg(
                self.__handle, filename.encode("ascii"), logging, includeReplies
            )
        )

    def cmd(self, commandString: str):
        self.__check_error(
            self.__dll.hp816x_cmd(self.__handle, commandString.encode("ascii"))
        )

    def cmdString_Q(self, inputQuery: str, stringSize: int):
        result = (ViChar * stringSize)()
        self.__check_error(
            self.__dll.hp816x_cmdString_Q(
                self.__handle, inputQuery.encode("ascii"), stringSize, result
            )
        )
        return result.value.decode("ascii")

    def cmdInt(self, integerCommand: str, integerValue: int):
        self.__check_error(
            self.__dll.hp816x_cmdInt(
                self.__handle, integerCommand.encode("ascii"), integerValue
            )
        )

    def cmdInt32_Q(self, integerQuery: str):
        integerResult = ViInt32()
        self.__check_error(
            self.__dll.hp816x_cmdInt32_Q(
                self.__handle, integerQuery.encode("ascii"), byref(integerResult)
            )
        )
        return integerResult.value

    def cmdReal(self, realCommand: str, realValue: float):
        self.__check_error(
            self.__dll.hp816x_cmdReal(
                self.__handle, realCommand.encode("ascii"), realValue
            )
        )

    def cmdReal64_Q(self, realQuery: str):
        realResult = ViReal64()
        self.__check_error(
            self.__dll.hp816x_cmdReal64_Q(
                self.__handle, realQuery.encode("ascii"), byref(realResult)
            )
        )
        return realResult.value

    def reset(self):
        self.__check_error(self.__dll.hp816x_reset(self.__handle))

    def preset(self):
        self.__check_error(self.__dll.hp816x_preset(self.__handle))

    def mainframeSelftest(self):
        self_testResult = ViInt16()
        self_testMessage = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_mainframeSelftest(
                self.__handle, byref(self_testResult), self_testMessage
            )
        )
        return self_testResult.value, self_testMessage.value.decode("ascii")

    def moduleSelfTest(self, slottoTest: int):
        result = ViInt16()
        self_testMessage = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_moduleSelfTest(
                self.__handle, slottoTest, byref(result), self_testMessage
            )
        )
        return result.value, self_testMessage.value.decode("ascii")

    def revision_query(self):
        driverRevision = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        firmwareRevision = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_revision_query(
                self.__handle, driverRevision, firmwareRevision
            )
        )
        return driverRevision.value.decode("ascii"), firmwareRevision.value.decode(
            "ascii"
        )

    def opc_Q(self):
        operationComplete = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_opc_Q(self.__handle, byref(operationComplete))
        )
        return bool(operationComplete.value)

    def lockUnlockInstruments(self, softlock: bool, password: str):
        self.__check_error(
            self.__dll.hp816x_lockUnlockInstruments(
                self.__handle, softlock, password.encode("ascii")
            )
        )

    def getLockState(self):
        Soft_Lock = ViBoolean()
        Remote_Interlock = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_getLockState(
                self.__handle, byref(Soft_Lock), byref(Remote_Interlock)
            )
        )
        return bool(Soft_Lock.value), bool(Remote_Interlock.value)

    def enableDisableDisplaying(self, display: bool):
        self.__check_error(
            self.__dll.hp816x_enableDisableDisplaying(self.__handle, display)
        )

    def getSlotInformation_Q(self):
        if self.__model_name == Hp816xModel.HP8163AB:
            arraySize = ViInt32(3)
        elif self.__model_name == Hp816xModel.HP8164AB:
            arraySize = ViInt32(5)
        elif self.__model_name == Hp816xModel.HP8166AB:
            arraySize = ViInt32(18)
        else:
            raise RuntimeError("Unsupported hp816x model")
        slotInformation = (ViInt32 * arraySize.value)()
        self.__check_error(
            self.__dll.hp816x_getSlotInformation_Q(
                self.__handle, byref(arraySize), slotInformation
            )
        )
        return [Hp816xSlot(x) for x in slotInformation]

    def getModuleStatus_Q(self):
        statusSummary = ViBoolean()
        maxMessageLength = ViInt32()
        if self.__model_name == Hp816xModel.HP8163AB:
            moduleStatusArray = (ViInt32 * 3)()
        elif self.__model_name == Hp816xModel.HP8164AB:
            moduleStatusArray = (ViInt32 * 5)()
        elif self.__model_name == Hp816xModel.HP8166AB:
            moduleStatusArray = (ViInt32 * 18)()
        else:
            raise RuntimeError("Unsupported hp816x model")
        self.__check_error(
            self.__dll.hp816x_getModuleStatus_Q(
                self.__handle,
                byref(statusSummary),
                moduleStatusArray,
                byref(maxMessageLength),
            )
        )
        return (
            bool(statusSummary.value),
            [x for x in moduleStatusArray],
            maxMessageLength.value,
        )

    def hp816x_convertQuestionableStatus_Q(self, questionableStatusInput: int):
        message = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_convertQuestionableStatus_Q(
                self.__handle, questionableStatusInput, message
            )
        )
        return message.value.decode("ascii")

    def standardTriggerConfiguration(
        self,
        triggerConfiguration: Hp816xTriggerConfiguration,
        nodeAInputConfig: int,
        nodeBInputConfig: int,
        outputMatrixConfigurations: int,
    ):
        self.__check_error(
            self.__dll.hp816x_standardTriggerConfiguration(
                self.__handle,
                triggerConfiguration.value,
                nodeAInputConfig,
                nodeBInputConfig,
                outputMatrixConfigurations,
            )
        )

    def standardTriggerConfiguration_Q(
        self,
    ):
        # I believe the manual has a typo in this function
        triggerConfiguration = ViInt32()
        nodeAInputConfig = ViUInt32()
        nodeBInputConfig = ViUInt32()
        outputMatrixConfigurations = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_standardTriggerConfiguration_Q(
                self.__handle,
                byref(triggerConfiguration),
                byref(nodeAInputConfig),
                byref(nodeBInputConfig),
                byref(outputMatrixConfigurations),
            )
        )
        return (
            Hp816xTriggerConfiguration(triggerConfiguration.value),
            nodeAInputConfig.value,
            nodeBInputConfig.value,
            outputMatrixConfigurations.value,
        )

    def generateTrigger(self, triggerAt: Hp816xNode):
        self.__check_error(
            self.__dll.hp816x_generateTrigger(self.__handle, ViBoolean(triggerAt.value))
        )

    @classmethod
    def nodeInputConfiguration(
        cls,
        connectionFunctionNodeA: bool,
        BNCTriggerConnectorA: bool,
        nodeBTriggerOutput: bool,
        slotA0: bool,
        slotA1: bool,
        slotA2: bool,
        slotA3: bool,
        slotA4: bool,
        BNCTriggerConnectorB: bool,
        nodeATriggerOutput: bool,
        slotB0: bool,
        slotB1: bool,
        slotB2: bool,
        slotB3: bool,
        slotB4: bool,
    ):
        nodeAInputConfiguration = ViUInt32()
        nodeBInputConfiguration = ViUInt32()
        cls.__dll.hp816x_nodeInputConfiguration(
            connectionFunctionNodeA,
            BNCTriggerConnectorA,
            nodeBTriggerOutput,
            slotA0,
            slotA1,
            slotA2,
            slotA3,
            slotA4,
            BNCTriggerConnectorB,
            nodeATriggerOutput,
            slotB0,
            slotB1,
            slotB2,
            slotB3,
            slotB4,
            byref(nodeAInputConfiguration),
            byref(nodeBInputConfiguration),
        )
        return nodeAInputConfiguration.value, nodeBInputConfiguration.value

    @classmethod
    def trigOutConfiguration(
        cls, nodeswitchedtoBNCOutput, slot0, slot1, slot2, slot3, slot4
    ):
        outputMatrixConfiguration = ViUInt32()
        cls.__dll.hp816x_nodeInputConfiguration(
            nodeswitchedtoBNCOutput,
            slot0,
            slot1,
            slot2,
            slot3,
            slot4,
            byref(outputMatrixConfiguration),
        )
        return outputMatrixConfiguration.value

    def set_ATT_attenuation(
        self,
        ATTSlot: int,
        selection: Hp816xSelect,
        attenuation: float,
        waitforCompletion: bool,
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_attenuation(
                self.__handle, ATTSlot, selection.value, attenuation, waitforCompletion
            )
        )

    def get_ATT_attenuation_Q(self, AttSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_attenuation_Q(
                self.__handle,
                AttSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def set_ATT_attenuationOffset(
        self, selection: Hp816xSelect, offset: float, ATTSlot: int
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_attenuationOffset(
                self.__handle, selection.value, offset, ATTSlot
            )
        )

    def get_ATT_attenuationOffset_Q(self, ATTSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_attenuation_Q(
                self.__handle,
                ATTSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def set_ATT_attenuatorSpeed(
        self, ATTSlot: int, selection: Hp816xSelect, speed: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_attenuatorSpeed(
                self.__handle, ATTSlot, selection.value, speed
            )
        )

    def get_ATT_attenuatorSpeed_Q(self, ATTSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_attenuatorSpeed_Q(
                self.__handle,
                ATTSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def ATT_displayToOffset(self, ATTSlot: int):
        self.__check_error(
            self.__dll.hp816x_ATT_displayToOffset(self.__handle, ATTSlot)
        )

    def set_ATT_wavelength(
        self, ATTSlot: int, selection: Hp816xSelect, wavelength: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_wavelength(
                self.__handle, ATTSlot, selection.value, wavelength
            )
        )

    def get_ATT_wavelength_Q(self, ATTSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_wavelength_Q(
                self.__handle,
                ATTSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def set_ATT_powerUnit(self, ATTSlot: int, unit: Hp816xPowerUnit):
        self.__check_error(
            self.__dll.hp816x_set_ATT_powerUnit(self.__handle, ATTSlot, unit.value)
        )

    def get_ATT_powerUnit_Q(self, ATTSlot: int):
        unit = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_ATT_powerUnit(self.__handle, byref(unit), ATTSlot)
        )
        return Hp816xPowerUnit(unit.value)

    def set_ATT_absPowerMode(self, ATTSlot: int, absolutePowerMode: bool):
        self.__check_error(
            self.__dll.hp816x_set_ATT_absPower(
                self.__handle, ATTSlot, absolutePowerMode
            )
        )

    def get_ATT_absPowerMode_Q(self, ATTSlot: int):
        absolutePowerMode = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_ATT_wavelength_Q(
                self.__handle, ATTSlot, byref(absolutePowerMode)
            )
        )
        return bool(absolutePowerMode.value)

    def set_ATT_power(
        self,
        ATTSlot: int,
        powerControl: bool,
        powerUnit: Hp816xPowerUnit,
        selection: Hp816xSelect,
        power: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_power(
                self.__handle,
                ATTSlot,
                powerControl,
                powerUnit.value,
                selection.value,
                power,
            )
        )

    def get_ATT_power_Q(self, ATTSlot: int):
        powerControl = ViBoolean()
        powerUnit = ViBoolean()
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_power_Q(
                self.__handle,
                ATTSlot,
                byref(powerControl),
                byref(powerUnit),
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return (
            powerControl.value,
            Hp816xPowerUnit(powerUnit.value),
            minimum.value,
            maximum.value,
            default.value,
            current.value,
        )

    def cp_ATT_refFromExtPM(self, ATTSlot: int, PWMSlot: int, channel: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_cp_ATT_refFromExtPM(
                self.__handle, ATTSlot, PWMSlot, channel.value
            )
        )

    def set_ATT_powerReference(
        self, ATTSlot: int, selection: Hp816xSelect, reference: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_powerReference(
                self.__handle, ATTSlot, selection.value, reference
            )
        )

    def get_ATT_powerReference_Q(self, ATTSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_powerReference_Q(
                self.__handle,
                ATTSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def set_ATT_shutterState(self, ATTSlot: int, shutterState: bool):
        self.__check_error(
            self.__dll.hp816x_set_ATT_shutterState(self.__handle, ATTSlot, shutterState)
        )

    def get_ATT_shutterState_Q(self, ATTSlot: int):
        shutterState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_ATT_shutterState_Q(
                self.__handle, ATTSlot, byref(shutterState)
            )
        )
        return bool(shutterState.value)

    def set_ATT_shutterAtPowerOn(self, ATTSlot: int, shutterState: bool):
        self.__check_error(
            self.__dll.hp816x_set_ATT_shutterState(self.__handle, ATTSlot, shutterState)
        )

    def get_ATT_shutterAtPowerOn_Q(self, ATTSlot: int):
        shutterState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_ATT_shutterAtPowerOn_Q(
                self.__handle, ATTSlot, byref(shutterState)
            )
        )
        return bool(shutterState.value)

    def get_ATT_operStatus(self, ATTSlot: int):
        value = ViUInt32()
        conditionalInfo = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_get_ATT_operStatus(
                self.__handle, ATTSlot, byref(value), conditionalInfo
            )
        )
        return value.value, conditionalInfo.value.decode("ascii")

    def set_ATT_wlOffsRefPowermeter(
        self, ATTSlot: int, PWMSlot: int, channel: Hp816xChan
    ):
        self.__check_error(
            self.__dll.hp816x_set_ATT_wlOffsRefPowermeter(
                self.__handle, ATTSlot, PWMSlot, channel.value
            )
        )

    def get_ATT_wlOffsRefPowermeter_Q(self, ATTSlot: int):
        slot = ViInt32()
        channel = ViInt32()
        self.__check_error(
            self.__dll.hp816x_set_ATT_wlOffsRefPowermeter(
                self.__handle, ATTSlot, byref(slot), byref(channel)
            )
        )
        return slot.value, channel.value

    def set_ATT_wavelengthOffsetState(self, ATTSlot: int, offsetDependant: bool):
        self.__check_error(
            self.__dll.hp816x_set_ATT_wavelengthOffsetState(
                self.__handle, ATTSlot, offsetDependant
            )
        )

    def get_ATT_wavelengthOffsetState_Q(self, ATTSlot: int):
        offsetDependancy = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_ATT_wavelengthOffsetState_Q(
                self.__handle, ATTSlot, byref(offsetDependancy)
            )
        )
        return bool(offsetDependancy.value)

    def set_ATT_wavelengthOffset(
        self, ATTSlot: int, wavelength: float, offsetSource: bool, offsetValue: float
    ):
        self.__check_error(
            self.__dll.__hp816x_set_ATT_wavelengthOffset(
                self.__handle, ATTSlot, wavelength, offsetSource, offsetValue
            )
        )

    def get_ATT_wavelengthOffsetIndex_Q(self, ATTSlot: int, tableIndex: int):
        wavelength = ViReal64()
        offset = ViReal64()
        self.__check_error(
            self.__dll.__hp816x_get_ATT_wavelengthOFfsetIndex_Q(
                self.__handle, ATTSlot, tableIndex, byref(wavelength), byref(offset)
            )
        )
        return wavelength.value, offset.value

    def get_ATT_offsetFromWavelength_Q(self, ATTSlot: int, wavelength: float):
        offset = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_offsetFromWavelength_Q(
                self.__handle, ATTSlot, wavelength, byref(offset)
            )
        )
        return offset.value

    def delete_ATT_offsetTblEntries(
        self, ATTSlot: int, noOfEntries: bool, wavelengthOrIndex: float
    ):
        self.__check_error(
            self.__dll.hp816x_delete_ATT_offsetTblEntries(
                self.__handle, ATTSlot, noOfEntries, wavelengthOrIndex
            )
        )

    def get_ATT_offsetTable_Q(
        self, ATTSlot: int, wavelengthArray_size: int, offsetArray_size: int
    ):
        wavelengthArray = (ViReal64 * wavelengthArray_size)()
        offsetArray = (ViReal64 * offsetArray_size)()
        self.__check_error(
            self.__dll.hp816x_get_ATT_offsetTable_Q(
                self.__handle, ATTSlot, wavelengthArray, offsetArray
            )
        )
        return [x for x in wavelengthArray], [x for x in offsetArray]

    def get_ATT_offsetTblSize_Q(self, ATTSlot: int):
        currentSize = ViUInt32()
        maximumSize = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_get_ATT_offsetTblSize_Q(
                self.__handle, ATTSlot, byref(currentSize), byref(maximumSize)
            )
        )
        return currentSize.value, maximumSize.value

    def read_ATT_outputPower(self, ATTSlot: int):
        Output_Power = (ViReal64 * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_read_ATT_outputPower(self.__handle, ATTSlot, Output_Power)
        )
        return [x for x in Output_Power]

    def fetch_ATT_outputPower(self, ATTSlot: int):
        Output_Power = (ViReal64 * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_fetch_ATT_outputPower(
                self.__handle, ATTSlot, Output_Power
            )
        )
        return [x for x in Output_Power]

    def set_ATT_powerOffset(self, ATTSlot: int, selection: Hp816xSelect, offset: float):
        self.__check_error(
            self.__dll.hp816x_set_ATT_powerOffset(
                self.__handle, ATTSlot, selection.value, offset
            )
        )

    def get_ATT_powerOffset_Q(self, ATTSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        default = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_powerOffset_Q(
                self.__handle,
                ATTSlot,
                byref(minimum),
                byref(maximum),
                byref(default),
                byref(current),
            )
        )
        return minimum.value, maximum.value, default.value, current.value

    def set_ATT_pwrOffsRefPM(self, ATTSlot: int, PWMSLot: int, PWMChannel: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_set_ATT_pwrOffsRefPM(
                self.__handle, ATTSlot, PWMSLot, PWMChannel.value
            )
        )

    def set_ATT_offsByRefPM(self, ATTSlot: int, PWMSlot: int, PWMChannel: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_set_ATT_offsByRefPM(
                self.__handle, ATTSlot, PWMSlot, PWMChannel.value
            )
        )

    def set_ATT_controlLoopState(self, ATTSlot: int, controlLoop: bool):
        self.__check_error(
            self.__dll.hp816x_set_ATT_controlLoopState(
                self.__handle, ATTSlot, controlLoop
            )
        )

    def get_ATT_controlLoopState_Q(self, ATTSlot: int):
        controlLoop = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_set_ATT_controlLoopState(
                self.__handle, ATTSlot, byref(controlLoop)
            )
        )
        return bool(controlLoop.value)

    def set_ATT_avTime(self, ATTSlot: int, averagingTime: float):
        self.__check_error(
            self.__dll.hp816x_set_ATT_avTime(self.__handle, ATTSlot, averagingTime)
        )

    def get_ATT_avTime_Q(self, ATTSlot: int):
        averagingTime = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_ATT_avTime_Q(
                self.__handle, ATTSlot, byref(averagingTime)
            )
        )
        return averagingTime.value

    def set_ATT_TriggerConfig(self, ATT_Slot: int, Trigger_In: Hp816xPWMTrigIn):
        self.__check_error(
            self.__dll.hp816x_set_ATT_TriggerConfig(
                self.__handle, ATT_Slot, Trigger_In.value
            )
        )

    def get_ATT_TriggerConfig_Q(self, ATT_Slot: int):
        Trigger_In = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_ATT_TriggerConfig_Q(
                self.__handle, ATT_Slot, byref(Trigger_In)
            )
        )
        return Hp816xPWMTrigIn(Trigger_In.value)

    def zero_ATT_powermeter(self, ATTSlot: int):
        self.__check_error(
            self.__dll.hp816x_zero_ATT_powermeter(self.__handle, ATTSlot)
        )

    def get_ATT_zeroResult_Q(self, ATTSlot):
        lastZeroResult = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_ATT_zeroResult_Q(
                self.__handle, ATTSlot, byref(lastZeroResult)
            )
        )
        return lastZeroResult.value

    def zero_ATT_all(self):
        self.__check_error(self.__dll.hp816x_zero_ATT_all(self.__handle))

    def spectralCalibration(self, Slot: int, Size_of_Spectrum: int):
        Wavelength = (ViReal64 * Size_of_Spectrum)()
        Power = (ViReal64 * Size_of_Spectrum)()
        Wavelength_Result = ViReal64()
        Error_Diagnose = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        status = self.__dll.hp816x_spectralCalibration(
            self.__handle,
            Slot,
            Size_of_Spectrum,
            Wavelength,
            Power,
            byref(Wavelength_Result),
            Error_Diagnose,
        )
        if status.value != VI_SUCCESS.value:
            self.__check_error(
                status, additional_info=Error_Diagnose.value.decode("ascii")
            )
        return (
            [x for x in Wavelength],
            [x for x in Power],
            Wavelength_Result.value,
        )

    def getWlRespTblSize(self, ATT_Slot: int):
        Size = ViUInt32()
        CSV_Size = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_getWlRespTblSize(
                self.__handle, ATT_Slot, byref(Size), byref(CSV_Size)
            )
        )
        return Size.value, CSV_Size.value

    def readWlRespTable(self, ATT_Slot: int, size: int):
        Wavelength = (ViReal64 * size)()
        Response_Factor = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_readWlRespTable(
                self.__handle, ATT_Slot, size, Wavelength, Response_Factor
            )
        )
        return [x for x in Wavelength], [x for x in Response_Factor]

    def readWlRepTblCSV(self, ATT_Slot: int, size: int):
        CSV_List = (ViChar * size)()
        self.__check_error(
            self.__dll.hp816x_readWlRepTblCSV(self.__handle, ATT_Slot, CSV_List)
        )
        return CSV_List.value.decode("ascii")

    def PWM_slaveChannelCheck(self, PWMSlot: int, slaveChannelCheck: bool):
        self.__check_error(
            self.__dll.hp816x_PWM_slaveChannelCheck(
                self.__handle, PWMSlot, slaveChannelCheck
            )
        )

    def set_PWM_parameters(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        rangeMode: Hp816xPWMRangeMode,
        powerUnit: Hp816xPowerUnit,
        internalTrigger: Hp816xPWMTrigger,
        wavelength: float,
        averagingTime: float,
        powerRange: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_parameters(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                rangeMode.value,
                powerUnit.value,
                internalTrigger.value,
                wavelength,
                averagingTime,
                powerRange,
            )
        )

    def get_PWM_parameters_Q(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
    ):
        rangeMode = ViBoolean()
        powerUnit = ViBoolean()
        internalTrigger = ViInt32()
        wavelength = ViReal64()
        averagingTime = ViReal64()
        powerRange = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_parameters_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(rangeMode),
                byref(powerUnit),
                byref(internalTrigger),
                byref(wavelength),
                byref(averagingTime),
                byref(powerRange),
            )
        )
        return (
            Hp816xPWMRangeMode(rangeMode.value),
            Hp816xPowerUnit(powerUnit.value),
            Hp816xPWMTrigger(internalTrigger.value),
            wavelength.value,
            averagingTime.value,
            powerRange.value,
        )

    def set_PWM_averagingTime(
        self, PWMSlot: int, channelNumber: Hp816xChan, averagingTime: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_averagingTime(
                self.__handle, PWMSlot, channelNumber.value, averagingTime
            )
        )

    def get_PWM_averagingTime_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        averagingTime = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_averagingTime_Q(
                self.__handle, PWMSlot, channelNumber.value, byref(averagingTime)
            )
        )
        return averagingTime.value

    def set_PWM_wavelength(
        self, PWMSlot: int, channelNumber: Hp816xChan, wavelength: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_wavelength(
                self.__handle, PWMSlot, channelNumber.value, wavelength
            )
        )

    def get_PWM_wavelength_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        minWavelength = ViReal64()
        maxWavelength = ViReal64()
        currentWavelength = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_wavelength_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(currentWavelength),
                byref(minWavelength),
                byref(maxWavelength),
            )
        )
        return minWavelength.value, maxWavelength.value, currentWavelength.value

    def set_PWM_calibration(
        self, PWMSlot: int, channelNumber: Hp816xChan, calibration: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_calibration(
                self.__handle, PWMSlot, channelNumber.value, calibration
            )
        )

    def get_PWM_calibration_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        calibration = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_calibration_Q(
                self.__handle, PWMSlot, channelNumber.value, byref(calibration)
            )
        )
        return calibration.value

    def set_PWM_powerRange(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        rangeMode: Hp816xPWMRangeMode,
        powerRange: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_powerRange(
                self.__handle, PWMSlot, channelNumber.value, rangeMode.value, powerRange
            )
        )

    def get_PWM_powerRange_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        rangeMode = ViBoolean()
        powerRange = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_powerRange_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(rangeMode),
                byref(powerRange),
            )
        )
        return Hp816xPWMRangeMode(rangeMode.value), powerRange.value

    def set_PWM_powerUnit(
        self, PWMSlot: int, channelNumber: Hp816xChan, powerUnit: Hp816xPowerUnit
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_powerUnit(
                self.__handle, PWMSlot, channelNumber.value, powerUnit.value
            )
        )

    def get_PWM_powerUnit_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        powerUnit = ViInt32()
        self.__check_error(
            self.__dll.hp816x_set_PWM_powerUnit(
                self.__handle, PWMSlot, channelNumber.value, byref(powerUnit)
            )
        )
        return Hp816xPowerUnit(powerUnit)

    def set_PWM_referenceSource(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        measureMode: Hp816xPWMMeasureMode,
        referenceSource: Hp816xPWMReferenceSource,
        slot: int,
        channel: Hp816xChan,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_referenceSource(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                measureMode.value,
                referenceSource.value,
                slot,
                channel.value,
            )
        )

    def get_PWM_referenceSource_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        measureMode = ViInt32()
        referenceSource = ViInt32()
        slot = ViInt32()
        channel = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_PWM_referenceSource_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(measureMode),
                byref(referenceSource),
                byref(slot),
                byref(channel),
            )
        )
        return (
            Hp816xPWMMeasureMode(measureMode.value),
            Hp816xPWMReferenceSource(referenceSource.value),
            slot.value,
            Hp816xChan(channel),
        )

    def set_PWM_referenceValue(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        internalReference: float,
        referenceChannel: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_referenceValue(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                internalReference,
                referenceChannel,
            )
        )

    def get_PWM_referenceValue_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        referenceMode = ViInt32()
        internalReference = ViReal64()
        referenceChannel = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_referenceValue_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(referenceMode),
                byref(internalReference),
                byref(referenceChannel),
            )
        )
        return (
            Hp816xPWMReferenceSource(referenceMode.value),
            internalReference.value,
            referenceChannel.value,
        )

    def set_PWM_triggerConfiguration(
        self,
        PWMSlot: int,
        triggerIn: Hp816xPWMTrigIn,
        triggerOut: Hp816xPWMTrigOut,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_triggerConfiguration(
                self.__handle, PWMSlot, triggerIn.value, triggerOut.value
            )
        )

    def get_PWM_triggerConfiguration(self, PWMSlot: int):
        triggerIn = ViInt32()
        triggerOut = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_PWM_triggerConfiguration(
                self.__handle, PWMSlot, byref(triggerIn), byref(triggerOut)
            )
        )
        return Hp816xPWMTrigIn(triggerIn.value), Hp816xPWMTrigOut(triggerOut.value)

    def PWM_displayToReference(self, PWMSlot, channelNumber: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_PWM_displayToReference(
                self.__handle, PWMSlot, channelNumber.value
            )
        )

    def set_PWM_internalTrigger(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        internalTrigger: Hp816xPWMTrigger,
    ):
        self.__check_error(
            self.__dll.hp816x_set_PWM_internalTrigger(
                self.__handle, PWMSlot, channelNumber.value, internalTrigger.value
            )
        )

    def start_PWM_internalTrigger(self, PWMSlot: int, channelNumber: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_start_PWM_internalTrigger(
                self.__handle, PWMSlot, channelNumber.value
            )
        )

    def PWM_readValue(self, PWMSlot: int, channelNumber: Hp816xChan):
        measuredValue = ViReal64()
        self.__check_error(
            self.__dll.hp816x_PWM_readValue(
                self.__handle, PWMSlot, channelNumber.value, byref(measuredValue)
            )
        )
        return measuredValue.value

    def PWM_fetchValue(self, PWMSlot: int, channelNumber: Hp816xChan):
        measuredValue = ViReal64()
        self.__check_error(
            self.__dll.hp816x_PWM_fetchValue(
                self.__handle, PWMSlot, channelNumber.value, byref(measuredValue)
            )
        )
        return measuredValue.value

    def PWM_readAll(self, size: int):
        Number_of_Channels = ViReal64()
        Slots = (ViInt32 * size)()
        Channels = (ViInt32 * size)()
        Values = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_PWM_readAll(
                self.__handle, byref(Number_of_Channels), Slots, Channels, Values
            )
        )
        return (
            Number_of_Channels.value,
            [x for x in Slots],
            [Hp816xChan(x) for x in Channels],
            [x for x in Values],
        )

    def PWM_zeroing(self, PWMSlot: int, channelNumber: Hp816xChan):
        zeroingResult = ViInt32()
        self.__check_error(
            self.__dll.hp816x_PWM_zeroing(
                self.__handle, byref(zeroingResult), PWMSlot, channelNumber.value
            )
        )
        return zeroingResult.value

    def PWM_zeroingAll(self):
        summaryofZeroingAll = ViInt32()
        self.__check_error(
            self.__dll.hp816x_PWM_zeroingAll(self.__handle, byref(summaryofZeroingAll))
        )
        return summaryofZeroingAll.value

    def PWM_ignoreError(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        ignoreError: bool,
        instrumentErrorNumber: int,
    ):
        self.__check_error(
            self.__dll.hp816x_PWM_ignoreError(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                ignoreError,
                instrumentErrorNumber,
            )
        )

    def set_PWM_logging(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        averagingTime: float,
        dataPoints: int,
    ):
        estimatedTimeout = ViInt32()
        self.__check_error(
            self.__dll.hp816x_set_PWM_logging(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                averagingTime,
                dataPoints,
                byref(estimatedTimeout),
            )
        )
        return estimatedTimeout.value

    def get_PWM_loggingResults_Q(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        waitforCompletion: bool,
        resultUnit: Hp816xPowerUnit,
        size: int,
    ):
        loggingStatus = ViBoolean()
        loggingResult = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_PWM_loggingResults_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                waitforCompletion,
                resultUnit.value,
                byref(loggingStatus),
                loggingResult,
            )
        )
        return bool(loggingStatus.value), [x for x in loggingResult]

    def set_PWM_stability(
        self,
        PLWSlot: int,
        channelNumber: Hp816xChan,
        averagingTime: float,
        delayTime: float,
        totalTime: float,
    ):
        estimatedResults = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_set_PWM_stability(
                self.__handle,
                PLWSlot,
                channelNumber.value,
                averagingTime,
                delayTime,
                totalTime,
                byref(estimatedResults),
            )
        )
        return estimatedResults.value

    def get_PWM_stability_Q(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        waitforCompletion: bool,
        resultUnit: Hp816xPowerUnit,
        size: int,
    ):
        stabilityStatus = ViBoolean()
        stabilityResult = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_PWM_stability_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                waitforCompletion,
                resultUnit.value,
                byref(stabilityStatus),
                stabilityResult,
            )
        )
        return bool(stabilityStatus.value), [x for x in stabilityResult]

    def set_PWM_minMax(
        self,
        PWMSlot: int,
        channelNumber: Hp816xChan,
        minmaxMode: Hp816xMinMaxMode,
        dataPoints: int,
    ):
        estimatedTime = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_set_PWM_minMax(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                minmaxMode.value,
                dataPoints,
                byref(estimatedTime),
            )
        )
        return estimatedTime.value

    def get_PWM_minMaxResults_Q(self, PWMSlot: int, channelNumber: Hp816xChan):
        minimum = ViReal64()
        maximum = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_PWM_minMaxResults_Q(
                self.__handle,
                PWMSlot,
                channelNumber.value,
                byref(minimum),
                byref(maximum),
                byref(current),
            )
        )
        return minimum.value, maximum.value, current.value

    def PWM_functionStop(self, PWMSlot: int, channelNumber: Hp816xChan):
        self.__check_error(
            self.__dll.hp816x_PWM_functionStop(self.__handle, PWMSlot, channelNumber)
        )

    def spectralCalibrationEx(
        self,
        Slot: int,
        channelNumber: Hp816xChan,
        Size_of_Spectrum: int,
        Wavelength: list[float],
        Power: list[float],
    ):
        wl = (ViReal64 * len(Wavelength))(*Wavelength)
        pw = (ViReal64 * len(Power))(*Power)
        Wavelength_Result = ViReal64()
        Error_Diagnose = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        status = self.__dll.hp816x_spectralCalibrationEx(
            self.__handle,
            Slot,
            channelNumber.value,
            Size_of_Spectrum,
            wl,
            pw,
            byref(Wavelength_Result),
            Error_Diagnose,
        )
        if status.value != VI_SUCCESS.value:
            self.__check_error(
                status, additional_info=Error_Diagnose.value.decode("ascii")
            )
        return Wavelength_Result.value

    def getWlRespTblSizeEx(self, Slot: int, channelNumber: Hp816xChan):
        Size = ViUInt32()
        CSV_Size = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_getWlRespTblSizeEx(
                self.__handle, Slot, channelNumber.value, byref(Size), byref(CSV_Size)
            )
        )
        return Size.value, CSV_Size.value

    def readWlRespTableEx(self, Slot: int, channelNumber: Hp816xChan, size: int):
        wl = (ViReal64 * size)()
        pw = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_readWlRespTableEx(
                self.__handle, Slot, channelNumber.value, wl, pw
            )
        )
        return [x for x in wl], [x for x in pw]

    def readWlRepTblCSV_Ex(self, Slot: int, channelNumber: Hp816xChan, size: int):
        CSV_List = (ViChar * size)()
        self.__check_error(
            self.__dll.hp816x_readWlRepTblCSV_Ex(
                self.__handle, Slot, channelNumber.value, CSV_List
            )
        )
        return CSV_List.value.decode("ascii")

    def set_FLS_parameters(
        self,
        FLSSlot: int,
        wavelengthSource: Hp816xSource,
        turnLaser: bool,
        modulationLowerSource: Hp816xModulationSource,
        modulationUpperSource: Hp816xModulationSource,
        modulationFreqLowerSource: float,
        modulationFreqUpperSource: float,
        attenuationLowerSource: float,
        attenuationUpperSource: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_FLS_parameters(
                self.__dll.hp816x_set_FLS_parameters(
                    self.__handle,
                    FLSSlot,
                    wavelengthSource.value,
                    turnLaser,
                    modulationLowerSource.value,
                    modulationUpperSource.value,
                    modulationFreqLowerSource,
                    modulationFreqUpperSource,
                    attenuationLowerSource,
                    attenuationUpperSource,
                )
            )
        )

    def get_FLS_parameters_Q(self, FLSSlot: int):
        wavelengthSource = ViInt32()
        turnLaser = ViBoolean()
        modulationLowerSource = ViInt32()
        modulationUpperSource = ViInt32()
        modulationFreqLowerSource = ViReal64()
        modulationFreqUpperSource = ViReal64()
        attenuationLowerSource = ViReal64()
        attenuationUpperSource = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_FLS_parameters_Q(
                self.__handle,
                FLSSlot,
                byref(wavelengthSource),
                byref(turnLaser),
                byref(modulationLowerSource),
                byref(modulationUpperSource),
                byref(modulationFreqLowerSource),
                byref(modulationFreqUpperSource),
                byref(attenuationLowerSource),
                byref(attenuationUpperSource),
            )
        )
        return (
            Hp816xSource(wavelengthSource.value),
            bool(turnLaser.value),
            Hp816xModulationSource(modulationLowerSource.value),
            Hp816xModulationSource(modulationUpperSource.value),
            modulationFreqLowerSource.value,
            modulationFreqUpperSource.value,
            attenuationLowerSource.value,
            attenuationUpperSource.value,
        )

    def set_FLS_modulation(
        self,
        FLSSlot: int,
        laserSource: Hp816xSource,
        modulationFrequency: Hp816xModulationFrequency,
        modulationSource: Hp816xModulationSource,
        manualFrequency: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_FLS_modulation(
                self.__handle,
                FLSSlot,
                laserSource.value,
                modulationFrequency.value,
                modulationSource.value,
                manualFrequency,
            )
        )

    def get_FLS_modulation_Q(self, FLSSLot: int, wavelengthSource: Hp816xSource):
        modulationState = ViBoolean()
        modulationSource = ViInt32()
        minimumFrequency = ViReal64()
        maximumFrequency = ViReal64()
        defaultFrequency = ViReal64()
        currentFrequency = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_FLS_modulation_Q(
                self.__handle,
                FLSSLot,
                wavelengthSource.value,
                byref(modulationState),
                byref(modulationSource),
                byref(minimumFrequency),
                byref(maximumFrequency),
                byref(defaultFrequency),
                byref(currentFrequency),
            )
        )
        return (
            bool(modulationState.value),
            Hp816xModulationSource(modulationSource.value),
            minimumFrequency.value,
            maximumFrequency.value,
            defaultFrequency.value,
            currentFrequency.value,
        )

    def set_FLS_laserSource(self, FLSSLot: int, laserSource: Hp816xModulationSource):
        self.__check_error(
            self.__dll.hp816x_set_FLS_laserSource(
                self.__handle, FLSSLot, laserSource.value
            )
        )

    def get_FLS_laserSource_Q(self, FLSSLot: int):
        laserSource = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_FLS_laserSource_Q(
                self.__handle, FLSSLot, byref(laserSource)
            )
        )
        return Hp816xSource(laserSource.value)

    def get_FLS_wavelength_Q(self, FLSSLot: int):
        wavelengthLowerSource = ViReal64()
        wavelengthUpperSource = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_FLS_wavelength_Q(
                self.__handle,
                FLSSLot,
                byref(wavelengthLowerSource),
                byref(wavelengthUpperSource),
            )
        )
        return wavelengthLowerSource.value, wavelengthUpperSource.value

    def set_FLS_attenuation(
        self, FLSSLot: int, attenuationLowerSource: float, attenuationUpperSource: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_FLS_attenuation(
                self.__handle, FLSSLot, attenuationLowerSource, attenuationUpperSource
            )
        )

    def get_FLS_attenuation_Q(self, FLSSlot: int):
        attenuationLowerSource = ViReal64()
        attenuationUpperSource = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_FLS_attenuation_Q(
                self.__handle,
                FLSSlot,
                byref(attenuationLowerSource),
                byref(attenuationUpperSource),
            )
        )
        return attenuationLowerSource.value, attenuationUpperSource.value

    def set_FLS_triggerState(self, FLSSlot: int, outputTrigger: bool):
        self.__check_error(
            self.__dll.hp816x_set_FLS_triggerState(
                self.__handle, FLSSlot, outputTrigger
            )
        )

    def get_FlS_laserState_Q(self, FLSSlot: int):
        outputTrigger = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_FLS_laserState_Q(
                self.__handle, FLSSlot, byref(outputTrigger)
            )
        )
        return bool(outputTrigger.value)

    def get_FLS_power(self, FLSSlot: int, laserSource: Hp816xSource):
        laserPower = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_FLS_power(
                self.__handle, FLSSlot, laserSource.value, byref(laserPower)
            )
        )
        return laserPower.value

    def set_FLS_laserState(self, FLSSlot: int, laserState: bool):
        self.__check_error(
            self.__dll.hp816x_set_FLS_laserState(self.__handle, FLSSlot, laserState)
        )

    def get_FLS_laserState_Q(self, FLSSlot: int):
        laserState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_FLS_laserState_Q(
                self.__handle, FLSSlot, byref(laserState)
            )
        )
        return bool(laserState.value)

    def get_SWT_type(self, SWT_slot: int):
        Switch_Type = ViInt32()
        Switch_Description = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_get_SWT_type(
                self.__handle, SWT_slot, byref(Switch_Type), Switch_Description
            )
        )
        return Switch_Type.value, Switch_Description.value.decode("ascii")

    def set_SWT_route(
        self, SWT_Slot: int, Input: Hp816xSwitchInput, Output: Hp816xSwitchOutput
    ):
        self.__check_error(
            self.__dll.hp816x_set_SWT_route(
                self.__handle, SWT_Slot, Input.value, Output.value
            )
        )

    def get_SWT_route(self, SWT_Slot: int, Input: Hp816xSwitchInput):
        Output = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_SWT_route(
                self.__handle, SWT_Slot, Input, byref(Output)
            )
        )
        return Hp816xSwitchOutput(Output.value)

    def get_SWT_routeTable(self, SWT_Slot: int):
        Route_Table = (ViChar * DEFAULT_MSG_BUFFER_SIZE)()
        self.__check_error(
            self.__dll.hp816x_get_SWT_routeTable(self.__handle, SWT_Slot, Route_Table)
        )
        return Route_Table.value.decode("ascii")

    def set_RLM_parameters(
        self,
        RLMSlot: int,
        internalTrigger: Hp816xRLMInternalTrigger,
        wavelength: float,
        averagingTime: float,
        laserSource: Hp816xSource,
        laserState: bool,
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_parameters(
                self.__handle,
                RLMSlot,
                internalTrigger.value,
                wavelength,
                averagingTime,
                laserSource.value,
                laserState,
            )
        )

    def get_RLM_parameters_Q(self, RLMSlot: int):
        internalTrigger = ViInt32()
        wavelength = ViReal64()
        averagingTime = ViReal64()
        laserSource = ViBoolean()
        laserState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_RLM_parameters_Q(
                self,
                RLMSlot,
                byref(internalTrigger),
                byref(wavelength),
                byref(averagingTime),
                byref(laserSource),
                byref(laserState),
            )
        )
        return (
            Hp816xRLMInternalTrigger(internalTrigger.value),
            wavelength.value,
            averagingTime.value,
            Hp816xSource(laserSource.value),
            bool(laserState.value),
        )

    def set_RLM_internalTrigger(
        self, RLMSlot: int, internalTrigger: Hp816xRLMInternalTrigger
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_internalTrigger(
                self.__handle, RLMSlot, internalTrigger.value
            )
        )

    def set_RLM_averagingTime(self, RLMSlot: int, averagingTime: float):
        self.__check_error(
            self.__dll.hp816x_set_RLM_averagingTime(
                self.__handle, RLMSlot, averagingTime
            )
        )

    def get_RLM_averagingTime_Q(self, RLMSlot: int):
        averagingTime = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_averagingTime_Q(
                self.__handle, RLMSlot, byref(averagingTime)
            )
        )
        return averagingTime.value

    def set_RLM_wavelength(self, RLMSlot: int, wavelength: float):
        self.__check_error(
            self.__dll.hp816x_set_RLM_wavelength(self.__handle, RLMSlot, wavelength)
        )

    def get_RLM_wavelength_Q(self, RLMSlot: int):
        minWavelength = ViReal64()
        maxWavelength = ViReal64()
        defaultWavelength = ViReal64()
        currentWavelength = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_wavelength_Q(
                self.__handle,
                RLMSlot,
                byref(minWavelength),
                byref(maxWavelength),
                byref(defaultWavelength),
                byref(currentWavelength),
            )
        )
        return (
            minWavelength.value,
            maxWavelength.value,
            defaultWavelength.value,
            currentWavelength.value,
        )

    def set_RLM_powerRange(
        self,
        RLMSlot: int,
        rangeMode: Hp816xPWMRangeMode,
        powerRange: float,
        powerRangeSecondSensor: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_powerRange(
                self.__handle,
                RLMSlot,
                rangeMode.value,
                powerRange,
                powerRangeSecondSensor,
            )
        )

    def get_RLM_powerRange_Q(self, RLMSlot: int):
        rangeMode = ViBoolean()
        powerRange = ViReal64()
        powerRangeSecondSensor = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_powerRange_Q(
                self.__handle,
                RLMSlot,
                byref(rangeMode),
                byref(powerRange),
                byref(powerRangeSecondSensor),
            )
        )
        return (
            Hp816xPWMRangeMode(rangeMode.value),
            powerRange.value,
            powerRangeSecondSensor.value,
        )

    def set_RLM_triggerConfiguration(
        self,
        RLMSlot: int,
        triggerIn: Hp816xRLMTriggerIn,
        triggerOut: Hp816xRLMTriggerOut,
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_triggerConfiguration(
                self.__handle, RLMSlot, triggerIn.value, triggerOut.value
            )
        )

    def start_RLM_internalTrigger(self, RLMSlot: int):
        self.__check_error(
            self.__dll.hp816x_start_RLM_internalTrigger(self.__handle, RLMSlot)
        )

    def RLM_readReturnLoss(self, RLMSlot: int):
        returnLoss = ViReal64()
        self.__check_error(
            self.__dll.hp816x_RLM_readReturnLoss(
                self.__handle, RLMSlot, byref(returnLoss)
            )
        )
        return returnLoss.value

    def RLM_fetchReturnLoss(self, RLMSlot: int):
        returnLoss = ViReal64()
        self.__check_error(
            self.__dll.hp816x_fetchReturnLoss(self.__handle, RLMSlot, byref(returnLoss))
        )
        return returnLoss.value

    def RLM_readValue(self, RLMSlot: int, monitorDiode: bool):
        powerValue = ViReal64()
        self.__check_error(
            self.__dll.hp816x_RLM_readValue(
                self.__handle, RLMSlot, monitorDiode, byref(powerValue)
            )
        )
        return powerValue.value

    def RLM_fetchValue(self, RLMSlot: int, monitorDiode: bool):
        powerValue = ViReal64()
        self.__check_error(
            self.__dll.hp816x_RLM_fetchValue(
                self.__handle, RLMSlot, monitorDiode, byref(powerValue)
            )
        )
        return powerValue.value

    def set_RLM_rlReference(self, RLMSlot: int, returnLossReference: float):
        self.__check_error(
            self.__dll.hp816x_set_RLM_flReference(
                self.__handle, RLMSlot, returnLossReference
            )
        )

    def get_RLM_flReference_Q(self, RLMSlot: int):
        returnLossReference = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_flReference_Q(
                self.__handle, RLMSlot, byref(returnLossReference)
            )
        )

    def set_RLM_FPDelta(self, RLMSlot: int, frontPanelDelta: float):
        self.__check_error(
            self.__dll.hp816x_set_RLM_FPDelta(self.__handle, RLMSlot, frontPanelDelta)
        )

    def get_RLM_FPDelta_Q(self, RLMSlot: int):
        frontPanelDelta = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_FPDelta_Q(
                self.__handle, RLMSlot, byref(frontPanelDelta)
            )
        )
        return frontPanelDelta.value

    def calibrate_RLM(self, RLMSlot: int, calibrate: Hp816xCAL):
        self.__check_error(
            self.__dll.hp816x_calibrate_RLM(self.__handle, RLMSlot, calibrate.value)
        )

    def RLM_zeroing(self, RLMSlot: int):
        zeroingResult = ViInt32()
        self.__check_error(
            self.__dll.hp816x_RLM_zeroing(self.__handle, RLMSlot, byref(zeroingResult))
        )
        return zeroingResult.value

    def RLM_zeroingAll(self):
        summaryofZeroingAll = ViInt32()
        self.__check_error(
            self.__dll.hp816x_RLM_zeroingAll(self.__handle, byref(summaryofZeroingAll))
        )
        return summaryofZeroingAll.value

    def enable_RLM_sweep(self, enableRLMLambdaSweep: bool):
        self.__check_error(
            self.__dll.hp816x_enable_RLM_sweep(self.__handle, enableRLMLambdaSweep)
        )

    def get_RLM_reflectanceValues_Q(self, RLMSlot: int):
        mref = ViReal64()
        pref = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_reflectanceValues_Q(
                self.__handle, RLMSlot, byref(mref), byref(pref)
            )
        )
        return mref.value, pref.value

    def get_RLM_terminationValues_Q(self, RLMSlot: int):
        mpara = ViReal64()
        ppara = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_terminationValues_Q(
                self.__handle, RLMSlot, byref(mpara), byref(ppara)
            )
        )
        return mpara.value, ppara.value

    def get_RLM_dutValues_Q(self, RLMSlot: int):
        mdut = ViReal64()
        pdut = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_dutValues_Q(
                self.__handle, RLMSlot, byref(mdut), byref(pdut)
            )
        )
        return mdut.value, pdut.value

    def calculate_RL(
        self,
        RLMSlot: int,
        mref: float,
        mpara: float,
        pref: float,
        ppara: float,
        mdut: float,
        pdut: float,
        frontPanelDelta: float,
        returnLoss: float,
    ):
        self.__check_error(
            self.__dll.hp816x_calculate_RL(
                self.__handle,
                RLMSlot,
                mref,
                mpara,
                pref,
                ppara,
                mdut,
                pdut,
                frontPanelDelta,
                returnLoss,
            )
        )

    def get_RLM_srcWavelength_Q(self, RLMSlot: int):
        wavelengthLowerSource = ViReal64()
        wavelengthUpperSource = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_srcWavelength_Q(
                self.__handle,
                RLMSlot,
                byref(wavelengthLowerSource),
                byref(wavelengthUpperSource),
            )
        )
        return wavelengthLowerSource.value, wavelengthUpperSource.value

    def set_RLM_laserSourceParameters(
        self, RLMSlot: int, laserSource: Hp816xSource, turnLaser: bool
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_laserSourceParameters(
                self.__handle, RLMSlot, laserSource, turnLaser
            )
        )

    def get_RLM_laserSourceParameters_Q(self, RLMSlot: int):
        laserSource = ViInt32()
        laserState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_RLM_laserSourceParameters_Q(
                self.__handle, RLMSlot, byref(laserSource), byref(laserState)
            )
        )
        return Hp816xSource(laserSource.value), bool(laserState.value)

    def set_RLM_modulationState(
        self, RLMSlot: int, laserSource: Hp816xSource, lowFrequencyControl: bool
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_modulationState(
                self.__handle, RLMSlot, laserSource.value, lowFrequencyControl
            )
        )

    def get_RLM_modulationState_Q(self, RLMSlot: int):
        laserSource = ViInt32()
        lowFrequencyControl = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_RLM_modulationState_Q(
                self.__handle, RLMSlot, byref(laserSource), lowFrequencyControl
            )
        )
        return Hp816xSource(laserSource.value), bool(lowFrequencyControl.value)

    def set_RLM_laserState(self, RLMSlot: int, laserState: bool):
        self.__check_error(
            self.__dll.hp816x_set_RLM_laserState(self.__handle, RLMSlot, laserState)
        )

    def get_RLM_laserState_Q(self, RLMSlot: int):
        laserState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_RLM_laserState_Q(
                self.__handle, RLMSlot, byref(laserState)
            )
        )
        return bool(laserState.value)

    def set_RLM_logging(self, RLMSlot: int, averagingTime: float, dataPoints: int):
        estimatedTimeout = ViInt32()
        self.__check_error(
            self.__dll.hp816x_set_RLM_logging(
                self.__handle,
                RLMSlot,
                averagingTime,
                dataPoints,
                byref(estimatedTimeout),
            )
        )
        return estimatedTimeout.value

    def get_RLM_loggingResults_Q(
        self,
        RLMSlot: int,
        waitforCompletion: bool,
        resultUnit: Hp816xPowerUnit,
        size: int,
    ):
        loggingStatus = ViBoolean()
        loggingResult = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_RLM_loggingResults_Q(
                self.__handle,
                RLMSlot,
                waitforCompletion,
                resultUnit.value,
                size,
                byref(loggingStatus),
                loggingResult,
            )
        )
        return bool(loggingStatus.value), list(loggingResult)

    def set_RLM_stability(
        self, RLMSlot: int, averagingTime: float, periodTime: float, totalTime: float
    ):
        estimatedResults = ViInt32()
        self.__check_error(
            self.__dll.hp816x_set_RLM_stability(
                self.__handle,
                RLMSlot,
                averagingTime,
                periodTime,
                totalTime,
                byref(estimatedResults),
            )
        )
        return estimatedResults.value

    def get_RLM_stabilityResults_Q(
        self,
        RLMSlot: int,
        waitforCompletion: bool,
        resultUnit: Hp816xPowerUnit,
        size: int,
    ):
        stabilityStatus = ViBoolean()
        stabilityResult = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_RLM_stabilityResults_Q(
                self.__handle,
                RLMSlot,
                waitforCompletion,
                resultUnit,
                byref(stabilityStatus),
                stabilityResult,
            )
        )
        return bool(stabilityStatus.value), list(stabilityResult)

    def set_RLM_minMax(
        self,
        RLMSlot: int,
        minmaxMode: Hp816xMinMaxMode,
        dataPoints: int,
        estimatedTime: int,
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLM_minMax(
                self.__handle, RLMSlot, minmaxMode.value, dataPoints, estimatedTime
            )
        )

    def get_RLM_minMaxResults_Q(self, RLMSlot: int):
        minimum = ViReal64()
        maximum = ViReal64()
        current = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_RLM_minMaxResults_Q(
                self.__handle, RLMSlot, byref(minimum), byref(maximum), byref(current)
            )
        )
        return minimum.value, maximum.value, current.value

    def RLM_functionStop(self, RLMSlot: int):
        self.__check_error(self.__dll.hp816x_RLM_functionStop(self.__handle, RLMSlot))

    def WaitForOPC(self, TLS_Slot: int, Wait_for_Operation_Complete: bool):
        self.__check_error(
            self.__dll.hp816x_WaitForOPC(
                self.__handle, TLS_Slot, Wait_for_Operation_Complete
            )
        )

    def set_TLS_parameters(
        self,
        TLSSlot: int,
        powerUnit: Hp816xPowerUnit,
        opticalOutput: Hp816xOpticalOutputMode,
        turnLaser: bool,
        power: float,
        attenuation: float,
        wavelength: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLS_parameters(
                self.__handle,
                TLSSlot,
                powerUnit.value,
                opticalOutput.value,
                turnLaser,
                power,
                attenuation,
                wavelength,
            )
        )

    def get_TLS_parameters_Q(self, TLSSlot: int):
        powerUnit = ViInt32()
        laserState = ViBoolean()
        opticalOutput = ViInt32()
        power = ViReal64()
        attenuation = ViReal64()
        wavelength = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_parameters_Q(
                self.__handle,
                TLSSlot,
                byref(powerUnit),
                byref(laserState),
                byref(opticalOutput),
                byref(power),
                byref(attenuation),
                byref(wavelength),
            )
        )
        return (
            Hp816xPowerUnit(powerUnit.value),
            bool(laserState.value),
            Hp816xOpticalOutputMode(opticalOutput.value),
            power.value,
            attenuation.value,
            wavelength.value,
        )

    def set_TLS_wavelength(
        self, TLSSlot: int, wavelengthSelection: Hp816xInputType, wavelength: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_RLS_wavelength(
                self.__handle, TLSSlot, wavelengthSelection.value, wavelength
            )
        )

    def get_TLS_wavelength_Q(self, TLSSlot: int):
        minimumWavelength = ViReal64()
        defaultWavelength = ViReal64()
        maximumWavelength = ViReal64()
        currentWavelength = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_wavelength_Q(
                self.__handle,
                TLSSlot,
                byref(minimumWavelength),
                byref(defaultWavelength),
                byref(maximumWavelength),
                byref(currentWavelength),
            )
        )
        return (
            minimumWavelength.value,
            defaultWavelength.value,
            maximumWavelength.value,
            currentWavelength.value,
        )

    def set_TLS_power(
        self,
        TLSSlot: int,
        unit: Hp816xPowerUnit,
        powerSelection: Hp816xInputType,
        manualPower: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_power(
                self.__handle, TLSSlot, unit.value, powerSelection.value, manualPower
            )
        )

    def get_RLS_power_Q(self, TLSSlot: int):
        powerUnit = ViInt32()
        minimumPower = ViReal64()
        defaultPower = ViReal64()
        maximumPower = ViReal64()
        currentPower = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_power_Q(
                self.__handle,
                TLSSlot,
                byref(powerUnit),
                byref(minimumPower),
                byref(defaultPower),
                byref(maximumPower),
                byref(currentPower),
            )
        )
        return (
            Hp816xPowerUnit(powerUnit.value),
            minimumPower.value,
            defaultPower.value,
            maximumPower.value,
            currentPower.value,
        )

    def set_TLS_opticalOutput(
        self, TLSSlot: int, setOpticalOutput: Hp816xOpticalOutputMode
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_opticalOutput(
                self.__handle, TLSSlot, setOpticalOutput.value
            )
        )

    def get_TLS_opticalOutput_Q(self, TLSSlot: int):
        opticalOutput = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_opticalOutput_Q(
                self.__handle, TLSSlot, byref(opticalOutput)
            )
        )
        return Hp816xOpticalOutputMode(opticalOutput.value)

    def get_TLS_powerMaxInRange_Q(
        self, TLSSlot: int, startofRange: float, endofRange: float
    ):
        maximumPower = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_powerMaxInRange_Q(
                self.__handle, TLSSlot, startofRange, endofRange, byref(maximumPower)
            )
        )

    def set_TLS_laserState(self, TLSSlot: int, laserState: bool):
        self.__check_error(
            self.__dll.hp816x_set_TLS_laserState(self.__handle, TLSSlot, laserState)
        )

    def get_TLS_laserState_Q(self, TLSSlot: int):
        laserState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_TLS_laserState_Q(
                self.__handle, TLSSlot, byref(laserState)
            )
        )
        return laserState.value

    def set_TLS_laserRiseTime(self, TLSSlot: int, laserRiseTime: float):
        self.__check_error(
            self.__dll.hp816x_set_TLS_laserRiseTime(
                self.__handle, TLSSlot, laserRiseTime
            )
        )

    def get_TLS_laserRiseTime(self, TLSSlot: int):
        laserRiseTime = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_laserRiseTime(
                self.__handle, TLSSlot, byref(laserRiseTime)
            )
        )
        return laserRiseTime.value

    def set_TLS_triggerConfiguration(
        self,
        TLSSlot: int,
        triggerIn: Hp816xTLSTriggerIn,
        triggerOut: Hp816xTLSTriggerOut,
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_triggerConfiguration(
                self.__handle, triggerIn.value, triggerOut.value
            )
        )

    def get_TLS_triggerConfiguration(self, TLSSlot: int):
        triggerIn = ViInt32()
        triggerOut = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_triggerConfiguration(
                self.__handle, byref(triggerIn), byref(triggerOut)
            )
        )
        return Hp816xTLSTriggerIn(triggerIn.value), Hp816xTLSTriggerOut(
            triggerOut.value
        )

    def set_TLS_attenuation(
        self,
        TLSSlot: int,
        powerMode: Hp816xPowerMode,
        darkenLaser: bool,
        attenuation: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_attenuation(
                self.__handle, TLSSlot, powerMode.value, darkenLaser, attenuation
            )
        )

    def get_TLS_attenuationSettings_Q(self, TLSSlot: int):
        powerMode = ViInt32()
        dark = ViBoolean()
        attenuation = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_attenuationSettings_Q(
                self.__handle,
                TLSSlot,
                byref(powerMode),
                byref(dark),
                byref(attenuation),
            )
        )
        return Hp816xPowerMode(powerMode.value), bool(dark.value), attenuation.value

    def set_TLS_dark(self, TLSSlot: int, darkenLaser: bool):
        self.__check_error(
            self.__dll.hp816x_set_TLS_dark(self.__handle, TLSSlot, darkenLaser)
        )

    def get_TLS_darkState_Q(self, TLSSlot: int):
        dark = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_TLS_darkState_Q(self.__handle, TLSSlot, byref(dark))
        )
        return bool(dark.value)

    def get_TLS_temperatures(self):
        Actual_Temperature = ViReal64()
        Temperature_Difference = ViReal64()
        Temperature_Laser_Zero = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_temperatures(
                self.__handle,
                byref(Actual_Temperature),
                byref(Temperature_Difference),
                byref(Temperature_Laser_Zero),
            )
        )
        return (
            Actual_Temperature.value,
            Temperature_Difference.value,
            Temperature_Laser_Zero.value,
        )

    def get_TLS_temeperaturesEx(self, TLSSlot: int):
        Actual_Temperature = ViReal64()
        Temperature_Difference = ViReal64()
        Temperature_Laser_Zero = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_temeperaturesEx(
                self.__handle,
                TLSSlot,
                byref(Actual_Temperature),
                byref(Temperature_Difference),
                byref(Temperature_Laser_Zero),
            )
        )
        return (
            Actual_Temperature.value,
            Temperature_Difference.value,
            Temperature_Laser_Zero.value,
        )

    def TLS_zeroing(self):
        self.__check_error(self.__dll.hp816x_TLS_zeroing(self.__handle))

    def TLS_zeroingAll(self):
        self.__check_error(self.__dll.hp816x_TLS_zeroingAll(self.__handle))

    def TLS_zeroingEx(self, TLSSlot: int):
        self.__check_error(self.__dll.hp816x_TLS_zeroingEx(self.__handle, TLSSlot))

    def set_TLS_autoCalibration(self, TLSSlot: int, Autocalibration: bool):
        self.__check_error(
            self.__dll.hp816x_set_TLS_autoCalibration(
                self.__handle, TLSSlot, Autocalibration
            )
        )

    def get_TLS_autoCalState(self, TLS_Slot: int):
        Auto_Calibration_State = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_TLS_autoCalState(
                self.__handle, TLS_Slot, byref(Auto_Calibration_State)
            )
        )
        return bool(Auto_Calibration_State.value)

    def get_TLS_accClass(self, TLS_Slot: int):
        Accurancy_Class = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_accClass(
                self.__handle, TLS_Slot, byref(Accurancy_Class)
            )
        )
        return Accurancy_Class.value

    def displayToLambdaZero(self, TLSSlot: int):
        self.__check_error(
            self.__dll.hp816x_displayToLambdaZero(self.__handle, TLSSlot)
        )

    def get_TLS_lambdaZero_Q(self, TLSSlot: int):
        lambda0 = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_lambdaZero_Q(
                self.__handle, TLSSlot, byref(lambda0)
            )
        )
        return lambda0.value

    def set_TLS_frequencyOffset(self, TLSSlot: int, offset: float):
        self.__check_error(
            self.__dll.hp816x_set_TLS_frequencyOffset(self.__handle, TLSSlot, offset)
        )

    def get_TLS_frequencyOffset_Q(self, TLSSlot: int):
        offset = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_frequencyOffset_Q(
                self.__handle, TLSSlot, byref(offset)
            )
        )
        return offset.value

    def set_TLS_sweep(
        self,
        TLSSLot: int,
        sweepMode: Hp816xSweepMode,
        repeatMode: Hp816xRepeatMode,
        cycles: int,
        dwellTime: float,
        startWavelength: float,
        stopWavelength: float,
        stepSize: float,
        sweepSpeed: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_sweep(
                self.__handle,
                TLSSLot,
                sweepMode.value,
                repeatMode.value,
                cycles,
                dwellTime,
                startWavelength,
                stopWavelength,
                stepSize,
                sweepSpeed,
            )
        )

    def TLS_sweepControl(self, TLSSlot: int, action: Hp816xSweepCommand):
        self.__check_error(
            self.__dll.hp816x_TLS_sweepControl(self.__handle, TLSSlot, action.value)
        )

    def get_TLS_sweepState_Q(self, TLSSlot: int):
        sweepState = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_sweepState_Q(
                self.__handle, TLSSlot, byref(sweepState)
            )
        )
        return Hp816xSweepCommand(sweepState.value)

    def TLS_sweepNextStep(self, TLSSlot: int):
        self.__check_error(self.__dll.hp816x_TLS_sweepNextStep(self.__handle, TLSSlot))

    def TLS_sweepPreviousStep(self, TLSSlot: int):
        self.__check_error(
            self.__dll.hp816x_TLS_sweepPreviousStep(self.__handle, TLSSlot)
        )

    def TLS_sweepWait(self, TLSSlot: int):
        self.__check_error(self.__dll.hp816x_TLS_sweepWait(self.__handle, TLSSlot))

    def set_TLS_modulation(
        self,
        TLSSlot: int,
        modulationSource: Hp816xModulationType,
        modulationOutput: Hp816xModulationOutput,
        modulation: bool,
        modulationFrequency: float,
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_modulation(
                self.__handle,
                TLSSlot,
                modulationSource.value,
                modulationOutput.value,
                modulation,
                modulationFrequency,
            )
        )

    def get_TLS_modulationSettings_Q(self, TLSSlot: int):
        modulationSource = ViInt32()
        modulationOutput = ViBoolean()
        modulationState = ViBoolean()
        frequency = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_modulationSettings_Q(
                self.__handle,
                TLSSlot,
                byref(modulationSource),
                byref(modulationOutput),
                byref(modulationState),
                byref(frequency),
            )
        )
        return (
            Hp816xModulationType(modulationSource.value),
            Hp816xModulationOutput(modulationOutput.value),
            bool(modulationState.value),
            frequency.value,
        )

    def TLS_configureBNC(self, TLSSlot: int, BNCOutput: Hp816xBNCOutput):
        self.__check_error(
            self.__dll.hp816x_TLS_configureBNC(self.__handle, TLSSlot, BNCOutput.value)
        )

    def get_TLS_BNC_config_Q(self, TLSSlot: int):
        BNCOutput = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_BNC_config_Q(
                self.__handle, TLSSlot, byref(BNCOutput)
            )
        )
        return Hp816xBNCOutput(BNCOutput.value)

    def set_TLS_ccLevel(self, TLS_Slot: int, CC_Level: float):
        self.__check_error(
            self.__dll.hp816x_set_TLS_ccLevel(self.__handle, TLS_Slot, CC_Level)
        )

    def get_TLS_ccLevel_Q(self, TLS_Slot: int):
        CC_Level = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_ccLevel_Q(
                self.__handle, TLS_Slot, byref(CC_Level)
            )
        )
        return CC_Level.value

    def set_TLS_SBSLevel(self, TLS_Slot: int, SBSLevel: float):
        self.__check_error(
            self.__dll.hp816x_set_TLS_SBSLevel(self.__handle, TLS_Slot, SBSLevel)
        )

    def get_TLS_SBSLevel_Q(self, TLS_Slot: int):
        SBSLevel = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_SBSLevel_Q(
                self.__handle, TLS_Slot, byref(SBSLevel)
            )
        )
        return SBSLevel.value

    def set_TLS_SBS_control(
        self, TLSSlot: int, mod_state: bool, modulationFrequency: float
    ):
        self.__check_error(
            self.__dll.hp816x_set_TLS_SBS_control(
                self.__handle, TLSSlot, mod_state, modulationFrequency
            )
        )

    def get_TLS_SBS_control_Q(self, TLSSlot: int):
        modState = ViBoolean()
        frequency = ViReal64()
        self.__check_error(
            self.__dll.hp816x_get_TLS_SBS_control_Q(
                self.__handle, TLSSlot, byref(modState), byref(frequency)
            )
        )
        return bool(modState.value), frequency.value

    def get_TLS_powerPoints_Q(self, TLSSlot: int):
        numberofPowerPoints = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_powerPoints_Q(
                self.__handle, TLSSlot, byref(numberofPowerPoints)
            )
        )
        return numberofPowerPoints.value

    def get_TLS_powerData_Q(self, TLSSlot: int, numberofDataItems: int, size: int):
        wavelengthData = (ViReal64 * size)()
        powerData = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_TLS_powerData_Q(
                self.__handle, TLSSlot, numberofDataItems, wavelengthData, powerData
            )
        )
        return list(wavelengthData), list(powerData)

    def set_TLS_lambdaLoggingState(self, lambdaLoggingState: bool):
        self.__check_error(
            self.__dll.hp816x_set_TLS_lambdaLoggingState(
                self.__handle, lambdaLoggingState
            )
        )

    def get_TLS_lambdaLoggingState_Q(self):
        lambdaLoggingState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_TLS_lambdaLoggingState_Q(
                self.__handle, byref(lambdaLoggingState)
            )
        )
        return bool(lambdaLoggingState.value)

    def set_TLS_lambdaLoggingStateEx(self, TLSSlot: int, lambdaLOggingState: bool):
        self.__check_error(
            self.__dll.hp816x_set_TLS_lambdaLoggingStateEx(
                self.__handle, TLSSlot, lambdaLOggingState
            )
        )

    def get_TLS_lambdaLoggingStateEx_Q(self, TLSSlot: int):
        lambdaLoggingState = ViBoolean()
        self.__check_error(
            self.__dll.hp816x_get_TLS_lambdaLoggingStateEx_Q(
                self.__handle, TLSSlot, byref(lambdaLoggingState)
            )
        )
        return bool(lambdaLoggingState.value)

    def get_TLS_wavelengthPoints_Q(self):
        numberofWavelengthValues = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_wavelengthPoints_Q(
                self.__handle, byref(numberofWavelengthValues)
            )
        )
        return numberofWavelengthValues.value

    def get_TLS_wavelengthPointsEx_Q(self, TLSSlot: int):
        numberofWavelengthValues = ViInt32()
        self.__check_error(
            self.__dll.hp816x_get_TLS_wavelengthPointsEx_Q(
                self.__handle, TLSSlot, byref(numberofWavelengthValues)
            )
        )
        return numberofWavelengthValues.value

    def get_TLS_wvelengthData_Q(self, arraySize: int, size: int):
        wavelengthData = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_TLS_wvelengthData_Q(
                self.__handle, arraySize, wavelengthData
            )
        )
        return list(wavelengthData)

    def get_TLS_wvelengthDataEx_Q(self, TLSSlot: int, arraySize: int, size: int):
        wavelengthData = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_get_TLS_wvelengthDataEx_Q(
                self.__handle, TLSSlot, arraySize, wavelengthData
            )
        )
        return list(wavelengthData)

    def set_LambdaScan_wavelength(self, powerMeterWavelength: float):
        self.__check_error(
            self.__dll.hp816x_set_LambdaScan_wavelength(
                self.__handle, powerMeterWavelength
            )
        )

    def enableHighSweepSpeed(self, fastSweepSpeed: bool):
        self.__check_error(
            self.__dll.hp816x_enableHighSweepSpeed(self.__handle, fastSweepSpeed)
        )

    def prepareLambdaScan(
        self,
        powerUnit: Hp816xPowerUnit,
        power: float,
        opticalOutput: Hp816xOpticalOutputMode,
        numberofScans: Hp816xNumberOfScans,
        PWMChannels: int,
        startWavelength: float,
        stopWavelength: float,
        stepSize: float,
    ):
        numberofDatapoints = ViUInt32()
        numberofChannels = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_prepareLambdaScan(
                self.__handle,
                powerUnit.value,
                power,
                opticalOutput.value,
                numberofScans.value,
                PWMChannels,
                startWavelength,
                stopWavelength,
                stepSize,
                byref(numberofDatapoints),
                byref(numberofChannels),
            )
        )
        return numberofDatapoints.value, numberofChannels.value

    def getLambdaScanParameters_Q(self):
        startWavelength = ViReal64()
        stopWavelength = ViReal64()
        averagingTime = ViReal64()
        sweepSpeed = ViReal64()
        self.__check_error(
            self.__dll.hp816x_getLambdaScanParameters_Q(
                self.__handle,
                byref(startWavelength),
                byref(stopWavelength),
                byref(averagingTime),
                byref(sweepSpeed),
            )
        )
        return (
            startWavelength.value,
            stopWavelength.value,
            averagingTime.value,
            sweepSpeed.value,
        )

    def executeLambdaScan(self, size: int):
        wavelengthArray = (ViReal64 * size)()
        powerArray1 = (ViReal64 * size)()
        powerArray2 = (ViReal64 * size)()
        powerArray3 = (ViReal64 * size)()
        powerArray4 = (ViReal64 * size)()
        powerArray5 = (ViReal64 * size)()
        powerArray6 = (ViReal64 * size)()
        powerArray7 = (ViReal64 * size)()
        powerArray8 = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_executeLambdaScan(
                self.__handle,
                size,
                wavelengthArray,
                powerArray1,
                powerArray2,
                powerArray3,
                powerArray4,
                powerArray5,
                powerArray6,
                powerArray7,
                powerArray8,
            )
        )
        return (
            list(wavelengthArray),
            list(powerArray1),
            list(powerArray2),
            list(powerArray3),
            list(powerArray4),
            list(powerArray5),
            list(powerArray6),
            list(powerArray7),
            list(powerArray8),
        )

    def returnEquidistantData(self, equallySpacedDatapoints: bool):
        self.__check_error(
            self.__dll.hp816x_returnEquidistantData(
                self.__handle, equallySpacedDatapoints
            )
        )

    def registerMainframe(self):
        self.__check_error(self.__dll.hp816x_registerMainframe(self.__handle))

    def unregisterMainframe(self):
        self.__check_error(self.__dll.hp816x_unregisterMainframe(self.__handle))

    def setSweepSpeed(self, Sweep_Speed: Hp816xSweepSpeed):
        self.__check_error(
            self.__dll.hp816x_setSweepSpeed(self.__handle, Sweep_Speed.value)
        )

    def prepareMfLambdaScan(
        self,
        powerUnit: Hp816xPowerUnit,
        power: float,
        opticalOutput: Hp816xOpticalOutputMode,
        numberofScans: Hp816xNumberOfScans,
        PWMChannels: int,
        startWavelength: float,
        stopWavelength: float,
        stepSize: float,
    ):
        numberofDatapoints = ViUInt32()
        numberofChannels = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_prepareMfLambdaScan(
                self.__handle,
                powerUnit.value,
                power,
                opticalOutput.value,
                numberofScans.value,
                PWMChannels,
                startWavelength,
                stopWavelength,
                stepSize,
                byref(numberofDatapoints),
                byref(numberofChannels),
            )
        )
        return numberofDatapoints.value, numberofChannels.value

    def getMFLambdaScanParameters_Q(self):
        startWavelength = ViReal64()
        stopWavelength = ViReal64()
        averagingTime = ViReal64()
        sweepSpeed = ViReal64()
        self.__check_error(
            self.__dll.hp816x_getMFLambdaScanParameters_Q(
                self.__handle,
                byref(startWavelength),
                byref(stopWavelength),
                byref(averagingTime),
                byref(sweepSpeed),
            )
        )
        return (
            startWavelength.value,
            stopWavelength.value,
            averagingTime.value,
            sweepSpeed.value,
        )

    def executeMfLambdaScan(self, size: int):
        wavelengthArray = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_executeMfLambdaScan(self.__handle, wavelengthArray)
        )
        return list(wavelengthArray)

    def getLambdaScanResult(
        self, PWMChannel: int, cliptoLimit: bool, clippingLimit: float, size: int
    ):
        powerArray = (ViReal64 * size)()
        lambdaArray = (ViReal64 * size)()
        self.__check_error(
            self.__dll.hp816x_getLambdaScanResult(
                self.__handle,
                PWMChannel,
                cliptoLimit,
                clippingLimit,
                powerArray,
                lambdaArray,
            )
        )
        return list(powerArray), list(lambdaArray)

    def getNoOfRegPWMChannels_Q(self):
        numberofPWMChannels = ViUInt32()
        self.__check_error(
            self.__dll.hp816x_getNoOfRegPWMChannels_Q(
                self.__handle, byref(numberofPWMChannels)
            )
        )
        return numberofPWMChannels.value

    def getChannelLocation(self, PWMChannel: int):
        mainframeNumber = ViInt32()
        slotNumber = ViInt32()
        channelNumber = ViInt32()
        self.__check_error(
            self.__dll.hp816x_getChannelLocation(
                self.__handle,
                PWMChannel,
                byref(mainframeNumber),
                byref(slotNumber),
                byref(channelNumber),
            )
        )
        return mainframeNumber.value, slotNumber.value, channelNumber.value

    def excludeChannel(self, PWMChannel: int):
        self.__check_error(self.__dll.hp816x_excludeChannel(self.__handle, PWMChannel))

    def setInitialRangeParams(
        self,
        PWMChannel: int,
        resettoDefault: bool,
        initialRange: float,
        rangeDecrement: float,
    ):
        self.__check_error(
            self.__dll.hp816x_setInitialRangeParams(
                self.__handle, PWMChannel, resettoDefault, initialRange, rangeDecrement
            )
        )

    def setScanAttenuation(self, Scan_Attenuation: float):
        self.__check_error(
            self.__dll.hp816x_setScanAttenuation(self.__handle, Scan_Attenuation)
        )


if __name__ == "__main__":
    print(Hp816xDriver.listVisa_Q(0, False))
    print(Hp816xDriver.getInstrumentId_Q("GPIB0::20::INSTR"))

    print("Connecting to laser...")
    laser = Hp816xDriver(Hp816xModel.HP8164AB, "GPIB0::20::INSTR", True, True)
    print("Laser connected!")

    laser.forceTransaction(True)
    laser.forceTransaction(False)

    print(laser.cmdString_Q("*IDN?", 512))

    # print(laser.revision_Q())
    # print(laser.self_test())
