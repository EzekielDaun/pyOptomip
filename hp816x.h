/*****************************************************************************/
/*  hp816x.h                                                                 */
/*  Copyright (C) 1998 Hewlett-Packard Company                               */
/*---------------------------------------------------------------------------*/
/*  Driver for hp816x, $instrument desc$                                     */
/*  Driver Version: V 2.90                                                  */
/*****************************************************************************/

#ifndef hp816x_INCLUDE 
#define hp816x_INCLUDE
#include "vpptype.h"

/* Used for "C" externs in C++ */
#if defined(__cplusplus) || defined(__cplusplus__)
extern "C" {
#endif

/* BASIC START*/

/*****************************************************************************/
/*  STANDARD SECTION                                                         */
/*  Constants and function prototypes for HP standard functions.             */
/*****************************************************************************/

/*---------------------------------------------------------------------------*/
/* DEVELOPER: Remove what you don't need from this standard function         */
/*              section, with the exception that VPP required functions      */
/*              may not be removed.                                          */
/*            Don't add to this section - add to the instrument specific     */
/*              section below.                                               */
/*            Don't change section - if you need to "change" the prototype   */
/*              of a standard function, delete it from this section and      */
/*              add a new function (named differently) in the instrument     */
/*              specific section.                                            */
/*---------------------------------------------------------------------------*/

        /***************************************************/
        /*  Standard constant error conditions returned    */
        /*  by driver functions.                           */
        /*    HP Common Error numbers start at BFFC0D00    */
        /*    The parameter errors extend the number of    */
        /*      errors over the eight defined in VPP 3.4   */
        /***************************************************/

/*Additional Parameter Errors */

#define VI_ERROR_PARAMETER9							 (_VI_ERROR+0x3FFC0009L) /* 0xBFFC0009 */
#define VI_ERROR_PARAMETER10						 (_VI_ERROR+0x3FFC000AL) /* 0xBFFC000A */
#define VI_ERROR_PARAMETER11						 (_VI_ERROR+0x3FFC000BL) /* 0xBFFC000B */



#define hp816x_INSTR_ERROR_NULL_PTR      (_VI_ERROR+0x3FFC0D02L) /* 0xBFFC0D02 */
#define hp816x_INSTR_ERROR_RESET_FAILED  (_VI_ERROR+0x3FFC0D03L) /* 0xBFFC0D03 */
#define hp816x_INSTR_ERROR_UNEXPECTED    (_VI_ERROR+0x3FFC0D04L) /* 0xBFFC0D04 */
#define hp816x_INSTR_ERROR_INV_SESSION   (_VI_ERROR+0x3FFC0D05L) /* 0xBFFC0D05 */
#define hp816x_INSTR_ERROR_LOOKUP        (_VI_ERROR+0x3FFC0D06L) /* 0xBFFC0D06 */
#define hp816x_INSTR_ERROR_DETECTED      (_VI_ERROR+0x3FFC0D07L) /* 0xBFFC0D07 */
#define hp816x_INSTR_NO_LAST_COMMA       (_VI_ERROR+0x3FFC0D08L) /* 0xBFFC0D08 */ 
#define hp816x_INSTR_NO_VALID_SLOT       (_VI_ERROR+0x3FFC0D09L) /* 0xBFFC0D09 */ 
#define hp816x_INSTR_NO_VALID_CHAN       (_VI_ERROR+0x3FFC0D0AL) /* 0xBFFC0D0A */ 
#define hp816x_DRIVER_LOCKED             (_VI_ERROR+0x3FFC0D0BL) /* 0xBFFC0D0B */ 
#define hp816x_MEM_ALLOC                 (_VI_ERROR+0x3FFC0D0CL) /* 0xBFFC0D0C */ 
#define hp816x_INSTR_NO_VALID_SRC        (_VI_ERROR+0x3FFC0D0DL) /* 0xBFFC0D0D */ 
#define hp816x_INSTR_LOGGING_ACTIVE      (_VI_ERROR+0x3FFC0D0EL) /* 0xBFFC0D0E */ 
#define hp816x_INSTR_STAB_LOGG_ACTIVE    (_VI_ERROR+0x3FFC0D0FL) /* 0xBFFC0D0F */ 
#define hp816x_INSTR_MINMAX_ACTIVE       (_VI_ERROR+0x3FFC0D10L) /* 0xBFFC0D10 */ 
#define hp816x_NOVALID_SRCSEL            (_VI_ERROR+0x3FFC0D11L) /* 0xBFFC0D11 */ 
#define hp816x_INVALID_FUNC              (_VI_ERROR+0x3FFC0D12L) /* 0xBFFC0D12 */ 
#define hp816x_INVALID_IDN               (_VI_ERROR+0x3FFC0D13L) /* 0xBFFC0D13 */ 
#define hp816x_MODULE_NOT_PLUGGED        (_VI_ERROR+0x3FFC0D14L) /* 0xBFFC0D14 */ 
#define hp816x_NO_DUAL_SOURCE            (_VI_ERROR+0x3FFC0D15L) /* 0xBFFC0D15 */ 
#define hp816x_NO_VALID_MODULATION	     (_VI_ERROR+0x3FFC0D16L) /* 0xBFFC0D16 */
#define hp816x_INVALID_PASSWORD		       (_VI_ERROR+0x3FFC0D17L) /* 0xBFFC0D17 */  	
#define hp816x_MOD_SOURCE_NOT_SUPPORTED	 (_VI_ERROR+0x3FFC0D18L) /* 0xBFFC0D18 */ 
#define hp816x_OPT_OUTPUT_NOT_SUPPORTED	 (_VI_ERROR+0x3FFC0D19L) /* 0xBFFC0D19 */ 
#define hp816x_NO_POWERMETER		         (_VI_ERROR+0x3FFC0D1AL) /* 0xBFFC0D1A */ 
#define hp816x_NO_LSPREPARE_CALL      	 (_VI_ERROR+0x3FFC0D1BL) /* 0xBFFC0D1B */
#define hp816x_PARAMETER_MISMATCH        (_VI_ERROR+0x3FFC0D1CL) /* 0xBFFC0D1C */
#define hp816x_SAME_SENSOR               (_VI_ERROR+0x3FFC0D1DL) /* 0xBFFC0D1D */ 
#define hp816x_NO_BUILTIN_SOURCE         (_VI_ERROR+0x3FFC0D1EL) /* 0xBFFC0D1E */ 
#define hp816x_ARRAYSIZE_TOSMALL         (_VI_ERROR+0x3FFC0D1FL) /* 0xBFFC0D1F */ 
#define hp816x_ZERODIVIDE                (_VI_ERROR+0x3FFC0D20L) /* 0xBFFC0D20 */ 
#define hp816x_NO_FRAME_REGISTERED       (_VI_ERROR+0x3FFC0D21L) /* 0xBFFC0D21 */  
#define hp816x_NO_BL_TLS                 (_VI_ERROR+0x3FFC0D22L) /* 0xBFFC0D22 */ 
#define hp816x_NO_DATA_ALLOC             (_VI_ERROR+0x3FFC0D23L) /* 0xBFFC0D23 */  
#define hp816x_NO_TRIGGERS               (_VI_ERROR+0x3FFC0D24L) /* 0xBFFC0D24 */   
#define hp816x_INVALID_VI                (_VI_ERROR+0x3FFC0D25L) /* 0xBFFC0D25 */   
#define hp816x_FILEOPEN_ERROR            (_VI_ERROR+0x3FFC0D26L) /* 0xBFFC0D26 */   
#define hp816x_TOO_FEW_TRIGGERS          (_VI_ERROR+0x3FFC0D27L) /* 0xBFFC0D27 */   
#define hp816x_MODVERSION_ERROR          (_VI_ERROR+0x3FFC0D28L) /* 0xBFFC0D28 */    
#define hp816x_LLOG_NUMBER               (_VI_ERROR+0x3FFC0D29L) /* 0xBFFC0D29 */    
#define hp816x_CHAN_EXCLUDED             (_VI_ERROR+0x3FFC0D2AL) /* 0xBFFC0D2A */    
#define hp816x_NOT_RELIABLE              (_VI_ERROR+0x3FFC0D2BL) /* 0xBFFC0D2B */ 
#define hp816x_INTERNAL_ERROR            (_VI_ERROR+0x3FFC0D2CL) /* 0xBFFC0D2C */  
#define hp816x_SOFT_LOCKED               (_VI_ERROR+0x3FFC0D2DL) /* 0xBFFC0D2D */  
#define hp816x_ERR_OFFSET_TBL            (_VI_ERROR+0x3FFC0D2EL) /* 0xBFFC0D2E */  
#define hp816x_NO_BUILTIN_PM             (_VI_ERROR+0x3FFC0D2FL) /* 0xBFFC0D2F */
#define hp816x_INSTR_ERROR_PARAMETER9    (_VI_ERROR+0x3FFC0D30L) /* 0xBFFC0D30 */
#define hp816x_INSTR_ERROR_PARAMETER10   (_VI_ERROR+0x3FFC0D31L) /* 0xBFFC0D31 */
#define hp816x_INSTR_ERROR_PARAMETER11   (_VI_ERROR+0x3FFC0D32L) /* 0xBFFC0D32 */
#define hp816x_INSTR_ERROR_PARAMETER12   (_VI_ERROR+0x3FFC0D33L) /* 0xBFFC0D33 */
#define hp816x_INSTR_ERROR_PARAMETER13   (_VI_ERROR+0x3FFC0D34L) /* 0xBFFC0D34 */
#define hp816x_INSTR_ERROR_PARAMETER14   (_VI_ERROR+0x3FFC0D35L) /* 0xBFFC0D35 */
#define hp816x_INSTR_ERROR_PARAMETER15   (_VI_ERROR+0x3FFC0D36L) /* 0xBFFC0D36 */
#define hp816x_INSTR_ERROR_PARAMETER16   (_VI_ERROR+0x3FFC0D37L) /* 0xBFFC0D37 */
#define hp816x_INSTR_ERROR_PARAMETER17   (_VI_ERROR+0x3FFC0D38L) /* 0xBFFC0D38 */
#define hp816x_INSTR_ERROR_PARAMETER18   (_VI_ERROR+0x3FFC0D39L) /* 0xBFFC0D39 */
#define hp816x_WRONG_FCT                 (_VI_ERROR+0x3FFC0D3AL) /* 0xBFFC0D3A */ 
#define hp816x_UNKNOWN_MODULE            (_VI_ERROR+0x3FFC0D3BL) /* 0xBFFC0D3B */ 



        /***************************************************/
        /*  Constants used by system status functions      */
        /*    These defines are bit numbers which define   */
        /*    the operation and questionable registers.    */
        /*    They are instrument specific.                */
        /***************************************************/

/*---------------------------------------------------------------------------*/
/* DEVELOPER: Modify these bit values to reflect the meanings of the         */
/*            operation and questionable status registers for your           */
/*              instrument.                                                  */
/*---------------------------------------------------------------------------*/

#define hp816x_QUES_BIT0          1
#define hp816x_QUES_BIT1          2
#define hp816x_QUES_BIT2          4
#define hp816x_QUES_BIT3          8
#define hp816x_QUES_BIT4         16
#define hp816x_QUES_BIT5         32
#define hp816x_QUES_BIT6         64
#define hp816x_QUES_BIT7        128
#define hp816x_QUES_BIT8        256
#define hp816x_QUES_BIT9        512
#define hp816x_QUES_BIT10      1024
#define hp816x_QUES_BIT11      2048
#define hp816x_QUES_BIT12      4096
#define hp816x_QUES_BIT13      8192
#define hp816x_QUES_BIT14     16384
#define hp816x_QUES_BIT15     32768

#define hp816x_OPER_BIT0          1
#define hp816x_OPER_BIT1          2
#define hp816x_OPER_BIT2          4
#define hp816x_OPER_BIT3          8
#define hp816x_OPER_BIT4         16
#define hp816x_OPER_BIT5         32
#define hp816x_OPER_BIT6         64
#define hp816x_OPER_BIT7        128
#define hp816x_OPER_BIT8        256
#define hp816x_OPER_BIT9        512
#define hp816x_OPER_BIT10      1024
#define hp816x_OPER_BIT11      2048
#define hp816x_OPER_BIT12      4096
#define hp816x_OPER_BIT13      8192
#define hp816x_OPER_BIT14     16384
#define hp816x_OPER_BIT15     32768

        /***************************************************/
        /*  Constants used by function hp816x_timeOut      */
        /***************************************************/

#define hp816x_TIMEOUT_MAX         2147483647L
#define hp816x_TIMEOUT_MIN         0L

#define hp816x_CMDINT16ARR_Q_MIN   1L
#define hp816x_CMDINT16ARR_Q_MAX   2147483647L

#define hp816x_CMDINT32ARR_Q_MIN   1L
#define hp816x_CMDINT32ARR_Q_MAX   2147483647L

#define hp816x_CMDREAL64ARR_Q_MIN  1L
#define hp816x_CMDREAL64ARR_Q_MAX  2147483647L


        /***************************************************/
        /*  Required plug and play functions from VPP-3.1  */
        /***************************************************/

ViStatus _VI_FUNC hp816x_init  (ViRsrc     resourceName,
                         ViBoolean  IDQuery,
                         ViBoolean  resetDevice,
                         ViPSession IHandle);

ViStatus _VI_FUNC hp816x_getHandle (ViSession instrumentHandle,          
                                   ViPSession IHandle);

ViStatus _VI_FUNC hp816x_close (ViSession  IHandle);

ViStatus _VI_FUNC hp816x_reset (ViSession  IHandle);

ViStatus _VI_FUNC hp816x_self_test (ViSession iHandle,
                                    ViPInt16  selfTestResult,
                                    ViPString selfTestMessage);

ViStatus _VI_FUNC hp816x_mainframeSelftest (ViSession  IHandle,
                         ViPInt16   selfTestResult,
                         ViPString  selfTestMessage);

ViStatus _VI_FUNC hp816x_error_query (ViSession  IHandle,
                         ViPInt32   errorCode,
                         ViPString  errorMessage);

ViStatus _VI_FUNC hp816x_error_message (ViSession  IHandle,
                         ViStatus   statusCode,
                         ViPString  message);

ViStatus _VI_FUNC hp816x_revision_query (  ViSession iHandle,
                                    ViPString instrumentDriverRevision,
                                    ViPString firmwareRevision);

ViStatus _VI_FUNC hp816x_revision_Q (ViSession  IHandle,
                         ViPString  instrumentDriverRevision,
                         ViPString  firmwareRevision);


        /***************************************************/
        /*  HP standard utility functions                  */
        /***************************************************/

ViStatus _VI_FUNC hp816x_timeOut (ViSession  IHandle,
                         ViInt32    setTimeOut);

ViStatus _VI_FUNC hp816x_timeOut_Q (ViSession  IHandle,
                         ViPInt32   timeOut);

ViStatus _VI_FUNC hp816x_errorQueryDetect (ViSession  IHandle,
                         ViBoolean  setErrorQueryDetect);

ViStatus _VI_FUNC hp816x_errorQueryDetect_Q (ViSession  IHandle,
                         ViPBoolean errorQueryDetect);

ViStatus _VI_FUNC hp816x_dcl (ViSession  IHandle);

ViStatus _VI_FUNC hp816x_opc_Q (ViSession  IHandle,
                         ViPBoolean instrumentReady);

ViStatus _VI_FUNC hp816x_WattToDBm (ViSession IHandle, ViReal64 watt,
                                   ViReal64 *dBm);
    

ViStatus _VI_FUNC hp816x_dbmToWatt (ViSession IHandle, ViReal64 dBm,
                                   ViReal64 *watt);

ViStatus _VI_FUNC  hp816x_setDate (ViSession IHandle, ViInt32 year, ViInt32 month,
                                 ViInt32 day);                                   

ViStatus  _VI_FUNC hp816x_getDate (ViSession IHandle, ViInt32 *year,  
                                   ViInt32 *month, ViInt32 *day);      
    
ViStatus _VI_FUNC hp816x_setTime (ViSession IHandle, ViInt32 hour, ViInt32 minute,
                                 ViInt32 second);

ViStatus _VI_FUNC hp816x_getTime (ViSession IHandle, ViInt32 *hour,
                                 ViInt32 *minute, ViInt32 *second);
    

ViStatus _VI_FUNC hp816x_SystemError (ViSession IHandle, ViInt32 *errorNumber,
                                     ViPString errorMessage);
    

ViStatus _VI_FUNC hp816x_cls (ViSession IHandle);
    
    

        /***************************************************/
        /*  HP standard status functions                   */
        /***************************************************/

ViStatus _VI_FUNC hp816x_readStatusByte_Q (ViSession  IHandle,
                         ViPInt16   statusByte);

ViStatus _VI_FUNC hp816x_operEvent_Q (ViSession  IHandle,
                         ViPInt32   operationEventRegister);

ViStatus _VI_FUNC hp816x_operCond_Q (ViSession  IHandle,
                         ViPInt32   operationConditionRegister );

ViStatus _VI_FUNC hp816x_quesEvent_Q (ViSession  IHandle,
                         ViPInt32   questionableEventRegister );

ViStatus _VI_FUNC hp816x_quesCond_Q (ViSession  IHandle,
                         ViPInt32   questionableConditionRegister );


        /***************************************************/
        /*  HP standard command passthrough functions      */
        /***************************************************/

ViStatus _VI_FUNC hp816x_cmd (ViSession  IHandle,
                         ViString   sendStringCommand);

ViStatus _VI_FUNC hp816x_cmdString_Q (ViSession  IHandle,
                         ViString   queryStringCommand, 
                        ViInt32    stringSize,
                         ViChar   stringResult[]);
  
ViStatus _VI_FUNC hp816x_cmdInt (ViSession  IHandle,
                         ViString   sendIntegerCommand,
                         ViInt32    sendInteger);

ViStatus _VI_FUNC hp816x_cmdInt16_Q (ViSession  IHandle,
                         ViString   queryI16Command,
                         ViPInt16   i16Result);

ViStatus _VI_FUNC hp816x_cmdInt32_Q (ViSession  IHandle,
                         ViString   queryI32Command,
                         ViPInt32   i32Result);

ViStatus _VI_FUNC hp816x_cmdInt16Arr_Q (ViSession  IHandle,
                         ViString   queryI16ArrayCommand,
                         ViInt32    i16ArraySize,
                         ViPInt16   i16ArrayResult,
                         ViPInt32   i16ArrayCount);

ViStatus _VI_FUNC hp816x_cmdInt32Arr_Q (ViSession  IHandle,
                         ViString   queryI32ArrayCommand,
                         ViInt32    i32ArraySize,
                         ViPInt32    i32ArrayResult,
                         ViPInt32   i32ArrayCount);
    
ViStatus _VI_FUNC hp816x_cmdReal   (ViSession  IHandle,
                         ViString   sendRealCommand,
                         ViReal64   sendReal);

ViStatus _VI_FUNC hp816x_cmdReal64_Q  (ViSession  IHandle,
                         ViString   queryRealCommand,
                         ViPReal64  realResult);

ViStatus _VI_FUNC hp816x_cmdReal64Arr_Q (ViSession  IHandle,
                         ViString   realArrayCommand,
                         ViInt32    realArraySize,
                         ViPReal64  realArrayResult,
                         ViPInt32   realArrayCount);

    

    

    

    

    

/* End of HP standard declarations */
/*---------------------------------------------------------------------------*/


/*****************************************************************************/
/*  INSTRUMENT SPECIFIC SECTION                                              */
/*  Constants and function prototypes for instrument specific functions.     */
/*****************************************************************************/

/*---------------------------------------------------------------------------*/
/* DEVELOPER: Add constants and function prototypes here.                    */
/*            As a metter of style, add the constant #define's first,        */
/*              followed by function prototypes.                             */
/*            Remember that function prototypes must be consistent with      */
/*              the driver's function panel prototypes.                      */
/*---------------------------------------------------------------------------*/

        /***************************************************/
        /*  Instrument specific constants                  */
        /***************************************************/


/*Maximum of supported instruments */
#define hp816x_MAX_INSTR          256

/*bus type definitions*/
#define hp816x_INTF_GPIB            0 
#define hp816x_INTF_ASRL            1 
#define hp816x_INTF_ALL             2 

/*list visa adresses */
#define hp816x_SEL_816X             1 
#define hp816x_SEL_ALL              0 



/* channel and slot definitions*/
#define hp816x_SLOT_0               0 
#define hp816x_SLOT_1               1 
#define hp816x_SLOT_2               2 
#define hp816x_SLOT_3               3 
#define hp816x_SLOT_4               4 
#define hp816x_SLOT_5               5 
#define hp816x_SLOT_6               6
#define hp816x_SLOT_7               7
#define hp816x_SLOT_8               8
#define hp816x_SLOT_9               9
#define hp816x_SLOT_10              10
#define hp816x_SLOT_11              11
#define hp816x_SLOT_12              12
#define hp816x_SLOT_13              13
#define hp816x_SLOT_14              14
#define hp816x_SLOT_15              15
#define hp816x_SLOT_16              16
#define hp816x_SLOT_17              17

#define hp816x_CHAN_1								0
#define hp816x_CHAN_2								1

        /***_************************************************/
        /*  Constants for retrieving the type of modul plugged */
        /***************************************************/


#define hp816x_UNDEF               0L
#define hp816x_SINGLE_SENSOR       1L
#define hp816x_DUAL_SENSOR         2L
#define hp816x_FIXED_SINGLE_SOURCE 3L       
#define hp816x_FIXED_DUAL_SOURCE   4L
#define hp816x_TUNABLE_SOURCE      5L  
#define hp816x_RETURN_LOSS         6L 
#define hp816x_ATTENUATOR          7L
#define hp816x_SWITCH              8L

        /***************************************************/
        /*  Frame specific  constants                       */
        /***************************************************/

#define hp816x_PWM_SLOT_MIN 1
#define hp816x_MAX_SLOTS 18

#define hp816x_NODE_A  0
#define hp816x_NODE_B  1


#define hp816x_TRIG_DISABLED     0
#define hp816x_TRIG_DEFAULT      1
#define hp816x_TRIG_PASSTHROUGH  2
#define hp816x_TRIG_LOOPBACK     3
#define hp816x_TRIG_CUSTOM       4 

        /***************************************************/
        /*  Attenuator  specific  constants                */
        /***************************************************/

#define hp816x_SELECT_MIN 0
#define hp816x_SELECT_MAX 1
#define hp816x_SELECT_DEF 2
#define hp816x_SELECT_MANUAL 3


        /***************************************************/
        /*  Powermeter  specific  constants                   */
        /***************************************************/
/*available channels*/
#define hp816x_PWM_CHAN_MIN 0
#define hp816x_PWM_CHAN_MAX 1 

/*power range also used for return loss*/
#define hp816x_PWM_RANGE_AUTO  1
#define hp816x_PWM_RANGE_MANUAL 0

/*reference used internal or other modul*/
#define hp816x_PWM_TO_REF      0
#define hp816x_PWM_TO_MOD      1


#define hp816x_PWM_REF_ABSOLUTE  0
#define hp816x_PWM_REF_RELATIV   1

/*trigger modes*/
#define hp816x_PWM_IMMEDIATE  0
#define hp816x_PWM_CONTINUOUS  1

/*trigger force*/
#define hp816x_PWM_WAIT_TRIG   0
#define hp816x_PWM_FORCE_TRIG  1



/*wave limits in nm*/
#define hp816x_PWM_WAVE_MIN  300.0E-9
#define hp816x_PWM_WAVE_MAX  1800.0E-9

/*averaging time limits in s*/
#define hp816x_PWM_ATIME_MIN  25.0E-6
#define hp816x_PWM_ATIME_MAX  900.0

/*correction limits in dbm*/
#define hp816x_PWM_CORR_MIN   -180.0
#define hp816x_PWM_CORR_MAX   200.0

/*reference limits in db, dBm*/
#define hp816x_PWM_REV_DB_MIN   -180.0
#define hp816x_PWM_REV_DB_MAX   200.0

#define hp816x_PWM_REV_WATT_MIN   1.0e-18
#define hp816x_PWM_REV_WATT_MAX		1.0e18

/*power range in dBm*/
#define hp816x_PWM_RANGE_MIN  -110.0
#define hp816x_PWM_RANGE_MAX  30.0

/*power range mode*/
#define hp816x_PWM_RANGE_AUTO_OFF  0
#define hp816x_PWM_RANGE_AUTO_ON   1



/*logging limits */

#define hp816x_MAX_LOGNUMBER   100001
/*logging limits for old modules*/
#define hp816x_MAX_OLD_LOGNR    4001

/*includes 11 bytes header and 1 CR*/
#define hp816x_HEADER_SIZE     12               
#define hp816x_MAX_FUNCMODES   4
#define hp816x_LOGSTAB_TTIME   3600.0 * 24.0
#define hp816x_LOGSTAB_DTIME   3600.0 * 24.0

/*function types*/
#define hp816x_NONE           0
#define hp816x_LOGGING        1
#define hp816x_STABILITY      2
#define hp816x_MINMAX         3

/*MINMAX modes*/
#define hp816x_MM_CONT         0
#define hp816x_MM_WIN          1
#define hp816x_MM_REFRESH      2

/*Trigger Configuration*/
/*input Trigger*/
#define hp816x_PWM_TRIGIN_IGN  0
/*single measurement*/
#define hp816x_PWM_TRIGIN_SME  1
/*measurement completed*/
#define hp816x_PWM_TRIGIN_CME  2


/*output Trigger*/

/*no  trigger*/
#define hp816x_PWM_TRIGOUT_NONE  0 
/*end of averaging trigger*/
#define hp816x_PWM_TRIGOUT_AVG   1
/*begin of averaging trigger*/
#define hp816x_PWM_TRIGOUT_MEAS  2
  
        /***************************************************/
        /*  fixed laser source specific  constants           */
        /***************************************************/


/*available channels for fixed laser*/
#define hp816x_FLS_CHAN_MIN 1
#define hp816x_FLS_CHAN_MAX 2 
#define hp816x_FLS_SRC_SEL_MAX 3 



#define hp816x_FLS_ATTENUATION 0
#define hp816x_FLS_POWER       1
#define hp816x_CC_MODE_OFF     0 
#define hp816x_CC_MODE_ON      1 

#define hp816x_MODULATION_OFF      0 
#define hp816x_MODULATION_ON       1 

/*defines for which laser sources a command is applied */

#define hp816x_LOWER_SRC	0
#define hp816x_UPPER_SRC	1
#define hp816x_BOTH_SRC	  2

#define hp816x_EXTERN_SRC	 2



/*attenuation limits */
#define hp816x_ATT_MIN  0.0
#define hp816x_ATT_MAX 10.0

/* Modulation enabled */
#define hp816x_MOD_DISABLED      0 
#define hp816x_MOD_ENABLED       1 

/* Modulation enabled */
#define hp816x_SBS_CONTROL_DISABLED      0 
#define hp816x_SBS_CONTROL_ENABLED       1 

/* Modulation preselection */
#define hp816x_AM_MIN            0 
#define hp816x_AM_MAX            1 
#define hp816x_AM_DEFAULT        2 
#define hp816x_AM_MANUAL         3 

/* Modulation sources */
#define hp816x_AM_OFF            0 
#define hp816x_AM_INT            1 
#define hp816x_AM_CC						 2 
#define hp816x_AM_LFCC					 3 
#define hp816x_AM_BACKPLANE      4

/* Attenuation mode */
#define hp816x_ATT_MODE          0 
#define hp816x_ATT_POWER         1 

/* laser state */
#define hp816x_LASER_OFF         0 
#define hp816x_LASER_ON          1 

/* power unit*/
#define hp816x_PU_DBM            0 
#define hp816x_PU_WATT           1 
/*only for return loss*/

#define hp816x_PU_DB             2  


/* trigger state*/
#define hp816x_TRIG_DIS          0 
#define hp816x_TRIG_MOD          1 

        /***************************************************/
        /*  return loss module specific  constants         */
        /***************************************************/
/*trigger configuration */
#define hp816x_RLM_TRIGIN_IGN     0
#define hp816x_RLM_TRIGIN_SME     1
#define hp816x_RLM_TRIGIN_CME     2 
    
#define hp816x_RLM_TRIGOUT_NONE   0
#define hp816x_RLM_TRIGOUT_AVG    1 

/* calibration */

#define hp816x_CAL_REFL         0
#define hp816x_CAL_TERM         1 
#define hp816x_CAL_FACTORY      2

/*trigger modes*/
#define hp816x_RLM_IMMEDIATE   0
#define hp816x_RLM_CONTINUOUS  1
    
/*power range*/
#define hp816x_RLM_RANGE_AUTO   1
#define hp816x_RLM_RANGE_MANUAL 0

/*averaging time limits in s for return loss*/
#define hp816x_RLM_ATIME_MIN  20.0E-3
#define hp816x_RLM_ATIME_MAX  10.0


/*attenuation limits*/
#define hp816x_RLM_ATT_MIN   0.0
#define hp816x_RLM_ATT_MAX   3.0



        /***************************************************/
        /*  switch specific  constants                     */
        /***************************************************/

/*input port constants*/
#define hp816x_SWT_INP_A 0
#define hp816x_SWT_INP_B 1 

/*output port constants*/
#define hp816x_SWT_OUT_1 0
#define hp816x_SWT_OUT_2 1
#define hp816x_SWT_OUT_3 2
#define hp816x_SWT_OUT_4 3
#define hp816x_SWT_OUT_5 4
#define hp816x_SWT_OUT_6 5
#define hp816x_SWT_OUT_7 6
#define hp816x_SWT_OUT_8 7
 
        /***************************************************/
        /*  tunable laser source specific  constants         */
        /***************************************************/



/*wavelength units*/
#define hp816x_TLS_CHAN_MIN 1
#define hp816x_TLS_CHAN_MAX 2 


/* Modulation output */
#define hp816x_MOD_ALWAYS        0 
#define hp816x_MOD_LREADY        1 

/*input type for wavelength and pow*/
#define hp816x_INP_MIN       0
#define hp816x_INP_DEF       1
#define hp816x_INP_MAX       2
#define hp816x_INP_MAN       3

/*supported trigger in*/
#define hp816x_TLS_TRIGIN_IGN        0
#define hp816x_TLS_TRIGIN_NEXTSTEP   1
#define hp816x_TLS_TRIGIN_SWEEPSTART 2

/*supported trigger out*/
#define hp816x_TLS_TRIGOUT_DISABLED  0
#define hp816x_TLS_TRIGOUT_MOD       1
#define hp816x_TLS_TRIGOUT_STEPEND   2
#define hp816x_TLS_TRIGOUT_SWSTART   3
#define hp816x_TLS_TRIGOUT_SWEND     4

#define hp816x_TLS_ATTENUATION 0
#define hp816x_TLS_POWER       1

/*optical output modes*/
#define  hp816x_HIGHPOW      0
#define  hp816x_LOWSSE       1
#define  hp816x_BHR          2
#define  hp816x_BLR          3


/*sweep repeat constants*/
#define hp816x_ONEWAY  0
#define hp816x_TWOWAY  1

/*sweep parameter constants*/

#define hp816x_SWEEP_WAVE 0
#define hp816x_SWEEP_POW  1  
#define hp816x_SWEEP_ATT  2


/*sweep state commands*/
#define hp816x_SW_CMD_STOP    0
#define hp816x_SW_CMD_START   1 
#define hp816x_SW_CMD_PAUSE   2
#define hp816x_SW_CMD_CONT    3

/*bnc output constants*/
#define hp816x_BNC_MOD     0
#define hp816x_BNC_VPP     1
#define hp816x_BNC_VPL     2

/*sweep mode constants*/
#define hp816x_SWEEP_STEP    0
#define hp816x_SWEEP_MAN     1 
#define hp816x_SWEEP_CONT    2
#define hp816x_SWEEP_FAST    3

/* attenuation limits for tuneable lasersources*/
#define hp816x_TLS_ATT_MIN    0
#define hp816x_TLS_ATT_MAX    60

/*sweep limits */
#define hp816x_MIN_SWEEP_STEP    0.1e-12
#define hp816x_MIN_SWEEP_CYCLE   1
#define hp816x_MAX_SWEEP_CYCLE   999
#define hp816x_MIN_SWEEP_DWELL   100.0e-3
#define hp816x_MAX_SWEEP_DWELL   1.0e6

/*sweep speeds */
#define hp816x_SWEEP_SPEED_LOW      0.5e-9 
#define hp816x_SWEEP_SPEED_MEDIUM   5.0e-9 
#define hp816x_SWEEP_SPEED_HIGH    40.0e-9 



/*rise time limits */
#define hp816x_MIN_RISETIME      0.0
#define hp816x_MAX_RISETIME      3.0

/*coherence control level range for DFB laser sources*/
#define hp816x_CCMIN_LEVEL      1.0
#define hp816x_CCMAX_LEVEL      99.98

/*SBS level range for Fireball laser sources*/
#define hp816x_SBSMIN_LEVEL      0.0
#define hp816x_SBSMAX_LEVEL      100.0



/* Modulation types */

#define	hp816x_MOD_INT          0 
#define	hp816x_MOD_CC           1 
#define	hp816x_MOD_AEXT         2 
#define	hp816x_MOD_DEXT         3
#define	hp816x_MOD_VWLOCK		    4 
#define	hp816x_MOD_BACKPL		    5 

/*Lambda Scan defines*/
#define	hp816x_NO_OF_SCANS_1			0
#define	hp816x_NO_OF_SCANS_2			1
#define	hp816x_NO_OF_SCANS_3			2


#define hp816x_PWM_CHANNEL_1			0					
#define hp816x_PWM_CHANNEL_2			1					
#define hp816x_PWM_CHANNEL_3			2					
#define hp816x_PWM_CHANNEL_4			3					
#define hp816x_PWM_CHANNEL_5			4					
#define hp816x_PWM_CHANNEL_6			5					
#define hp816x_PWM_CHANNEL_7			6					
#define hp816x_PWM_CHANNEL_8			7					

/*sweep speeds*/
#define hp816x_SPEED_80NM         -1
#define hp816x_SPEED_40NM         0
#define hp816x_SPEED_20NM         1
#define hp816x_SPEED_10NM         2
#define hp816x_SPEED_5NM          3
#define hp816x_SPEED_05NM         4
#define hp816x_SPEED_AUTO         5  




/*baudrate definitions*/

#define hp816x_BAUD_9600          0  
#define hp816x_BAUD_19200         1
#define hp816x_BAUD_38400         2





/*number of channels a multiframe lambda scan can handle*/
#define MAX_MF_LAMBDASCAN_CHAN  1000

/******************************************************************************/
/************************  Utility   Funktions *****************************/
/******************************************************************************/

ViStatus _VI_FUNC hp816x_listVisa_Q (ViInt32 interf, ViBoolean selection,
                                     ViPInt32 noOfDef,  ViPString listofAdresses);

ViStatus _VI_FUNC hp816x_getInstrumentId_Q (ViChar busAddress[],
                                           ViChar IDNString[]);

                                                                

ViStatus _VI_FUNC hp816x_setBaudrate (ViChar interfaceIdentifier[], 
                                               ViUInt32 baudrate);          




               
/******************************************************************************/
/************************  Frame Specific Functions ***************************/
/******************************************************************************/


    
ViStatus _VI_FUNC hp816x_driverLogg (ViSession IHandle, ViString filename,
                                    ViBoolean logging, ViBoolean includeReplies);

    


ViStatus _VI_FUNC hp816x_forceTransaction (ViSession IHandle,
                                          ViBoolean forceTransaction);
    

    

ViStatus _VI_FUNC hp816x_preset (ViSession IHandle);
    


ViStatus _VI_FUNC hp816x_moduleSelftest (ViSession IHandle, ViInt32 slottoTest,
                                        ViPInt16 result,
                                        ViPString selfTestMessage);
    


ViStatus _VI_FUNC  hp816x_lockUnlockInstument (ViSession IHandle, ViBoolean softlock,
                                ViString password);

ViStatus _VI_FUNC hp816x_getLockState (ViSession IHandle, ViBoolean *softLock,
                                      ViBoolean *remoteInterlock);
    

ViStatus _VI_FUNC hp816x_enableDisableDisplay (ViSession IHandle, ViBoolean display);
    

ViStatus _VI_FUNC hp816x_getSlotInformation_Q (ViSession IHandle, ViInt32 arraySize,
                                     ViInt32 slotInfo[]);
    

ViStatus _VI_FUNC hp816x_getModuleStatus_Q (ViSession IHandle,
                                         ViPBoolean statusSummary,
                                         ViInt32 moduleStatusArray[],
                                         ViPInt32 maxMessageLength);
    

ViStatus _VI_FUNC hp816x_convertQuestionableStatus_Q (ViSession IHandle,
                                       ViInt32 questionableStatusInput,
                                       ViPString message);
    
ViStatus _VI_FUNC  hp816x_standardTriggerConfiguration (ViSession IHandle,         
                                                      ViInt32 triggerConfiguration,      
                                                      ViUInt32 nodeAInputConfig,          
                                                      ViUInt32 nodeInputBConfig,          
                                                      ViUInt32 outputMatrixConfiguration);

ViStatus _VI_FUNC  hp816x_standardTriggerConfiguration_Q (ViSession IHandle,         
                                                      ViPInt32 triggerConfiguration,      
                                                      ViPUInt32 nodeAInputConfig,          
                                                      ViPUInt32 nodeInputBConfig,          
                                                      ViPUInt32 outputMatrixConfiguration); 
 

ViStatus _VI_FUNC hp816x_nodeInputConfiguration (ViBoolean connectionFunctionNodeA,  
                                                ViBoolean BNCTriggerConnectorA,      
                                                ViBoolean nodeBTriggerOutput,       
                                                ViBoolean slotA0, ViBoolean slotA1,   
                                                ViBoolean slotA2, ViBoolean slotA3,   
                                                ViBoolean slotA4,                    
                                                ViBoolean connectionfunctionNodeB,  
                                                ViBoolean BNCTriggerConnectorB,      
                                                ViBoolean nodeATriggerOutput,       
                                                ViBoolean slotB0, ViBoolean slotB1,   
                                                ViBoolean slotB2, ViBoolean slotB3,   
                                                ViBoolean slotB4,                    
                                                ViUInt32 *resultNodeA,              
                                                ViUInt32 *resultNodeB);

ViStatus _VI_FUNC hp816x_trigOutConfiguration (ViBoolean nodeswitchedtoBNCOutput,
                                              ViBoolean slot0,    
                                              ViBoolean slot1,    
                                              ViBoolean slot2,    
                                              ViBoolean slot3,    
                                              ViBoolean slot4,
                                              ViPUInt32 result);    

              
  

ViStatus _VI_FUNC hp816x_generateTrigger (ViSession IHandle, ViBoolean triggerAt);

/******************************************************************************/
/************************  Attenuator Specific Funktions ***********************/
/******************************************************************************/

ViStatus _VI_FUNC hp816x_set_ATT_attenuation (ViSession IHandle, ViInt32 ATTSlot,
                                     ViInt32 selection, ViReal64 attenuation,ViBoolean waitForCompletion);
ViStatus _VI_FUNC hp816x_get_ATT_attenuation_Q (ViSession IHandle, ViInt32 ATTSlot,
                                       ViReal64 *minimum, ViReal64 *maximum,
                                       ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_set_ATT_attenuationOffset (ViSession IHandle, ViInt32 ATTSlot,
                                           ViInt32 selection, ViReal64 offset);
ViStatus _VI_FUNC hp816x_get_ATT_attenuationOffset_Q (ViSession IHandle, ViInt32 ATTSlot,
                                             ViReal64 *minimum, ViReal64 *maximum,
                                             ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_set_ATT_attenuatorSpeed (ViSession IHandle, ViInt32 ATTSlot,
                                         ViInt32 selection, ViReal64 speed);
ViStatus _VI_FUNC hp816x_get_ATT_attenuatorSpeed_Q (ViSession IHandle, ViInt32 ATTSlot,
                                           ViReal64 *minimum, ViReal64 *maximum,
                                           ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_ATT_displayToOffset (ViSession IHandle, ViInt32 ATTSlot);
ViStatus _VI_FUNC hp816x_set_ATT_wavelength (ViSession IHandle, ViInt32 ATTSlot,
                                    ViInt32 selection, ViReal64 wavelength);
ViStatus _VI_FUNC hp816x_get_ATT_wavelength_Q (ViSession IHandle, ViInt32 ATTSlot,
                                      ViReal64 *minimum, ViReal64 *maximum,
                                      ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_set_ATT_powerUnit (ViSession IHandle, ViInt32 ATTSlot,
                                   ViBoolean unit);
ViStatus _VI_FUNC hp816x_get_ATT_powerUnit_Q (ViSession IHandle, ViInt32 ATTSlot,
                                     ViBoolean *unit);
ViStatus _VI_FUNC hp816x_set_ATT_absPowerMode (ViSession IHandle, ViInt32 ATTSlot,
                                      ViBoolean absolutePowerMode);
ViStatus _VI_FUNC hp816x_get_ATT_absPowerMode_Q (ViSession IHandle, ViInt32 ATTSlot,
                                        ViBoolean *absolutePowerMode);
ViStatus _VI_FUNC hp816x_set_ATT_power (ViSession IHandle, ViInt32 ATTSlot,
                               ViBoolean powerControl, ViBoolean powerUnit,
                               ViInt32 selection, ViReal64 power);
ViStatus _VI_FUNC hp816x_get_ATT_power_Q (ViSession IHandle, ViInt32 ATTSlot,
                                 ViBoolean *powerControl, ViBoolean *powerUnit,
                                 ViReal64 *minimum, ViReal64 *maximum,
                                 ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_cp_ATT_refFromExtPM (ViSession IHandle, ViInt32 ATTSlot,
                                     ViInt32 slot, ViInt32 channel);
ViStatus _VI_FUNC hp816x_set_ATT_powerReference (ViSession IHandle, ViInt32 ATTSlot,
                                        ViInt32 selection, ViReal64 reference);
ViStatus _VI_FUNC hp816x_get_ATT_powerReference_Q (ViSession IHandle, ViInt32 ATTSlot,
                                          ViReal64 *minimum, ViReal64 *maximum,
                                          ViReal64 *def, ViReal64 *current);
ViStatus _VI_FUNC hp816x_set_ATT_shutterState (ViSession IHandle, ViInt32 ATTSlot,
                                      ViBoolean shutterState);
ViStatus _VI_FUNC hp816x_get_ATT_shutterState_Q (ViSession IHandle, ViInt32 ATTSlot,
                                        ViBoolean *shutterState);
ViStatus _VI_FUNC hp816x_set_ATT_shutterAtPowerOn (ViSession IHandle, ViInt32 ATTSlot,
                                          ViBoolean shutterState);
ViStatus _VI_FUNC hp816x_get_ATT_shutterStateAtPowerOn_Q (ViSession IHandle, ViInt32 ATTSlot,
                                                 ViBoolean *shutterState);
ViStatus _VI_FUNC hp816x_get_ATT_operStatus (ViSession IHandle, ViInt32 ATTSlot,
                                             ViUInt32 *value,
                                             ViChar conditionalInfo[]);
ViStatus _VI_FUNC hp816x_read_ATT_outputPower (ViSession IHandle,     
                                               ViInt32 ATTSlot,       
                                               ViReal64 *outputPower); 
ViStatus _VI_FUNC hp816x_fetch_ATT_outputPower (ViSession IHandle,     
                                               ViInt32 ATTSlot,       
                                               ViReal64 *outputPower); 

ViStatus _VI_FUNC hp816x_set_ATT_wlOffsRefPowermeter (ViSession IHandle, ViInt32 ATTSlot,
                                       ViInt32 slot, ViInt32 channel);
ViStatus _VI_FUNC hp816x_get_ATT_wlOffsRefPowermeter_Q (ViSession IHandle, ViInt32 ATTSlot,
                                         ViInt32 *slot, ViInt32 *channel);

ViStatus _VI_FUNC hp816x_set_ATT_wavelengthOffsetState (ViSession IHandle, ViInt32 ATTSlot,
                                               ViBoolean offsetDependant);
ViStatus _VI_FUNC hp816x_get_ATT_wavelengthOffsetState_Q (ViSession IHandle, ViInt32 ATTSlot,
                                                 ViBoolean *offsetDependancy);
ViStatus _VI_FUNC hp816x_set_ATT_wavelengthOffset (ViSession IHandle, ViInt32 ATTSlot,
                                          ViReal64 wavelength,
                                          ViBoolean offsetSource,
                                          ViReal64 offsetValue);
ViStatus _VI_FUNC hp816x_get_ATT_wavelengthOffsetIndex_Q (ViSession IHandle, ViInt32 ATTSlot,
                                                 ViUInt32 tableIndex,
                                                 ViReal64 *wavelength,
                                                 ViReal64 *offset);
ViStatus _VI_FUNC hp816x_get_ATT_offsetFromWavelength_Q (ViSession IHandle, ViInt32 ATTSlot,
                                                ViReal64 wavelength,
                                                ViReal64 *offset);
ViStatus _VI_FUNC hp816x_delete_ATT_offsetTblEntries (ViSession IHandle, ViInt32 ATTSlot,
                                             ViBoolean noOfEntries,
                                             ViReal64 wavelengthOrIndex);
ViStatus _VI_FUNC hp816x_get_ATT_offsetTable_Q (ViSession IHandle, ViInt32 ATTSlot,
                                       ViReal64 wavelengthArray[],
                                       ViReal64 offsetArray[]);
ViStatus _VI_FUNC hp816x_get_ATT_offsetTblSize_Q (ViSession IHandle, ViInt32 ATTSlot,
                                       ViUInt32 *currentSize, ViUInt32 *maximumSize);
ViStatus _VI_FUNC hp816x_set_ATT_powerOffset (ViSession IHandle, ViInt32 ATTSlot,
                                     ViInt32 selection, ViReal64 offset);
ViStatus _VI_FUNC hp816x_get_ATT_powerOffset_Q (ViSession IHandle, ViInt32 ATTSlot,             
                                             ViReal64 *minimum, ViReal64 *maximum,
                                             ViReal64 *defVal, ViReal64 *actual);
ViStatus _VI_FUNC hp816x_set_ATT_pwrOffsRefPM (ViSession IHandle, ViInt32 ATTSlot, ViInt32 slot,
                               ViInt32 channel);
ViStatus _VI_FUNC hp816x_set_ATT_offsByRefPM (ViSession IHandle, ViInt32 ATTSlot,
                                     ViInt32 slot, ViInt32 channel);
ViStatus _VI_FUNC hp816x_set_ATT_controlLoopState (ViSession IHandle, ViInt32 ATTSlot,
                                          ViBoolean controlLoop);
ViStatus _VI_FUNC hp816x_get_ATT_controlLoopState_Q (ViSession IHandle, ViInt32 ATTSlot,
                                            ViBoolean *controlLoopState);
ViStatus _VI_FUNC hp816x_set_ATT_avTime (ViSession IHandle, ViInt32 ATTSlot,
                                ViReal64 averagingTime);
ViStatus _VI_FUNC hp816x_get_ATT_avTime_Q (ViSession IHandle, ViInt32 ATTSlot,
                                  ViReal64 *averagingTime);
ViStatus _VI_FUNC hp816x_set_ATT_triggerConfig (ViSession IHandle, 
                                               ViInt32 ATTSlot,   
                                               ViInt32 triggerIn); 
ViStatus _VI_FUNC hp816x_get_ATT_triggerConfig_Q (ViSession IHandle, 
                                               ViInt32 ATTSlot,   
                                               ViInt32 *triggerIn);

ViStatus _VI_FUNC hp816x_zero_ATT_powermeter (ViSession IHandle, ViInt32 ATTSlot);
ViStatus _VI_FUNC hp816x_get_ATT_zeroResult_Q (ViSession IHandle, ViInt32 ATTSlot,
                                      ViInt32 *lastZeroResult);
ViStatus _VI_FUNC hp816x_zero_ATT_all (ViSession IHandle);

/******************************************************************************/
/************************  Powermeter Specific Funktions ***********************/
/******************************************************************************/

ViStatus _VI_FUNC hp816x_PWM_slaveChannelCheck (ViSession IHandle,ViInt32 PWMSlot,            
                                                 ViBoolean slaveChannelCheck);


ViStatus _VI_FUNC hp816x_set_PWM_parameters (ViSession IHandle, ViInt32 PWMSlot,
                                   ViInt32 channelNumber, ViBoolean rangeMode,
                                   ViBoolean powerUnit, ViBoolean internalTrigger,
                                   ViReal64 wavelength, ViReal64 averagingTime,
                                   ViReal64 powerRange);
    

ViStatus _VI_FUNC hp816x_get_PWM_parameters_Q (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber,
                                         ViBoolean *rangeMode,
                                         ViBoolean *powerUnit,
                                         ViBoolean *internalTrigger,
                                         ViReal64 *wavelength,
                                         ViReal64 *averagingTime,
                                         ViReal64 *powerRange);
    

ViStatus _VI_FUNC hp816x_set_PWM_referenceSource (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber,
                                         ViInt32 measure,
                                         ViInt32 referenceSource,
                                         ViInt32 slotNumber, ViInt32 channel);

ViStatus _VI_FUNC hp816x_get_PWM_referenceSource_Q (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber,
                                         ViPInt32 measure,
                                         ViPInt32 referenceSource,
                                         ViPInt32 slotNumber, ViPInt32 channel);
    

ViStatus _VI_FUNC hp816x_set_PWM_internalTrigger (ViSession IHandle,
                                              ViInt32 PWMSlot,
                                              ViInt32 channelNumber,
                                              ViBoolean internalTrigger);
    

ViStatus _VI_FUNC hp816x_set_PWM_averagingTime (ViSession IHandle,
                                               ViInt32 PWMSlot,
                                               ViInt32 channelNumber,
                                               ViReal64 averagingTime);
    

ViStatus _VI_FUNC hp816x_get_PWM_averagingTime_Q (ViSession IHandle,
                                               ViInt32 PWMSlot,
                                               ViInt32 channelNumber,
                                               ViReal64 *averagingTime);
    

ViStatus _VI_FUNC hp816x_set_PWM_wavelength (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViReal64 wavelength);
    

ViStatus _VI_FUNC hp816x_get_PWM_wavelength_Q (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViReal64 *minWavelength,
                                            ViReal64 *maxWavelength,
                                            ViReal64 *currentWavelength);
    

ViStatus _VI_FUNC hp816x_set_PWM_calibration (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViReal64 calibration);
    

ViStatus _VI_FUNC hp816x_get_PWM_calibration_Q (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViReal64 *calibration);
    

ViStatus _VI_FUNC hp816x_set_PWM_powerRange (ViSession IHandle, ViInt32 PWMSlot,
                                          ViInt32 channelNumber,
                                          ViBoolean rangeMode,
                                          ViReal64 powerRange);
    

ViStatus _VI_FUNC hp816x_get_PWM_powerRange_Q (ViSession IHandle, ViInt32 PWMSlot,
                                          ViInt32 channelNumber,
                                          ViBoolean *rangeMode,
                                          ViReal64 *powerRange);
    

ViStatus _VI_FUNC hp816x_set_PWM_powerUnit (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber, ViInt32 powerUnit);
    

ViStatus _VI_FUNC hp816x_get_PWM_powerUnit_Q (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber,
                                         ViInt32 *powerUnit);
    

ViStatus _VI_FUNC hp816x_set_PWM_referenceValue (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViReal64 internalReference,
                                            ViReal64 referenceChannel);
 

ViStatus _VI_FUNC hp816x_get_PWM_referenceValue_Q (ViSession IHandle, ViInt32 PWMSlot,                
				                                    ViInt32 channelNumber,                             
								                            ViPInt32 referenceMode,                            
												                    ViPReal64 internalReference,                        
																            ViPReal64 referenceChannel);                        
 

ViStatus _VI_FUNC hp816x_set_PWM_triggerConfiguration (ViSession IHandle, ViInt32 PWMSlot,
                                                       ViInt32 triggerIn, ViInt32 triggerOut);

ViStatus _VI_FUNC hp816x_get_PWM_triggerConfiguration ( ViSession  iHandle,
                                                        ViInt32    slot,
                                                        ViPInt32   trigIn,
                                                        ViPInt32   trigOut
                                                        );
    

ViStatus _VI_FUNC hp816x_PWM_displayToReference (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber);
    

ViStatus _VI_FUNC hp816x_start_PWM_internalTrigger (ViSession IHandle,
                                              ViInt32 PWMSlot,
                                              ViInt32 channelNumber);
    

ViStatus _VI_FUNC hp816x_PWM_readValue (ViSession IHandle, ViInt32 PWMSlot,
                                        ViInt32 channelNumber,
                                        ViReal64 *measuredValue);
    

ViStatus _VI_FUNC hp816x_PWM_fetchValue (ViSession IHandle, ViInt32 PWMSlot,
                                         ViInt32 channelNumber,
                                         ViReal64 *measuredValue);

ViStatus _VI_FUNC hp816x_PWM_readAll (ViSession IHandle,ViUInt32 *numberOfChannels,
                                      ViInt32 slots[],
                                     ViInt32 channels[], ViReal64 values[]);
    

ViStatus _VI_FUNC hp816x_PWM_zeroing (ViSession IHandle, ViInt32 PWMSlot,
                                  ViInt32 channelNumber, ViInt32 *zeroingResult);
    

ViStatus _VI_FUNC hp816x_PWM_zeroingAll (ViSession IHandle,ViInt32 *zeroingResult);




ViStatus _VI_FUNC  hp816x_PWM_ignoreError (ViSession iHandle,ViInt32 slot, 
                                          ViInt32 channelNumber,  
                                          ViBoolean ignoreError,
                                          ViInt32 instrumentErrorNumber);


ViStatus _VI_FUNC hp816x_set_PWM_logging (ViSession IHandle, ViInt32 PWMSlot,
                                           ViInt32 channelNumber,
                                           ViReal64 averagingTime,
                                           ViInt32 numberofValues,
                                           ViInt32 *estimatedTimeout);
    

ViStatus _VI_FUNC hp816x_get_PWM_loggingResults_Q (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViBoolean waitforCompletion,
                                            ViBoolean resultUnit,
                                            ViBoolean *loggingStatus,
                                            ViReal64 loggingResult[]);
    

ViStatus _VI_FUNC hp816x_set_PWM_stability (ViSession IHandle, ViInt32 PWMSlot,
                                             ViInt32 channelNumber,
                                             ViReal64 averagingTime,
                                             ViReal64 periodTime,
                                             ViReal64 totalTime,
                                             ViInt32 *estimatedResults);
    

ViStatus _VI_FUNC hp816x_get_PWM_stabilityResults_Q (ViSession IHandle, ViInt32 PWMSlot,
                                            ViInt32 channelNumber,
                                            ViBoolean waitforCompletion,
                                            ViBoolean resultUnit,
                                            ViBoolean *stabilityStatus,
                                            ViReal64 stabilityResult[]);
    

ViStatus _VI_FUNC hp816x_set_PWM_minMax (ViSession IHandle, ViInt32 PWMSlot,
                                          ViInt32 channelNumber,
                                          ViInt32 minMaxMode,
                                          ViInt32 dataPoints,
                                          ViInt32 *estimatedTimeout);
    

ViStatus _VI_FUNC hp816x_get_PWM_minMaxResults_Q (ViSession IHandle, ViInt32 PWMSlot,
                                        ViInt32 channelNumber,
                                        ViReal64 *minimum, ViReal64 *maximum,
                                        ViReal64 *current);
    

ViStatus _VI_FUNC hp816x_PWM_functionStop (ViSession IHandle, ViInt32 PWMSlot,
                                           ViInt32 channelNumber);



/******************************************************************************/
/************************  Fixed Laser Source Specific Funktions **************/
/******************************************************************************/
    

ViStatus _VI_FUNC hp816x_set_FLS_parameters (ViSession IHandle, ViInt32 FLSSlot, 
                                             ViInt32 wavelengthSource,           
                                             ViBoolean turnLaser,                 
                                             ViInt32  modulationLowerSource,     
                                             ViInt32  modulationUpperSource,     
                                             ViReal64 modulationFreqLowerSource,  
                                             ViReal64 modulationFreqUpperSource,  
                                             ViReal64 attenuationLowerSource,     
                                             ViReal64 attenuationUpperSource);    

ViStatus _VI_FUNC hp816x_get_FLS_parameters_Q (ViSession IHandle, ViInt32 FLSSlot,
                                              ViInt32 *wavelengthSource,
                                              ViBoolean *turnLaser,
                                              ViInt32 *modulationLowerSource,
                                              ViInt32 *modulationUpperSource,
                                              ViReal64 *modulationFreqLowerSource,
                                              ViReal64 *modulationFreqUpperSource,
                                              ViReal64 *attenuationLowerSource,
                                              ViReal64 *attenuationUpperSource);

    
ViStatus _VI_FUNC hp816x_set_FLS_modulation (ViSession IHandle, ViInt32 FLSSlot,
                                               ViInt32 wavelengthSource,
                                               ViInt32 modulationFrequency,
                                               ViInt32 modulationSource,
                                               ViReal64 manualFrequency);
    

ViStatus _VI_FUNC hp816x_get_FLS_modulationSettings_Q (ViSession IHandle, ViInt32 FLSSlot,
                                           ViInt32 wavelengthSource,
                                           ViBoolean *modulationState,
																					 ViInt32  *modSource,
                                           ViReal64 *minimumFrequency,
                                           ViReal64 *maximumFrequency,
                                           ViReal64 *defValFrequency,
                                           ViReal64 *currentFrequency);

ViStatus _VI_FUNC hp816x_set_FLS_triggerState (ViSession IHandle,
                                                      ViInt32 FLSSlot,
                                                      ViUInt16 outputTrigger);

ViStatus _VI_FUNC hp816x_get_FLS_triggerState_Q (ViSession IHandle,
                                                      ViInt32 FLSSlot,
                                                      ViBoolean *outputTrigger);

    
                                                      

ViStatus _VI_FUNC hp816x_set_FLS_laserSource (ViSession IHandle, ViInt32 FLSSlot,
                                             ViInt32 laserSource);
    

ViStatus _VI_FUNC hp816x_get_FLS_laserSource_Q (ViSession IHandle, ViInt32 FLSSlot,
                                             ViInt32 *outputWavelength);
    

ViStatus _VI_FUNC hp816x_get_FLS_wavelength_Q (ViSession IHandle, ViInt32 FLSSlot,
                                            ViReal64 *wavelengthLowerSource,
                                            ViReal64 *wavelengthUpperSource);
    

ViStatus _VI_FUNC hp816x_set_FLS_attenuation (ViSession IHandle, ViInt32 FLSSlot,
                                             ViReal64 attenuationLowerSource,
                                             ViReal64 attenuationUpperSource);
    

ViStatus _VI_FUNC hp816x_get_FLS_attenuation_Q (ViSession IHandle, ViInt32 FLSSlot,
                                             ViReal64 *attenuationLowerSource,
                                             ViReal64 *attenuationUpperSource);

ViStatus _VI_FUNC  hp816x_get_FLS_power (ViSession IHandle,ViInt32 FLSSlot, 
                                         ViInt32 laserSource,ViReal64 *laserPower);

    

ViStatus _VI_FUNC hp816x_set_FLS_laserState (ViSession IHandle, ViInt32 FLSSlot,
                                        ViBoolean laserState);
    

ViStatus _VI_FUNC hp816x_get_FLS_laserState_Q (ViSession IHandle, ViInt32 FLSSlot,
                                         ViBoolean *laserState);


/******************************************************************************/
/************************  Switch Module Specific Funktions   ************/
/******************************************************************************/



ViStatus _VI_FUNC hp816x_get_SWT_type (ViSession IHandle, ViInt32 SWTSlot,                  
                                       ViPInt32 switchType,                                 
                                       ViChar  switchDescription[]);                 
ViStatus _VI_FUNC hp816x_set_SWT_route (ViSession IHandle, ViInt32 SWTSlot,                 
                                        ViInt32 inpt,               
                                        ViInt32 outpt);                                    
ViStatus _VI_FUNC hp816x_get_SWT_route (ViSession IHandle, ViInt32 SWTSlot,                 
                                         ViInt32  inpt,         
                                        ViPInt32 outpt);                                      
ViStatus _VI_FUNC hp816x_get_SWT_routeTable (ViSession IHandle, ViInt32 SWTSlot,                            
                                             ViChar  RouteTable[]);                   


/******************************************************************************/
/************************  Return Loss Module Specific Funktions   ************/
/******************************************************************************/

ViStatus _VI_FUNC hp816x_set_RLM_parameters (ViSession IHandle, ViInt32 RLMSlot, 
                                             ViBoolean internalTrigger,
                                             ViReal64 wavelength,
                                             ViReal64 averagingTime,
                                             ViInt32  laserSource,
                                             ViBoolean laserState);
ViStatus _VI_FUNC hp816x_get_RLM_parameters_Q (ViSession IHandle, ViInt32 RLMSlot,
                                               ViPBoolean internalTrigger,
                                               ViPReal64 wavelength,
                                               ViPReal64 averagingTime,
                                               ViPInt32 laserSource,
                                               ViPBoolean laserState);

ViStatus _VI_FUNC hp816x_set_RLM_internalTrigger (ViSession IHandle,
                                                  ViInt32 RLMSlot,
                                                  ViBoolean internalTrigger);

ViStatus _VI_FUNC hp816x_set_RLM_averagingTime (ViSession IHandle, ViInt32 RLMSlot,
                                                ViReal64 averagingTime);

ViStatus _VI_FUNC hp816x_get_RLM_averagingTime_Q (ViSession IHandle,
                                                  ViInt32 RLMSlot,
                                                  ViPReal64 averagingTime);

ViStatus _VI_FUNC hp816x_set_RLM_wavelength (ViSession IHandle, ViInt32 RLMSlot,
                                             ViReal64 wavelength);

ViStatus _VI_FUNC hp816x_get_RLM_wavelength_Q (ViSession IHandle, ViInt32 RLMSlot,
                                               ViPReal64 minWavelength,
                                               ViPReal64 maxWavelength,
                                               ViPReal64 defWavelength,
                                               ViPReal64 currentWavelength);


ViStatus _VI_FUNC hp816x_calibrate_RLM (ViSession IHandle, ViInt32 RLMSlot,
                                        ViInt32 calibrate);

ViStatus _VI_FUNC hp816x_set_RLM_triggerConfiguration (ViSession IHandle,
                                                       ViInt32 RLMSlot,
                                                       ViInt32 triggerIn,
                                                       ViInt32 triggerOut);

ViStatus _VI_FUNC hp816x_start_RLM_internalTrigger (ViSession IHandle,
                                                    ViInt32 RLMSlot);

ViStatus _VI_FUNC hp816x_RLM_readReturnLoss (ViSession IHandle, ViInt32 RLMSlot,
                                             ViPReal64 returnLoss);

ViStatus _VI_FUNC hp816x_RLM_fetchReturnLoss (ViSession IHandle, ViInt32 RLMSlot,
                                              ViPReal64 returnLoss);


ViStatus _VI_FUNC hp816x_RLM_readValue (ViSession IHandle, ViInt32 RLMSlot, ViBoolean monitorDiode,

                                        ViPReal64 powerValue );



ViStatus _VI_FUNC hp816x_RLM_fetchValue (ViSession IHandle, ViInt32 RLMSlot, ViBoolean monitorDiode,

                                        ViReal64 *powerValue );




ViStatus _VI_FUNC hp816x_RLM_zeroing (ViSession IHandle, ViInt32 RLMSlot,
                                      ViPInt32 zeroingResult);

ViStatus _VI_FUNC hp816x_RLM_zeroingAll (ViSession IHandle,
                                         ViPInt32 summaryofZeroingAll);

ViStatus _VI_FUNC hp816x_set_RLM_powerRange (ViSession IHandle, ViInt32 RLMSlot,
                                             ViBoolean rangeMode,
                                             ViReal64 powerRange,
                                             ViReal64 powerRangeSecondSensor);

ViStatus _VI_FUNC hp816x_get_RLM_powerRange_Q (ViSession IHandle, ViInt32 RLMSlot,
                                               ViPBoolean rangeMode,
                                               ViPReal64 powerRange,
                                               ViPReal64 powerRangeSecondSensor);

ViStatus _VI_FUNC hp816x_set_RLM_rlReference (ViSession IHandle, ViInt32 RLMSlot, 

                                              ViInt32 laserSource, 
                                              ViReal64 returnLossReference);


ViStatus _VI_FUNC hp816x_get_RLM_rlReference_Q (ViSession IHandle,
                                               ViInt32 RLMSlot,ViInt32 laserSource,
                                               ViReal64 *returnLossReference);

ViStatus _VI_FUNC hp816x_set_RLM_FPDelta (ViSession IHandle, ViInt32 RLMSlot,ViInt32 laserSource,
                                         ViReal64 frontPanelDelta);

ViStatus _VI_FUNC hp816x_get_RLM_FPDelta_Q (ViSession IHandle, ViInt32 RLMSlot,ViInt32 laserSource,
                                           ViReal64 *frontPanelDelta);

ViStatus _VI_FUNC hp816x_calculate_RL (ViSession IHandle, ViInt32 RLMSlot,
                                      ViReal64 mref, ViReal64 mpara,
                                      ViReal64 pref, ViReal64 ppara,
                                      ViReal64 mdut, ViReal64 pdut,
                                      ViReal64 FPDelta, ViReal64 *returnLoss);
             

                                                                       
ViStatus _VI_FUNC hp816x_get_RLM_reflectanceValues_Q (ViSession IHandle,
                                                   ViInt32 RLMSlot,ViInt32 laserSource,  
                                                   ViReal64 *mref,   
                                                   ViReal64 *pref);   



ViStatus _VI_FUNC hp816x_get_RLM_terminationValues_Q (ViSession IHandle, 
                                                   ViInt32 RLMSlot, ViInt32 laserSource,  
                                                   ViReal64 *mpara,   
                                                   ViReal64 *ppara);   



ViStatus _VI_FUNC hp816x_get_RLM_dutValues_Q (ViSession IHandle, ViInt32 RLMSlot,
                                           ViReal64 *mdut, ViReal64 *pdut);




ViStatus _VI_FUNC hp816x_get_RLM_srcWavelength_Q (ViSession IHandle,

                                                  ViInt32 RLMSlot,

                                                  ViReal64 *wavelengthLowerSource,

                                                  ViReal64 *wavelengthUpperSource);




ViStatus _VI_FUNC hp816x_set_RLM_laserSourceParameters (ViSession IHandle,
                                                        ViInt32 RLMSlot,
                                                        ViInt32 laserSource,
                                                        ViBoolean turnLaser);

ViStatus _VI_FUNC hp816x_get_RLM_laserSourceParameters_Q (ViSession IHandle,
                                                          ViInt32 RLMSlot,
                                                          ViPInt32 laserSource,
                                                          ViPBoolean laserState);

ViStatus _VI_FUNC hp816x_set_RLM_laserState (ViSession IHandle, ViInt32 RLMSlot,
                                             ViBoolean laserState);


ViStatus _VI_FUNC hp816x_get_RLM_modulationState_Q (ViSession IHandle,

                                                   ViInt32 RLMSlot,

                                                   ViInt32 laserSource,

                                                   ViBoolean *lowFrequencyControl);









ViStatus _VI_FUNC hp816x_set_RLM_modulationState (ViSession IHandle,

                                                 ViInt32 RLMSlot,

                                                 ViInt32 laserSource,

                                                 ViBoolean lowFrequencyControl);




ViStatus _VI_FUNC hp816x_get_RLM_laserState_Q (ViSession IHandle, ViInt32 RLMSlot,
                                               ViPBoolean laserState);

ViStatus _VI_FUNC hp816x_enable_RLM_sweep (ViSession IHandle,
                                          ViBoolean enableRLMLambdaSweep);



ViStatus _VI_FUNC hp816x_set_RLM_logging (ViSession IHandle, ViInt32 RLMSlot,
                                          ViReal64 averagingTime,
                                          ViInt32 dataPoints,
                                          ViPInt32 estimatedTimeout);

ViStatus _VI_FUNC hp816x_get_RLM_loggingResults_Q (ViSession IHandle,
                                                   ViInt32 RLMSlot,
                                                   ViBoolean waitforCompletion,
                                                   ViBoolean resultCalculatedas,

                                                   ViBoolean monitorDiode,     
                                                   ViBoolean *loggingStatus,
                                                   ViReal64 loggingResult[]);

ViStatus _VI_FUNC hp816x_set_RLM_stability (ViSession IHandle, ViInt32 RLMSlot,
                                            ViReal64 averagingTime,
                                            ViReal64 delayTime, ViReal64 totalTime,
                                            ViPInt32 estimatedResults);

ViStatus _VI_FUNC hp816x_get_RLM_stabilityResults_Q (ViSession IHandle,
                                                     ViInt32 RLMSlot,
                                                     ViBoolean waitforCompletion,
                                                     ViBoolean resultUnit,
                                                     ViBoolean *stabilityStatus,
                                                     ViReal64 stabilityResult[]);

ViStatus _VI_FUNC hp816x_set_RLM_minMax (ViSession IHandle, ViInt32 RLMSlot,
                                         ViInt32 minMaxMode, ViInt32 dataPoints,
                                         ViPUInt32 estimatedTime);

ViStatus _VI_FUNC hp816x_get_RLM_minMaxResults_Q (ViSession IHandle,
                                                  ViInt32 RLMSlot,
                                                  ViPReal64 minimum,
                                                  ViPReal64 maximum,
                                                  ViPReal64 current);

ViStatus _VI_FUNC hp816x_RLM_functionStop (ViSession IHandle, ViInt32 RLMSlot);
    
/******************************************************************************/
/************************  Tunable Laser Source Specific Funktions ************/
/******************************************************************************/
ViStatus _VI_FUNC hp816x_WaitForOPC (ViSession IHandle, ViInt32 TLSSlot,
                                    ViBoolean waitforOperationComplete);

ViStatus _VI_FUNC hp816x_set_TLS_parameters (ViSession IHandle, ViInt32 TLSSlot,
                                   ViInt32 powerUnit, ViInt32 opticalOutput,
                                   ViBoolean turnLaser, ViReal64 power,
                                   ViReal64 attenuation, ViReal64 wavelength);
    

ViStatus _VI_FUNC hp816x_get_TLS_parameters_Q (ViSession IHandle, ViInt32 TLSSlot,
                                          ViInt32 *powerUnit,
                                          ViBoolean *laserState,
                                          ViInt32 *opticalOutput,
                                          ViReal64 *power, ViReal64 *attenuation,
                                          ViReal64 *wavelength);
    

ViStatus _VI_FUNC hp816x_set_TLS_wavelength (ViSession IHandle, ViInt32 TLSSlot,
                                            ViInt32 wavelengthSelection,
                                            ViReal64 wavelength);
    

ViStatus _VI_FUNC hp816x_get_TLS_wavelength_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 *minimumWavelength,
                                            ViReal64 *defValWavelength,
                                            ViReal64 *maximumWavelength,
                                            ViReal64 *currentWavelength);
    

ViStatus _VI_FUNC hp816x_set_TLS_power (ViSession IHandle, ViInt32 TLSSlot,
                                       ViInt32 unit, ViInt32 powerSelection,
                                       ViReal64 manualPower);
    

ViStatus _VI_FUNC hp816x_get_TLS_power_Q (ViSession IHandle, ViInt32 TLSSlot,
                                       ViInt32 *powerUnits,
                                       ViReal64 *minimumPower,
                                       ViReal64 *defValPower,
                                       ViReal64 *maximumPower,
                                       ViReal64 *currentPower);
    

ViStatus _VI_FUNC hp816x_set_TLS_opticalOutput (ViSession IHandle, ViInt32 TLSSlot,
                                           ViInt32 setOpticalOutput);
    

ViStatus _VI_FUNC hp816x_get_TLS_opticalOutput_Q (ViSession IHandle, ViInt32 TLSSlot,
                                           ViInt32 *opticalOutput);
    

ViStatus _VI_FUNC hp816x_get_TLS_powerMaxInRange_Q (ViSession IHandle, ViInt32 TLSSlot,
                                             ViReal64 startofRange,
                                             ViReal64 endofRange,
                                             ViReal64 *maximumPower);
    

ViStatus _VI_FUNC hp816x_set_TLS_laserState (ViSession IHandle, ViInt32 TLSSlot,
                                            ViBoolean laserState);
    

ViStatus _VI_FUNC hp816x_get_TLS_laserState_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViBoolean *laserState);
    
ViStatus _VI_FUNC hp816x_set_TLS_laserRiseTime (ViSession IHandle,
                                               ViInt32 TLSSlot,
                                               ViReal64 laserRiseTime);

ViStatus _VI_FUNC hp816x_get_TLS_laserRiseTime (ViSession IHandle,
                                               ViInt32 TLSSlot,
                                               ViPReal64 laserRiseTime);

ViStatus _VI_FUNC hp816x_set_TLS_triggerConfiguration (ViSession IHandle, ViInt32 TLSSlot,
                                         ViInt32 triggerIn, ViInt32 triggerOut);
    
ViStatus _VI_FUNC hp816x_get_TLS_triggerConfiguration (ViSession IHandle, ViInt32 TLSSlot,
                                         ViPInt32 triggerIn, ViPInt32 triggerOut);

ViStatus _VI_FUNC hp816x_set_TLS_attenuation (ViSession IHandle, ViInt32 TLSSlot,
                                             ViBoolean powerMode,
                                             ViBoolean darkenLaser,
                                             ViReal64 attenuation);
    

ViStatus _VI_FUNC hp816x_get_TLS_attenuationSettings_Q (ViSession IHandle, ViInt32 TLSSlot,
                                             ViBoolean *powerMode,
                                             ViBoolean *dark,
                                             ViReal64 *attenuation);
    

ViStatus _VI_FUNC hp816x_set_TLS_dark (ViSession IHandle, ViInt32 TLSSlot,
                                      ViBoolean darkenLaser);
    

ViStatus _VI_FUNC hp816x_get_TLS_darkState_Q (ViSession IHandle, ViInt32 TLSSlot,
                                     ViBoolean *dark);
    
ViStatus _VI_FUNC hp816x_get_TLS_temperatures (ViSession IHandle,
                                              ViReal64 *actualTemperature,
                                              ViReal64 *temperatureDifference,
                                              ViReal64 *temperatureLastZero);

ViStatus _VI_FUNC hp816x_get_TLS_temperaturesEx (ViSession IHandle,
                                                ViInt32 TLSSlot,          
                                                ViReal64 *actualTemperature,
                                                ViReal64 *temperatureDifference,
                                                ViReal64 *temperatureLastZero);

ViStatus _VI_FUNC hp816x_set_TLS_autoCalibration (ViSession IHandle,        
                                                  ViInt32 TLSSlot,          
                                                  ViBoolean autocalibration);

ViStatus _VI_FUNC hp816x_get_TLS_autoCalState (ViSession IHandle,
                                               ViInt32 TLSSlot,
                                               ViBoolean *autoCalibrationState);

ViStatus _VI_FUNC hp816x_get_TLS_accClass (ViSession IHandle, ViInt32 TLSSlot,
                                           ViInt32 *accuracyClass);


ViStatus _VI_FUNC hp816x_TLS_zeroing (ViSession IHandle);

ViStatus _VI_FUNC hp816x_TLS_zeroingAll (ViSession IHandle);

ViStatus _VI_FUNC hp816x_TLS_zeroingEx (ViSession IHandle,
                                       ViInt32 TLSSlot);

ViStatus _VI_FUNC hp816x_displayToLambdaZero (ViSession IHandle, ViInt32 TLSSlot);
    

ViStatus _VI_FUNC hp816x_get_TLS_lambdaZero_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 *lambda0);
    

ViStatus _VI_FUNC hp816x_set_TLS_frequencyOffset (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 offset);
    

ViStatus _VI_FUNC hp816x_get_TLS_frequencyOffset_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 *offset);
    

ViStatus _VI_FUNC hp816x_TLS_configureBNC (ViSession IHandle, ViInt32 TLSSlot,
                                     ViInt32 BNCOutput);
    

ViStatus _VI_FUNC hp816x_get_TLS_BNC_config_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViInt32 *BNCOutput);
    

ViStatus _VI_FUNC hp816x_set_TLS_sweep (ViSession IHandle, ViInt32 TLSSlot,
                                         ViInt32 sweepMode, ViInt32 repeatMode,
                                         ViUInt32 cycles, ViReal64 dwellTime,
                                         ViReal64 startWavelength,
                                         ViReal64 stopWavelength,
                                         ViReal64 stepSize, ViReal64 sweepSpeed);
    

ViStatus _VI_FUNC hp816x_TLS_sweepControl (ViSession IHandle, ViInt32 TLSSlot,
                                          ViInt32 action);
    

ViStatus _VI_FUNC hp816x_get_TLS_sweepState_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViInt32 *sweepState);
    

