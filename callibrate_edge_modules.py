import time
import hid

VENDOR_ID = 0x054C
PRODUCT_ID_EDGE = 0x0DF2

########################################
# HID Device Initialization
########################################
def open_device():
    device = hid.device()
    
    try:
        device.open(VENDOR_ID, PRODUCT_ID_EDGE)
        print("Device opened successfully (DualSense Edge).")
        return device
    except Exception as e:
        print(f"[ERROR] Could not open device: {e}")

########################################
# Feature Report Handling with hidapi
########################################

def SendFeatureReport(device, data, length):
    if length > len(data):
        print("[ERROR] Length exceeds data array size.")
        return False

    out_data = bytes(data[:length])
    try:
        res = device.send_feature_report(out_data)
        if res == length:
            # Convert bytes to list of integers
            formatted_data = list(out_data) + [0] * (64 - len(out_data))
            # print(f"[DEBUG] Sent feature report successfully: {formatted_data}")
            return True
        else:
            print(f"[ERROR] Failed to send full feature report. Sent: {res}/{length}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception in SendFeatureReport: {e}")
        return False

def GetFeatureReport(device, report_id, length):
    try:
        report = device.get_feature_report(report_id, length)
        if len(report) > 0:
            # print(f"[DEBUG] Received feature report (len={len(report)}): {report}")
            return bytearray(report)
        else:
            print("[ERROR] Received empty report.")
            return None
    except Exception as e:
        print(f"[ERROR] Exception in GetFeatureReport: {e}")
        return None

########################################
if __name__ == "__main__":

    try:
        device = open_device()
        if device is None:
            print("[ERROR] No device found. Exiting.")
            exit(1)

        time.sleep(0.2)
        SendFeatureReport(device, [130, 1, 1, 1], 4)
        time.sleep(0.2)
        SendFeatureReport(device, [130, 3, 1, 1], 4)
        time.sleep(0.2)
        SendFeatureReport(device, [130, 2, 1, 1], 4)
        time.sleep(0.2)
        GetFeatureReport(device, 131, 64)

        time.sleep(0.2)
        SendFeatureReport(device, [128, 21, 5, 1], 4)
        time.sleep(0.2)
        GetFeatureReport(device, 129, 64)

        print("\nSaving changes to the devices (Edge Modules)")

        payload = [0, 11]
        
        print("\nUnlocking left module...")
        time.sleep(0.2)
        SendFeatureReport(device, [128, 21, 6, 0] + payload, len(payload) + 4)
        time.sleep(0.2)
        SendFeatureReport(device, [128, 21, 5, 0], 4)
        time.sleep(0.2)
        get_unlock_status_left = GetFeatureReport(device, 129, 64)
        if get_unlock_status_left[5] == 132:
            print("\nLeft module unlocked successfully.")
            print("\nSaving changes to the left edge modules complete!")
        else:
            print("\nLeft module unlock failed.")

        print("\nUnlocking right module...")    
        time.sleep(0.2)
        SendFeatureReport(device, [128, 21, 6, 1] + payload, len(payload) + 4)
        time.sleep(0.2)
        SendFeatureReport(device, [128, 21, 5, 1], 4)
        time.sleep(0.2)
        get_unlock_status_right = GetFeatureReport(device, 129, 64)
        time.sleep(0.2)
        if get_unlock_status_right[5] == 132:
            print("\nRight module unlocked successfully.")
            print("\nSaving changes to the right edge mdule complete!")
        else:
            print("\nRight module unlock failed.")


    except Exception as e:
        print("[ERROR] Could not complete the operation:", e)
        pass
    finally:
        try:
            device.close()
        except:
            pass
        # print("[DEBUG] Device closed.")