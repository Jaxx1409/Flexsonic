# predict_live.py
# Usage: python ml\predict_live.py COM3 115200
import sys, time, re, joblib
import serial
import numpy as np

if len(sys.argv) < 3:
    print("Usage: python predict_live.py <SERIAL_PORT> <BAUDRATE>")
    sys.exit(1)

port = sys.argv[1]
baud = int(sys.argv[2])

# Load models
scaler = joblib.load("models/scaler.pkl")
kmeans = joblib.load("models/kmeans.pkl")

pattern = re.compile(r"Thumb:\s*(-?\d+)\s*\|\s*Index:\s*(-?\d+)\s*\|\s*Middle:\s*(-?\d+)\s*\|\s*Ring:\s*(-?\d+)\s*\|\s*Pinky:\s*(-?\d+)")

with serial.Serial(port, baud, timeout=1) as ser:
    time.sleep(1)
    print("Listening on", port)
    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            m = pattern.search(line)
            if not m:
                continue
            vals = np.array([int(x) for x in m.groups()]).reshape(1,-1)
            vals_scaled = scaler.transform(vals)
            cluster = kmeans.predict(vals_scaled)[0]
            print(f"Cluster: {cluster}  | Raw: {vals.flatten().tolist()}")
    except KeyboardInterrupt:
        print("Stopped")