ViStatus _VI_FUNC hp816x_TLS_sweepNextStep (ViSession IHandle, ViInt32 TLSSlot);
    

ViStatus _VI_FUNC hp816x_TLS_sweepPreviousStep (ViSession IHandle, ViInt32 TLSSlot);

ViStatus _VI_FUNC hp816x_TLS_sweepWait (ViSession  iHandle, ViInt32 TLSSlot);
    

ViStatus _VI_FUNC hp816x_set_TLS_modulation (ViSession IHandle,
                                              ViInt32 TLSSlot,
                                              ViInt32 modulationSource,
                                              ViBoolean modulationOutput,
                                              ViBoolean modulation,
                                              ViReal64 modulationFrequency);
    

ViStatus _VI_FUNC hp816x_get_TLS_modulationSettings_Q (ViSession IHandle, ViInt32 TLSSlot,
                                           ViInt32 *modulationSource,
                                           ViBoolean *modulationOutput,
                                           ViBoolean *modulationState,
                                           ViReal64 *frequency);

ViStatus _VI_FUNC hp816x_set_TLS_SBS_control (ViSession IHandle,
                                              ViInt32 TLSSlot,
                                              ViBoolean mod_state,
                                              ViReal64 modulationFrequency);
    
ViStatus _VI_FUNC hp816x_get_TLS_SBS_control_q (ViSession IHandle, 
                                               ViInt32 TLSSlot,
                                               ViBoolean *mod_state,
                                               ViReal64 *frequency);

