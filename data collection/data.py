import serial
import csv
import time

# === CONFIG ===
port = "COM6"          # Windows example -> change to your ESP32 port
# port = "/dev/ttyUSB0"  # Linux/Mac example
baud = 115200

# Ask for filename
filename = input("Enter filename (without .csv): ") + ".csv"

# Serial connection
print(f"Connecting to {port} at {baud} baud...")
ser = serial.Serial(port, baud)
time.sleep(2)  # wait for ESP32 to reset

# Open CSV file
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)

    # Fixed header for 5 flex + 3 gyro
    writer.writerow(["flex1","flex2","flex3","flex4","flex5","gyroX","gyroY","gyroZ"])

    print(f"✅ Logging started: {filename}")
    print("Press Ctrl+C to stop...\n")

    try:
        while True:
            # Read a line from ESP32
            line = ser.readline().decode(errors="ignore").strip()
            data = line.split(",")

            # We expect exactly 8 values
            if len(data) == 8:
                writer.writerow(data)
                print(data)  # show live values

    except KeyboardInterrupt:
        print("\n🛑 Logging stopped. File saved:", filename)
