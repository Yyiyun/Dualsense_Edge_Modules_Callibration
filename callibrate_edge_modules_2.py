# import time
# import hid
# from enum import Enum
# from threading import Lock

# ########################################
# # Enums from the original code
# ########################################

# # These correspond to HID report IDs for various commands and data exchanges.
# class ReportId(Enum):
#     # Set and get BT configurations
#     SET_BT_CONTROL = 8
#     GET_BT_PAIRING = 9
#     SET_BT_PAIRING = 10
    
#     # Firmware related
#     GET_FIRM_INFO = 32
    
#     # Audio controls
#     SET_AUDIO_CONTROL = 33
#     GET_MANUFACTURING_INFO = 34
    
#     # Test and calibration commands
#     SET_TEST_COMMAND = 128
#     GET_TEST_RESULT = 129
#     SET_CALIBRATION_COMMAND = 130
#     GET_CALIBRATION_DATA = 131
#     SET_INDIVIDUAL_DATA = 132
#     GET_INDIVIDUAL_DATA_RESULT = 133
    
#     # DFU (Device Firmware Update)
#     SET_DFU_ENABLE = 160
#     GET_SYSTEM_PROFILE = 224
#     FLASH_CMD = 240
#     GET_FLASH_CMD_STATUS = 241
#     USER_UPDATE_CMD = 244
#     USER_GET_UPDATE_STATUS = 245
    
#     # Input/Output for standard controller reports
#     INPUT_REPORT = 1
#     INPUT_REPORT_BT = 17
#     INPUT_REPORT_BT_PPR = 49
#     OUTPUT_REPORT_ID = 2
#     OUTPUT_REPORT_BT = 17
#     OUTPUT_REPORT_BT_PPR = 49
    
#     # IR Code Setup
#     SET_IR_CODE_SET = 112
#     GET_IR_CODE_SET_RESULT = 113


# # Devices under test (the controller segments or subsystems that can be tested)
# # and what actions we can perform on them
# class TestDeviceId(Enum):
#     SYSTEM = 1         # System-level operations (e.g., reset, PCBA ID, etc.)
#     POWER = 2          # Power-related tests
#     MOEMORY = 3         # Possibly memory-related tests (typo in original code, likely 'MEMORY')
#     ANALOG_DATA = 4     # Analog data tests (sticks, triggers)
#     TOUCH = 5           # Touchpad tests
#     AUDIO = 6           # Audio subsystem tests
#     ADAPTIVE_TRIGGER = 7 # In original code, "BULLET"/"WALTHER" or "ADAPTIVE_TRIGGER" tests
#     BULLET = 8          # Bullet (Adaptive Trigger) tests or actuator tests
#     BLUETOOTH = 9       # Bluetooth-related tests
#     MOTION = 10         # Motion sensor tests (accelerometer/gyro)
#     TRIGGER = 11        # Trigger-related tests
#     STICK = 12          # Analog stick tests
#     LED = 13            # LED tests
#     BT_PATCH = 14       # Bluetooth patch info retrieval
#     DSP_FW = 15         # DSP firmware tests
#     SPIDER_DSP_FW = 16  # Spider DSP firmware tests
#     FINGER = 17         # Finger/Capacitive sensor tests
#     POSITION_TRACKING = 19 # Position tracking tests
#     BUILTIN_MIC_CALIB_DATA = 20 # Built-in mic calibration data tests (in original code)
#     STICK_MODULE = 21   # Stick module tests
#     UNKNOWN_22 = 22     # Unknown device ID
#     UNKNOWN_23 = 23     # Unknown device ID
#     UNKNOWN_24 = 24     # Unknown device ID
#     TELEMETRY = 112 # Telemetery actions