ViStatus _VI_FUNC hp816x_set_TLS_ccLevel (ViSession IHandle, ViInt32 TLSSlot,
                                          ViReal64 CCLevel);

ViStatus _VI_FUNC hp816x_get_TLS_ccLevel_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 *CCLevel);

ViStatus _VI_FUNC hp816x_set_TLS_SBSLevel (ViSession IHandle, ViInt32 TLSSlot,
                                          ViReal64 SBSLevel);

ViStatus _VI_FUNC hp816x_get_TLS_SBSLevel_Q (ViSession IHandle, ViInt32 TLSSlot,
                                            ViReal64 *SBSLevel);
    
ViStatus _VI_FUNC  hp816x_set_TLS_lambdaLoggingState (ViSession IHandle,                      
                                                      ViBoolean lambdaLoggingState);

ViStatus _VI_FUNC  hp816x_set_TLS_lambdaLoggingStateEx (ViSession IHandle,
                                                       ViInt32 TLSSlot,
                                                       ViBoolean lambdaLoggingState);

ViStatus _VI_FUNC  hp816x_get_TLS_lambdaLoggingState_Q (ViSession IHandle,
                                                        ViPBoolean lambdaLoggingState);           

ViStatus _VI_FUNC  hp816x_get_TLS_lambdaLoggingStateEx_Q (ViSession IHandle,
                                                         ViInt32 TLSSlot,
                                                         ViPBoolean lambdaLoggingState);           

