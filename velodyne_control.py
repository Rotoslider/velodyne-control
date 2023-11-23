import pycurl
from io import BytesIO
from urllib.parse import urlencode
import json
import time
import tkinter as tk
from tkinter import messagebox

def sensor_do(s, url, pf):
    buffer = BytesIO()
    s.setopt(s.URL, url)
    s.setopt(s.POSTFIELDS, pf)
    s.setopt(s.WRITEDATA, buffer)
    s.perform()
    rcode = s.getinfo(s.RESPONSE_CODE)
    success = rcode in range(200, 207)
    response = buffer.getvalue().decode()
    print('%s %s: %d (%s)' % (url, pf, rcode, 'OK' if success else 'ERROR'))
    return success, response

def control_lidar(rpm):
    Base_URL = 'http://192.168.1.201/cgi/'
    sensor = pycurl.Curl()

    # Set laser and RPM
    if rpm > 0:
        laser_state = 'on'
    else:
        laser_state = 'off'
        
    # Set sensor parameters
    #rc, _ = sensor_do(sensor, Base_URL+'setting', urlencode({'rpm': str(rpm)}))
    rc, _ = sensor_do(sensor, Base_URL+'setting', urlencode({'laser': laser_state}))
    if rc:
        rc, _ = sensor_do(sensor, Base_URL+'setting', urlencode({'rpm': str(rpm)}))
        if rc:
            messagebox.showinfo("Success", f"LiDAR is set to {rpm} RPM with laser {laser_state}")
        else:
            messagebox.showerror("Error", "Failed to set LiDAR RPM")
            
    else:
        messagebox.showerror("Error", "Failed to set LiDAR Laser")

    sensor.close()

# Tkinter GUI setup
def create_gui():
    root = tk.Tk()
    root.title("LiDAR Control")

    start_button = tk.Button(root, text="Start LiDAR", command=lambda: control_lidar(600))
    stop_button = tk.Button(root, text="Stop LiDAR", command=lambda: control_lidar(0))

    start_button.pack(pady=10)
    stop_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