# # Actions (commands) that can be performed on these devices
# class TestActionId(Enum):
#     # System actions
#     RESET = 1
#     WRITE_PCBAID = 3
#     READ_PCBAID = 4
#     WRITE_HWVERSION = 5
#     READ_HWVERSION = 6
#     WRITE_FACTORY_DATA = 7
#     READ_FACTORY_DATA = 8
#     GET_MCU_UNIQUE_ID = 9
#     READ_PANIC_LOG = 10
#     CLEAR_PANIC_LOG = 11
#     WRITE_HW_INFO_WITH_DEVICE_INFO = 15
#     WRITE_PCBAID_FULL = 16
#     READ_PCBAID_FULL = 17
#     READ_SERIAL_NUMBER = 19
#     READ_ASSEMBLE_PARTS_INFO = 21
#     READ_BATTERY_BARCODE = 24
#     READ_VCM_LEFT_BARCODE = 26
#     READ_VCM_RIGHT_BARCODE = 28
    
#     # Power actions
#     SLEEP = 1
#     CHG_FORCE_ENABLE = 2
#     CHG_FORCE_DISABLE = 3
#     CHG_ENABLE_SET = 4
#     CHG_ENABLE_CLR = 5
#     BATTERY_VOLTAGE = 6
#     GET_FORCE_ENABLE = 7
#     GET_CHG_ENABLE = 8
    
#     # Memory actions
#     NVS_LOCK = 1
#     NVS_UNLOCK = 2
#     NVS_GET_STATUS = 3
    
#     # Analog data actions
#     ANALOG_TRIGGER = 1
#     ANALOG_STICK = 2
#     BATTERY = 3
    
#     # Touch actions (e.g., SOLOMON, CYPRESS)
#     SOLOMON_SELF_TEST = 1
#     SOLOMON_UID = 2
#     SOLOMON_DIAG = 3
#     SOLOMON_VERSION = 4
#     CYPRESS_VERSION = 33
#     CYPRESS_UNIQUE_ID = 34
#     CYPRESS_CALIBRATION = 35
#     CYPRESS_SIGNAL_STEP_1 = 36
#     CYPRESS_SIGNAL_STEP_2 = 37
#     CYPRESS_SELF_TEST = 38
#     CYPRESS_DEVICE_SELECT = 39
    
#     # Audio actions
#     WAVEOUT_CTRL = 2
#     READ_CODEC_FW_INFO = 3
#     SET_PATH_SELECTOR = 4
#     CTRL_SPK_COMP = 5
#     SET_NOISE_CANCELLER_TYPE = 6
#     SET_MIC_GAIN = 7
#     SET_PARAM_ENABLE_LR = 18
#     SET_MODE_PARAM_LR_FOR_MANU = 19
#     SET_MODE_PARAM_LR = 20
#     GET_CALIB_DATA_LR = 21
#     GET_VALUES = 22
#     GET_WALTHER_INFO = 24
#     WRITE_CALIB_DATA = 33
#     READ_CALIB_DATA = 34
#     ERASE_CALIB_DATA = 35
#     WRITE_TRACABILITY_INFO = 36
#     READ_TRACABILITY_INFO = 37
#     ERASE_TRACABILITY_INFO = 38
#     WRITE_CALIB_DATA_DEV = 49
#     READ_CALIB_DATA_DEV = 50
#     ERASE_CALIB_DATA_DEV = 51
#     WRITE_TRACABILITY_INFO_DEV = 52
#     READ_TRACABILITY_INFO_DEV = 53
#     ERASE_TRACABILITY_INFO_DEV = 54
#     WRITE_CALIBRATION_COEFFICIENT = 64
#     READ_CALIBRATION_COEFFICIENT = 65
#     SET_VALID_CALIBRATION_METHOD = 66
#     GET_VALID_CALIBRATION_METHOD = 67
    
#     # Bullet/Walther/Adaptive Trigger actions
#     SET_BULLET_TYPE = 3
#     GET_BULLET_TYPE = 4
    