ViStatus _VI_FUNC  hp816x_get_TLS_wavelengthData_Q (ViSession IHandle,ViInt32 Array_Size,
                                                ViReal64 wavelengthData[]);

ViStatus _VI_FUNC  hp816x_get_TLS_wavelengthDataEx_Q (ViSession IHandle,ViInt32 TLSSlot,
                                                     ViInt32 Array_Size,
                                                     ViReal64 wavelengthData[]);

ViStatus _VI_FUNC  hp816x_get_TLS_wavelengthPoints_Q (ViSession IHandle,
                                                    ViPInt32 numberofWavelengthPoints);

ViStatus _VI_FUNC  hp816x_get_TLS_wavelengthPointsEx_Q (ViSession IHandle,ViInt32 TLSSlot,
                                                       ViPInt32 numberofWavelengthPoints);

ViStatus _VI_FUNC hp816x_get_TLS_powerPoints_Q (ViSession IHandle,
                                               ViInt32 TLSSlot,
                                               ViPInt32 numberofPowerValues);

    

ViStatus _VI_FUNC hp816x_get_TLS_powerData_Q (ViSession IHandle, ViInt32 TLSSlot,
                                             ViInt32 arraySize,
                                             ViReal64 wavelengthData[],
                                             ViReal64 powerData[]);


