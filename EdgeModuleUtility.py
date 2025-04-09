#!/usr/bin/env python
import time
import hid

VENDOR_ID = 0x054C
PRODUCT_ID_EDGE = 0x0DF2

def print_disclaimer():
    print("########################################")
    print("# Script Author: lewy20041 / Driftguard")
    print("# Disclaimer:")
    print("# This script is provided as-is without any warranty.")
    print("# Use at your own risk. The author is not responsible")
    print("# for any damage or unintended side effects caused")
    print("# by using this script.")
    print("########################################\n")

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
        return None

########################################
# Feature Report Handling with hidapi
########################################
def send_feature_report(device, data, length):
    if device is None:
        print("[ERROR] No device connection.")
        return False
        
    if length > len(data):
        print("[ERROR] Length exceeds data array size.")
        return False

    out_data = bytes(data[:length])
    try:
        res = device.send_feature_report(out_data)
        if res == length:
            # Optionally format data for debugging
            formatted_data = list(out_data) + [0] * (64 - len(out_data))
            # print(f"[DEBUG] Sent feature report successfully: {formatted_data}")
            return True
        else:
            print(f"[ERROR] Failed to send full feature report. Sent: {res}/{length}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception in send_feature_report: {e}")
        return False

def get_feature_report(device, report_id, length):
    if device is None:
        print("[ERROR] No device connection.")
        return None
        
    try:
        report = device.get_feature_report(report_id, length)
        if len(report) > 0:
            # print(f"[DEBUG] Received feature report (len={len(report)}): {report}")
            return bytearray(report)
        else:
            print("[ERROR] Received empty report.")
            return None
    except Exception as e:
        print(f"[ERROR] Exception in get_feature_report: {e}")
        return None

########################################
# Device Status Functions
########################################
def check_module_status(device):
    """Check the status of both left and right modules"""
    if device is None:
        return None, None
    
    try:
        # Query left module status
        send_feature_report(device, [128, 21, 5, 0], 4)
        time.sleep(0.2)
        left_status_report = get_feature_report(device, 129, 64)
        
        # Query right module status
        send_feature_report(device, [128, 21, 5, 1], 4)
        time.sleep(0.2)
        right_status_report = get_feature_report(device, 129, 64)
        
        left_status = left_status_report[5] if left_status_report and len(left_status_report) > 5 else None
        right_status = right_status_report[5] if right_status_report and len(right_status_report) > 5 else None
        
        return left_status, right_status
    except Exception as e:
        print(f"[ERROR] Exception in check_module_status: {e}")
        return None, None

def get_module_status_text(status_code):
    """Convert module status code to readable text"""
    if status_code == 132:
        return "UNLOCKED"
    elif status_code == 140:
        return "LOCKED"
    else:
        return "UNKNOWN"

########################################
# Device Operation Functions
########################################
def ensure_device_connection(device):
    """Ensure the device is connected, attempting to reconnect if necessary."""
    if device is None:
        print("\nNo device connection. Attempting to connect...")
        return open_device()
    
    # Try a simple command to check if the device is still responsive
    try:
        device.get_feature_report(129, 64)
        return device
    except Exception:
        print("\nDevice connection lost. Attempting to reconnect...")
        try:
            device.close()
        except Exception:
            pass
        return open_device()

def calibrate_center_point(device):
    device = ensure_device_connection(device)
    if device is None:
        print("[ERROR] Cannot calibrate: No device connection.")
        return device
        
    # Recalibrate sticks center point using the provided sequence
    print("\nCalibrating sticks center point...")
    time.sleep(0.2)
    send_feature_report(device, [130, 1, 1, 1], 4)
    time.sleep(0.2)
    send_feature_report(device, [130, 3, 1, 1], 4)
    time.sleep(0.2)
    send_feature_report(device, [130, 2, 1, 1], 4)
    time.sleep(0.2)
    report = get_feature_report(device, 131, 64)
    if report:
        print("Sticks center point calibrated successfully.")
    else:
        print("Calibration of sticks center point failed.")
    
    return device