#     # Bluetooth actions
#     WRITE_BDADR = 1
#     READ_BDADR = 2
#     SET_VCOM = 3
#     SET_BT_ENABLE = 5
#     GET_BT_ENABLE = 6
#     SET_DUT_MODE = 7
#     READ_EFUSE = 8
#     WRITE_EFUSE = 9
#     GET_XTAL_TXPOWER = 10
#     WRITE_XTAL_OFFSET = 11
#     WRITE_XTAL_TXPOWER = 12
#     READ_PATCH_INFO = 13
#     GET_RAW_RSSI = 14
#     AGING_STATE = 15
#     AGING_INIT = 16

#     # Update and verification actions
#     WRITE_RAW_CALIBRATION_DATA = 1
#     READ_RAW_CALIBRATION_DATA = 2
#     ERASE_CALIBRATION_DATA = 3
#     CHIP_READ = 5
#     WRITE_INIT = 1
#     DATA_SEND = 2
#     DATA_START_VERIFY = 3
#     DATA_FINALIZE = 5
#     DATA_GET_VERIFY_STATUS = 7
#     DATA_SEND_ALL = 18
#     SPIDER_DSP_FW_DATA_VERISION = 4

#     # Finger/Position tracking (additional)
#     GET_INFO = 1
#     SET_SENS_STATUS = 2
#     GET_SENS_STATUS = 3
#     SET_FILTER_LENGTH = 4
#     GET_FILTER_LENGTH = 5
#     SET_ONOFF_HYSTERESIS = 6
#     GET_ONOFF_HYSTERESIS = 7
#     SET_CAP_SENS_OFFSET_CORRECT = 8
#     CLEAR_CAP_SENS_OFFSET_CORRECT = 9
#     SAVE_CONFIG = 10
#     ERASE_CONFIG = 11
#     GET_CALIB_DATA = 128
#     GET_SENS_DATA = 129
#     WRITE_CIRQUE_REG = 162
#     READ_CIRQUE_REG = 163
#     SET_CIRQUE_GAIN = 164
#     GET_CIRQUE_GAIN = 165
#     SET_CIRQUE_OFFSET = 166
#     GET_CIRQUE_OFFSET = 167
#     SET_OLYMPUS_0p1_CONFIG = 168
#     GET_OLYMPUS_0p1_CONFIG = 169
#     SET_OLYMPUS_CONFIG = 170
#     GET_OLYMPUS_CONFIG = 171
#     SET_LED_BRIGHTNESS = 11
#     SET_LED_BRIGHTNESS_ALL = 12
#     GET_LED_BRIGHTNESS_ALL = 15
#     SET_POSITION_TRACKING_ENABLE = 18
#     SET_POSITION_TRACKING_DISABLE = 19
#     SET_ALWAYS_ON_STARTUP_ENABLE = 20
#     SET_ALWAYS_ON_STARTUP_DISABLE = 21
#     GET_POSITION_TRACKING_STATE = 22
#     GET_ALWAYS_ON_STARTUP_STATE = 23

#     # Unknown actions
#     SET_AUTO_SWITCHOFF_ENABLE = 30
#     SET_AUTO_SWITCHOFF_DISABLE = 31
#     GET_AUTO_SWITCHOFF_FLG = 32

#     # Built-in mic calibration data actions
#     BUILTIN_MIC_CALIB_DATA_INIT = 1
#     BUILTIN_MIC_CALIB_DATA_SEND = 2
#     BUILTIN_MIC_CALIB_DATA_STORE = 3
#     BUILTIN_MIC_CALIB_DATA_VERIFY = 4
#     BUILTIN_MIC_CALIB_DATA_GET = 5

#     # Stick module actions
#     STICK_MODULE_SELF_TEST = 1
#     STICK_MODULE_SET_SOMETHING = 2
#     STICK_MODULE_GET_SOMETHING = 3
#     STICK_MODULE_UNKNOWN_1 = 4
#     STICK_MODULE_UNKNOWN_2 = 5
#     STICK_MODULE_UNKNOWN_3 = 6
#     STICK_MODULE_SET_CALIBRATION = 17
#     STICK_MODULE_GET_CALIBRATION = 18
#     STICK_MODULE_SET_SERIAL_NUMBER = 19
#     STICK_MODULE_GET_SERIAL_NUMBER = 20
#     STICK_MODULE_SET_BLINKING_ON = 49
#     STICK_MODULE_SET_BLINKING_OFF = 50
#     STICK_MODULE_GET_BLINKING = 51