/******************************************************************************/
/************************  Applications														 ************/
/******************************************************************************/
ViStatus _VI_FUNC hp816x_enableHighSweepSpeed (ViSession IHandle,
                                              ViBoolean highSweepSpeed);

ViStatus _VI_FUNC hp816x_returnEquidistantData (ViSession IHandle,
                                               ViBoolean equallySpacedDatapoints
                                               );
ViStatus _VI_FUNC hp816x_set_LambdaScan_wavelength (ViSession IHandle,             
                                                    ViReal64 powermeterWavelength);
ViStatus _VI_FUNC hp816x_prepareLambdaScan (ViSession IHandle, ViInt32 unit,
                          ViReal64 power,                  
                          ViInt32 opticalOutput,          
                          ViInt32 numberofScans,          
                          ViInt32 PWMChannels,            
                          ViReal64 startWavelength,        
                          ViReal64 stopWavelength,         
                          ViReal64 stepSize,               
                          ViUInt32 *numberofDatapoints,    
                          ViUInt32 *numberofValueArrays);   
                  
ViStatus _VI_FUNC hp816x_getLambdaScanParameters_Q (ViSession IHandle,
                                                     ViReal64 *startWavelength,
                                                     ViReal64 *stopWavelength,
                                                     ViReal64 *averagingTime,
                                                     ViReal64 *sweepSpeed);





