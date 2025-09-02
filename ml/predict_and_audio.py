import serial
import joblib
import numpy as np
import pandas as pd

# 1. Load trained clustering model
kmeans = joblib.load("models/gesture_clusters.pkl")

# 2. Serial connection to ESP32 (adjust COM port/baudrate for your system)
ser = serial.Serial("COM3", 115200, timeout=1)  # Windows -> COMx | Linux/Mac -> "/dev/ttyUSB0"

# 3. Define mapping: cluster → audio index (MP3 files on DFPlayer Mini)
cluster_to_audio = {
    0: 1,  # Cluster 0 plays 0001.mp3
    1: 2,  # Cluster 1 plays 0002.mp3
    2: 3,  # Cluster 2 plays 0003.mp3
    # add more if you have more clusters
}

print("✅ System ready. Listening for gesture data...")

while True:
    try:
        # 4. Read one line of sensor data from ESP32
        line = ser.readline().decode("utf-8").strip()
        if not line:
            continue

        # Example incoming format: "512,600,300,450,700, -0.05, 0.12, 9.80"
        values = [float(x) for x in line.split(",")]

        # Convert to NumPy array
        X_new = np.array(values).reshape(1, -1)

        # 5. Predict cluster
        cluster = kmeans.predict(X_new)[0]
        print(f"👉 Gesture detected: Cluster {cluster}")

        # 6. Map to audio
        if cluster in cluster_to_audio:
            audio_index = cluster_to_audio[cluster]
            cmd = f"PLAY:{audio_index}\n"
            ser.write(cmd.encode("utf-8"))
            print(f"🎵 Playing audio {audio_index} for cluster {cluster}")

    except Exception as e:
        print("⚠️ Error:", e)