# class TestResult(Enum):
#     TEST_RESULT_COMPLETE = 0
#     TEST_RESULT_COMPLETE_2 = 1
#     TEST_RESULT_FAIL = 2
#     TEST_RESULT_SET_FAIL = 3
#     TEST_RESULT_TIMEOUT = 4
#     TEST_RESULT_UNKNOWN = 5

# ########################################
# # Device Info and Setup
# ########################################

# class DeviceInfo:
#     FeatureReportByteLength = 64  # Example length

# DevInfo = DeviceInfo()

# # Replace these with your actual VID and PID
# VENDOR_ID = 0x054C
# PRODUCT_ID_NORM = 0x0CE6 # Normal
# PRODUCT_ID_EDGE = 0x0DF2 # Edge

# m_testCmdLock = Lock()

# ########################################
# # HID Device Initialization
# ########################################
# def open_device():
#     device = hid.device()
    
#     try:
#         device.open(VENDOR_ID, PRODUCT_ID_NORM)
#         print("[DEBUG] Device opened successfully with normal PID.")
#         return device
#     except Exception as e:
#         try:
#             device.open(VENDOR_ID, PRODUCT_ID_EDGE)
#             print("[DEBUG] Device opened successfully with Edge PID.")
#             return device
#         except Exception as e:
#             print(f"[ERROR] Could not open device: {e}")
#             return None

# ########################################
# # Feature Report Handling with hidapi
# ########################################

# def SendFeatureReport(device, data, length):
#     if length > len(data):
#         print("[ERROR] Length exceeds data array size.")
#         return False

#     out_data = bytes(data[:length])
#     try:
#         res = device.send_feature_report(out_data)
#         if res == length:
#             # Convert bytes to list of integers
#             formatted_data = list(out_data) + [0] * (64 - len(out_data))
#             # print(f"[DEBUG] Sent feature report successfully: {formatted_data}")
#             return True
#         else:
#             print(f"[ERROR] Failed to send full feature report. Sent: {res}/{length}")
#             return False
#     except Exception as e:
#         print(f"[ERROR] Exception in SendFeatureReport: {e}")
#         return False

# def GetFeatureReport(device, report_id, length):
#     try:
#         report = device.get_feature_report(report_id, length)
#         if len(report) > 0:
#             if report == [129, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
#                 # print("[DEBUG] Nothing to see")
#                 return None
#             print(f"[DEBUG] Received feature report (len={len(report)}): {report}")
#             return bytearray(report)
#         else:
#             print("[ERROR] Received empty report.")
#             return None
#     except Exception as e:
#         print(f"[ERROR] Exception in GetFeatureReport: {e}")
#         return None

# ########################################
# # TestResult Retrieval
# ########################################

# def GetTestResult(device, devicdId, actionId, featureReport, timeoutMs):
#     start_time = time.time()
#     while (time.time() - start_time)*1000 < timeoutMs:
#         resp = GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         if resp and resp[0] == 129:
#             status = resp[3]
#             # According to original logic, status=2 means COMPLETE, status=3 means COMPLETE_2
#             if status == 2: # COMPLETE
#                 print("[DEBUG] Test result: COMPLETE")
#                 for i in range(len(featureReport)):
#                     featureReport[i] = resp[i] if i < len(resp) else 0
#                 return TestResult.TEST_RESULT_COMPLETE
#             elif status == 3: # COMPLETE_2
#                 print("[DEBUG] Test result: COMPLETE_2")
#                 for i in range(len(featureReport)):
#                     featureReport[i] = resp[i] if i < len(resp) else 0
#                 return TestResult.TEST_RESULT_COMPLETE_2
#             # You can handle other statuses if needed.
#         time.sleep(0.01)
#     print("[ERROR] GetTestResult timed out.")
#     return TestResult.TEST_RESULT_TIMEOUT