ViStatus _VI_FUNC hp816x_executeLambdaScan (ViSession IHandle,         
                                           ViReal64 wavelengthArray[],
                                           ViReal64 powerArray1[],    
                                           ViReal64 powerArray2[],    
                                           ViReal64 powerArray3[],    
                                           ViReal64 powerArray4[],    
                                           ViReal64 powerArray5[],    
                                           ViReal64 powerArray6[],    
                                           ViReal64 powerArray7[],    
                                           ViReal64 powerArray8[]);    


/******************************************************************************/
/************************  Multiple Mainframe Support              ************/
/******************************************************************************/

ViStatus _VI_FUNC hp816x_registerMainframe (ViSession IHandle);  
ViStatus _VI_FUNC hp816x_unregisterMainframe (ViSession IHandle);
ViStatus _VI_FUNC hp816x_setSweepSpeed    (ViSession IHandle,
                                              ViInt32 sweepSpeed);
ViStatus _VI_FUNC hp816x_prepareMfLambdaScan (ViSession IHandle,                
                                             ViInt32 powerUnit, ViReal64 power,
                                             ViInt32 opticalOutput,            
                                             ViInt32 numberofScans,            
                                             ViInt32 PWMChannels,              
                                             ViReal64 startWavelength,         
                                             ViReal64 stopWavelength,          
                                             ViReal64 stepSize,                
                                             ViUInt32 *numberofDatapoints,     
                                             ViUInt32 *numberofChannels);  