def unlock_modules(device):
    device = ensure_device_connection(device)
    if device is None:
        print("[ERROR] Cannot unlock: No device connection.")
        return device
    
    print("\nSometimes you need to run this option twice to unlock the modules.")
    print("If modules are still locked, please try again.")
    # Unlock Left Module
    print("\nUnlocking left module...")
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 6, 0, 11], 5)
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 5, 0], 4)
    time.sleep(1.0)
    status_left = get_feature_report(device, 129, 64)
    if status_left and len(status_left) > 5 and status_left[5] == 132:
        print("Left module unlocked successfully.")
        print("Saving changes to the left edge module complete!")
    else:
        print("Left module unlock failed.")

    # Unlock Right Module
    print("\nUnlocking right module...")
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 6, 1, 11], 5)
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 5, 1], 4)
    time.sleep(1.0)
    status_right = get_feature_report(device, 129, 64)
    if status_right and len(status_right) > 5 and status_right[5] == 132:
        print("Right module unlocked successfully.")
        print("Saving changes to the right edge module complete!")
    else:
        print("Right module unlock failed.")
    
    return device

def lock_modules(device):
    device = ensure_device_connection(device)
    if device is None:
        print("[ERROR] Cannot lock: No device connection.")
        return device
        
    # Lock Left Module
    print("\nLocking left module...")
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 4, 0, 8], 5)
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 5, 0], 4)
    time.sleep(0.2)
    status_left = get_feature_report(device, 129, 64)
    if status_left and len(status_left) > 5 and status_left[5] == 140:
        print("Left module locked successfully.")
        print("Saving changes to the left edge module complete!")
    else:
        print("Left module lock failed.")

    # Lock Right Module
    print("\nLocking right module...")
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 4, 1, 8], 5)
    time.sleep(0.2)
    send_feature_report(device, [128, 21, 5, 1], 4)
    time.sleep(0.2)
    status_right = get_feature_report(device, 129, 64)
    time.sleep(0.2)
    if status_right and len(status_right) > 5 and status_right[5] == 140:
        print("Right module locked successfully.")
        print("Saving changes to the right edge module complete!")
    else:
        print("Right module lock failed.")
    
    return device

def backup_calibration_values(device):
    device = ensure_device_connection(device)
    if device is None:
        print("[ERROR] Cannot backup: No device connection.")
        return device
        
    print("\nBacking up default modules calibration values...")
    # Retrieve the calibration values (assuming they are available at report_id=131)
    send_feature_report(device, [128, 12, 2], 3)
    time.sleep(0.2)
    report = get_feature_report(device, 129, 64)
    if report:
        filename = "default_calibration_backup.bin"
        try:
            with open(filename, "wb") as f:
                f.write(report)
            print(f"Calibration values backed up successfully to '{filename}'.")
        except Exception as e:
            print(f"[ERROR] Could not write calibration backup to file: {e}")
    else:
        print("Failed to retrieve calibration values for backup.")
    
    return device

def display_menu_with_status(device):
    """Display menu with current module status"""
    # Check module status
    left_status, right_status = check_module_status(device)
    
    # Convert to readable text
    left_status_text = get_module_status_text(left_status)
    right_status_text = get_module_status_text(right_status)
    
    # Print header with status
    print("\n==== DualSense Edge Controller Status ====")
    if device is None:
        print("Controller Status: DISCONNECTED")
    else:
        print("Controller Status: CONNECTED")
        print(f"Left Module:  {left_status_text}")
        print(f"Right Module: {right_status_text}")
    print("=========================================")
    
    # Print menu options
    print("\nPlease select an option:")
    print("1. Unlock DualSense Edge Modules")
    print("2. Lock DualSense Edge Modules")
    print("3. Calibrate DualSense Edge Modules Center Point")
    print("4. Back Up Default Modules Calibration Values to a File")
    print("5. Exit")
    return input("Enter your choice (1/2/3/4/5): ").strip()

########################################
# Main Script Execution
########################################
if __name__ == "__main__":
    print_disclaimer()  # Display the disclaimer at the start
    
    device = None
    
    try:
        # Initial device connection attempt
        device = open_device()
        if device is None:
            print("[WARNING] No device found initially. The script will attempt to connect when an operation is selected.")
        
        while True:
            # Check device connection before displaying menu
            device = ensure_device_connection(device)
            
            choice = display_menu_with_status(device)

            if choice == "1":
                device = unlock_modules(device)
                input("\nPress Enter to return to the menu...")
            elif choice == "2":
                device = lock_modules(device)
                input("\nPress Enter to return to the menu...")
            elif choice == "3":
                device = calibrate_center_point(device)
                input("\nPress Enter to return to the menu...")
            elif choice == "4":
                device = backup_calibration_values(device)
                input("\nPress Enter to return to the menu...")
            elif choice == "5":
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print("[ERROR] Could not complete the operation:", e)
    finally:
        try:
            if device:
                device.close()
                print("Device closed.")
        except Exception:
            pass