# def SetGetTestCommand(device, devicdId, actionId, param=None, paramLength=0, getData=None, getDataLength=0, timeoutMs=1000, IgnoreLength=0):
#     featureReport = [0]*(DevInfo.FeatureReportByteLength)
#     featureReport[0] = 128
#     featureReport[1] = devicdId.value
#     featureReport[2] = actionId.value
#     if param and paramLength > 0:
#         for i in range(paramLength):
#             featureReport[3 + i] = param[i]

#     if not SendFeatureReport(device, featureReport, 3 + paramLength):
#         return TestResult.TEST_RESULT_SET_FAIL

#     resp_buffer = [0]*DevInfo.FeatureReportByteLength
#     test_result = GetTestResult(device, devicdId, actionId, resp_buffer, timeoutMs)
#     if test_result == TestResult.TEST_RESULT_COMPLETE:
#         if getData is not None:
#             copy_len = min(getDataLength, 56 - IgnoreLength)
#             for i in range(copy_len):
#                 getData[i] = resp_buffer[4 + IgnoreLength + i]
#     return test_result

# def SetGetTestCommand_GetRetry(device, devicdId, actionId, param, paramLength, getData, getDataLength, timeoutMs, getTestResultRetryNum, IgnoreLength=0):
#     if getTestResultRetryNum == 0:
#         # If no retries needed, just run a single command.
#         if paramLength > 0:
#             return SetGetTestCommand(device, devicdId, actionId, param, paramLength, getData, getDataLength, timeoutMs, IgnoreLength)
#         return SetGetTestCommand(device, devicdId, actionId, None, 0, getData, getDataLength, timeoutMs)

#     with m_testCmdLock:
#         featureReport = [0]*DevInfo.FeatureReportByteLength
#         b = 0
#         featureReport[0] = 128
#         featureReport[1] = devicdId.value
#         featureReport[2] = actionId.value

#         if paramLength > 0 and param is not None:
#             for i in range(paramLength):
#                 featureReport[3 + i] = param[i]

#         if not SendFeatureReport(device, featureReport, 3 + paramLength):
#             return TestResult.TEST_RESULT_SET_FAIL

#         num = 0
#         while True:
#             resp_buffer = [0]*DevInfo.FeatureReportByteLength
#             testResult = GetTestResult(device, devicdId, actionId, resp_buffer, timeoutMs)

#             if testResult == TestResult.TEST_RESULT_COMPLETE_2:
#                 # Append chunk of data
#                 copy_len = 56 - IgnoreLength
#                 start_index = (56 - IgnoreLength)*b
#                 for i in range(copy_len):
#                     getData[start_index + i] = resp_buffer[4 + IgnoreLength + i]
#                 b += 1

#             elif testResult == TestResult.TEST_RESULT_COMPLETE:
#                 # Final chunk of data
#                 remaining = getDataLength - (56 - IgnoreLength)*b
#                 copy_len = (56 - IgnoreLength) if remaining > (56 - IgnoreLength) else remaining
#                 start_index = (56 - IgnoreLength)*b
#                 for i in range(copy_len):
#                     getData[start_index + i] = resp_buffer[4 + IgnoreLength + i]

#                 # If we got a COMPLETE result, we stop further polling.
#                 # No more feature reports are requested after success.
#                 # This prevents unnecessary debug prints.
#                 break

#             elif testResult == TestResult.TEST_RESULT_FAIL:
#                 return TestResult.TEST_RESULT_FAIL

#             elif testResult == TestResult.TEST_RESULT_TIMEOUT:
#                 num += 1

#             # If WRITE_FACTORY_DATA and COMPLETE, break early
#             if actionId == TestActionId.WRITE_FACTORY_DATA and testResult == TestResult.TEST_RESULT_COMPLETE:
#                 break