ViStatus _VI_FUNC hp816x_executeMfLambdaScan (ViSession IHandle,
                                              ViReal64 wavelengthArray[]);

ViStatus _VI_FUNC hp816x_getMFLambdaScanParameters_Q (ViSession IHandle,
                                                     ViReal64 *startWavelength,
                                                     ViReal64 *stopWavelength,
                                                     ViReal64 *averagingTime,
                                                     ViReal64 *sweepSpeed);


ViStatus _VI_FUNC hp816x_getLambdaScanResult (ViSession IHandle,
                                             ViInt32 PWMChannel,
                                             ViBoolean clippUnderRange,
                                             ViReal64 clippingLimit,
                                             ViReal64 powerArray[],
                                             ViReal64 lambdaArray[]);

ViStatus _VI_FUNC hp816x_getNoOfRegPWMChannels_Q (ViSession IHandle,
                                                   ViPUInt32 numberofPWMChannels);



ViStatus _VI_FUNC hp816x_getChannelLocation (ViSession IHandle,
                                            ViInt32 PWMChannel,
                                            ViInt32 *mainframeNumber,
                                            ViInt32 *slotNumber,
                                            ViInt32 *channelNumber);     

ViStatus _VI_FUNC hp816x_excludeChannel (ViSession IHandle, ViInt32 PWMChannel,ViBoolean excludeChannel);