#             # If we have retried enough times, break out
#             if num >= getTestResultRetryNum:
#                 break

#             # If test is not complete yet but not failed, wait a short time before the next attempt
#             if testResult != TestResult.TEST_RESULT_COMPLETE:
#                 time.sleep(0.01)

#         return testResult
    
# def do_trigger_calibration():
#     print("Starting trigger calibration...")

#     # [131, 3, 1, 2, 1, 1, 0, 26, 1, 12, 246, 11, 254, 11, 246, 11, 2, 2, 255, 11, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#     # [131, 3, 1, 2, 1, 1, 0, 26, 85, 2, 246, 11, 95, 2, 246, 11, 2, 2, 95, 2, 0, 0, 95, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#     # [131, 3, 1, 2, 1, 1, 0, 26, 85, 2, 246, 11, 95, 2, 246, 11, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#     # [131, 3, 1, 2, 1, 1, 0, 26, 85, 2, 246, 11, 95, 2, 246, 11, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#     SendFeatureReport(device, [130, 1, 3, 1, 1], 5)
#     time.sleep(1)
#     # GetFeatureReport(device, 131, 64)

#     for i in range(2):
#         print("L2: release and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 1, 1], 5)
    
#     time.sleep(1)
#     GetFeatureReport(device, 131, 64)

#     for i in range(2):
#         print("L2: mid and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 2, 1], 5)

#     time.sleep(1)
#     GetFeatureReport(device, 131, 64)

#     for i in range(2):
#         print("L2: full and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 3, 1], 5)

#     time.sleep(1)
#     GetFeatureReport(device, 131, 64)

#     time.sleep(1)

#     SendFeatureReport(device, [130, 2, 3, 1, 1], 5)

#     time.sleep(1)
#     GetFeatureReport(device, 131, 64)

#     SendFeatureReport(device, [130, 1, 3, 1, 2], 5)

#     for i in range(2):
#         print("R2: release and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 1, 2], 5)

#     for i in range(2):
#         print("R2: mid and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 2, 2], 5)

#     for i in range(2):
#         print("R2: full and press enter")
#         input()
#         SendFeatureReport(device, [130, 3, 3, 3, 2], 5)

#     print("Write.")
#     time.sleep(1)
#     SendFeatureReport(device, [130, 2, 3, 0, 2], 5)

#     print("Trigger calibration done!!")
#     print()


# ########################################
# if __name__ == "__main__":

#     try:
#         device = open_device()
#         if device is None:
#             print("[ERROR] No device found. Exiting.")
#             exit(1)

#         # 3 in the byte number 3 in array sugest that there is more data to be read
#         # example: [129, 112, 1, 3, data]

#         #Password from reverse engineering (hex: 65 32 40 0C) ai come up with this password
#         #unlock_params = [0x65, 0x32, 0x40, 0x0C]

#         # trigger data from edege: 129, 11, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 250, 11, 159, 11, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 0, 0, 0, 0, 0, 0]
        
#         # devId = TestDeviceId.STICK_MODULE
#         # actId = TestActionId(18)
#         # # actId = TestActionId(3)
#         # param = [0x00, 0x00, 0x00, 0x00] + [11] * 8
#         # paramLength = 12
#         # getData = [0] * 512
#         # getDataLength = 512
#         # timeoutMs = 1000
#         # getTestResultRetryNum = 3
#         # IgnoreLength = 0

#         # # print("Action:", actId)

#         # result = SetGetTestCommand_GetRetry(device, devId, actId, param, paramLength, getData, getDataLength, timeoutMs, getTestResultRetryNum, IgnoreLength)
#         # print("Final Result:", result)
#         # # print("Data:", getData[:20])
#         # # print("Data:", getData)

#         # [129, 23, 2, 2, 1, 10, 191, 1, 163, 2, 132, 3, 76, 5, 16, 7, 218, 8, 157, 10, 101, 12, 70, 13, 38, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
#         # Data from trigers report id part of it is in adaptive triggers report id
#         # [129, 11, 2, 3, 2, 0, 1, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 245, 11, 0, 0, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 0, 0, 0, 0, 0, 0]
#         # [129, 11, 2, 3, 2, 0, 1, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 245, 11, 0, 0, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 0, 0, 0, 0, 0, 0]

#         # Data from adaptive triggers report id for kacper edge
#         # 34, 0
#         # [129, 7, 34, 2, 0, 229, 11, 4, 3, 9, 0, 250, 11, 159, 11, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 219, 11, 255, 10, 68, 10, 102, 9, 166, 8, 182, 7, 222, 6, 243, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         # 34, 1
#         # [129, 7, 34, 2, 0, 50, 64, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#         # Data from adaptive triggers report id for my dualsense
#         # 34, 0 left trigger calibration
#         # [129, 7, 34, 2, 0, 112, 12, 72, 3, 9, 0, 11, 7, 177, 6, 86, 6, 239, 5, 115, 5, 220, 4, 54, 4, 145, 3, 141, 2, 112, 12, 184, 11, 248, 10, 61, 10, 117, 9, 158, 8, 200, 7, 233, 6, 175, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         # 34, 1 right trigger calibration
#         # [129, 7, 34, 2, 0, 105, 12, 77, 3, 9, 0, 49, 6, 230, 5, 146, 5, 53, 5, 211, 4, 94, 4, 225, 3, 63, 3, 58, 2, 102, 12, 163, 11, 210, 10, 17, 10, 57, 9, 92, 8, 133, 7, 165, 6, 112, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#         # need to restart controller after trigger calibration:
#         # changing adaptive triggers will save without unlocking nvs
#         # 33, 0 is right trigger calibration
#         # 33, 1 is left trigger calibration
#         # kacper edge calibration     
#         # SendFeatureReport(device, [128, 7, 33, 0] + [229, 11, 4, 3, 9, 0, 250, 11, 159, 11, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 219, 11, 255, 10, 68, 10, 102, 9, 166, 8, 182, 7, 222, 6, 243, 5, 0, 5], 46)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 7, 34, 0] + [0] * 61, 64)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # SendFeatureReport(device, [128, 7, 33, 0] + [229, 11, 4, 3, 9, 0, 250, 11, 159, 11, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3, 219, 11, 255, 10, 68, 10, 102, 9, 166, 8, 182, 7, 222, 6, 243, 5, 0, 5], 46)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 7, 34, 0] + [0] * 61, 64)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)


#         # kacper edge calibration
#         # SendFeatureReport(device, [128, 11, 1, 2] + [2, 0, 245, 11, 0, 0, 60, 11, 170, 10, 6, 10, 20, 9, 245, 7, 81, 6, 193, 3], 24)
#         # SendFeatureReport(device, [128, 11, 1, 2] + [11] * 61, 64)


#         # my dualsense calibration
#         # SendFeatureReport(device, [128, 11, 1, 1] + [1, 12], 6)
#         # SendFeatureReport(device, [128, 11, 1, 2] + [2, 0, 245, 11, 0, 0, 86, 6, 239, 5, 115, 5, 220, 4, 54, 4, 145, 3, 141, 2, 112, 12], 24)
        
#         # SendFeatureReport(device, [128, 11, 1, 1] + [0, 0], 6)
#         # SendFeatureReport(device, [128, 11, 1, 2] + [0] * 60, 64)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 11, 2, 0] + [11] * 61, 64)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # Enable sine wave for testing
#         # neet to turn on speake with output report first
#         # SendFeatureReport(device, [128, 6, 4, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 23)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 6, 2, 1, 1, 0], 6)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 6, 2, 0, 1, 0], 6)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # tracebility info from my dualsense:
#         #[129, 7, 37, 2, 0, 32, 32, 8, 5, 9, 4, 68, 1, 1, 1, 121, 17, 2, 49, 0, 3, 112, 50, 78, 48, 54, 48, 52, 86, 49, 49, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 3, 2] + [0x65, 0x32, 0x40, 0x0C], 7)
#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 5, 2] + [0x65, 0x32, 0x40, 0x0C], 7)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 2, 1], 4)