ViStatus _VI_FUNC hp816x_setInitialRangeParams (ViSession IHandle, ViInt32 PWMChannel,
                                                ViBoolean resettoDefault,
                                                ViReal64 initialRange,
                                                ViReal64 rangeDecrement);
ViStatus _VI_FUNC hp816x_setScanAttenuation (ViSession IHandle,
                                            ViReal64 scanAttenuation);



ViStatus _VI_FUNC hp816x_getWlRespTblSize (ViSession IHandle, ViInt32 slot,        
                                           ViPUInt32 size, ViPUInt32 CSVSize);
ViStatus _VI_FUNC hp816x_getWlRespTblSizeEx (ViSession IHandle, ViInt32 slot, ViInt32 chan,        
                                             ViPUInt32 size, ViPUInt32 CSVSize);
    
ViStatus _VI_FUNC hp816x_readWlRespTable ( ViSession IHandle,ViInt32 slot,        
                                          ViReal64  wavelength[],          
                                          ViReal64  responseFactor[]); 
 
ViStatus _VI_FUNC hp816x_readWlRespTableEx ( ViSession IHandle,ViInt32 slot, ViInt32 chan,       
                                             ViReal64  wavelength[],          
                                             ViReal64  responseFactor[]); 

ViStatus _VI_FUNC hp816x_readWlRepTblCSV (ViSession IHandle, ViInt32 slot,        
                                          ViChar CSVList[]); 

ViStatus _VI_FUNC hp816x_readWlRepTblCSV_Ex (ViSession IHandle, ViInt32 slot, ViInt32 chan,        
                                             ViChar CSVList[]);               



ViStatus _VI_FUNC hp816x_spectralCalibration (ViSession IHandle, ViInt32 slot,       
                                                 ViUInt32 size_of_Spectrum, 
                                                 ViReal64 wavelength[],    
                                                 ViReal64 power[],
                                                 ViReal64 *wavelengthResult,
                                                 ViChar error_Diagnose[]); 
ViStatus _VI_FUNC hp816x_spectralCalibrationEx (ViSession IHandle, ViInt32 slot, ViInt32 chan,     
                                                 ViUInt32 size_of_Spectrum, 
                                                 ViReal64 wavelength[],    
                                                 ViReal64 power[],
                                                 ViReal64 *wavelengthResult,
                                                 ViChar error_Diagnose[]);        

/* BASIC END */


/* End of instrument specific declarations */
/*---------------------------------------------------------------------------*/

/* Used for "C" externs in C++ */
#if defined(__cplusplus) || defined(__cplusplus__)
}
#endif 

#endif /* hp816x_INCLUDE */