#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 24, 1] + 24*[2], 27)

#         # for i in range(2, 18):
#         #     print(i)
#         #     SendFeatureReport(device, [128, 21, i, 1], 4)
#         #     time.sleep(0.2)
#         #     GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)
            
#         #     time.sleep(0.2)
#         #     SendFeatureReport(device, [130, 1, 1, 1], 4)
#         #     time.sleep(0.2)
#         #     GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)
#         #     time.sleep(0.2)
#         #     SendFeatureReport(device, [130, 3, 1, 1], 4)
#         #     time.sleep(0.2)
#         #     GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)
#         #     time.sleep(0.2)
#         #     SendFeatureReport(device, [130, 2], 2)
#         #     time.sleep(0.2)
#         #     GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 12, 1] + [11] * 30, 33)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 17, 1] + [11] * 30, 33)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 3, 0], 4)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 2, 0], 4)
#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 3, 1, 128], 4)
#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 3, 3, 0], 4)
#         # # time.sleep(0.2)
#         # # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         # # time.sleep(1.0)
#         # # SendFeatureReport(device, [128, 1, 1], 3)

#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 21, 17, 0] + 24*[0], 27)
#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 21, 2, 1] + 24*[0], 27)
#         # # time.sleep(0.2)
#         # # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [130, 1, 1, 1], 4)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [130, 3, 1, 1], 4)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [130, 2, 1, 1], 4)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)

#         # SendFeatureReport(device, [128, 12, 1] + 60*[11], 63)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 17] + 60*[11], 63)
#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 12, 1] + 24*[0], 27)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 6, 1] + 24*[0], 27)
#         # # time.sleep(0.2)
#         # # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         # # time.sleep(0.2)
#         # # SendFeatureReport(device, [128, 21, 49, 1] + 24*[0], 27)
#         # # time.sleep(0.2)
#         # # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 1] + 60*[11], 63)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 3, 1, 1], 4)
#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 3, 4, 1], 4)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         print("\n\nSaving changes to the device...")

#         # Save changes to the device
#         # SendFeatureReport(device, [128, 3, 1], 3)


#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 1] + 60*[11], 63)

#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 21, 5, 1], 4)
#         time.sleep(0.2)
#         GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 21, 3, 0], 4)
#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 21, 2, 0], 4)
#         time.sleep(0.2)
#         GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)
#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 21, 6, 1] + 24*[00], 27)
#         time.sleep(0.2)
#         GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # time.sleep(0.2)
#         # SendFeatureReport(device, [128, 21, 5, 1], 4)
#         # time.sleep(0.2)
#         # GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 12, 1] + 61 * [11], 64)
#         SendFeatureReport(device, [128, 21, 17, 0] + 60 * [11], 64)

#         time.sleep(0.2)
#         SendFeatureReport(device, [130, 1, 1, 1], 4)
#         time.sleep(0.2)
#         SendFeatureReport(device, [130, 3, 1, 1], 4)
#         time.sleep(0.2)
#         SendFeatureReport(device, [130, 2, 1, 1], 4)
#         time.sleep(0.2)
#         GetFeatureReport(device, 131, DevInfo.FeatureReportByteLength)

#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 21, 1] + 60*[11], 63)
#         time.sleep(0.2)
#         GetFeatureReport(device, 129, DevInfo.FeatureReportByteLength)

#         # Save changes to the device
#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 3, 1, 1], 4)
#         time.sleep(0.2)
#         SendFeatureReport(device, [128, 3, 4, 1], 4)

#     except Exception as e:
#         print("[ERROR] Could not complete the operation:", e)
#         pass
#     finally:
#         # Close the device if it was opened
#         try:
#             device.close()
#         except:
#             pass
#         print("[DEBUG] Device closed.")