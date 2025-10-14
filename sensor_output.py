import matplotlib

matplotlib.use('TkAgg')  # Ensures the plot window stays open and responsive
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys
import threading
from queue import Queue
import time
import pyttsx3

# --- CONFIGURATION ---
SERIAL_PORT = 'COM4'  # Your Arduino's COM port
BAUD_RATE = 115200
MAX_RANGE_METERS = 10
PERSISTENCE_DURATION_SECONDS = 2.0  # How long the dot/peak stays after detection stops

# --- DATA QUEUE ---
data_queue = Queue()

# --- STATE TRACKING & TTS ---
was_previously_detected = False


def speak(text_to_speak):
    """
    Initializes a TTS engine and speaks the given text.
    Runs in a separate thread to avoid blocking the main plot.
    """
    try:
        engine = pyttsx3.init()
        engine.say(text_to_speak)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")


def serial_reader(port, baud, queue):
    """
    Function to run in a separate thread, continuously reading from the serial port.
    """
    print("Serial reader thread started.")
    try:
        with serial.Serial(port, baud, timeout=1) as ser:
            while True:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    queue.put(line)
    except serial.SerialException as e:
        print(f"FATAL: Serial Error on {port}: {e}")
        import os
        os._exit(1)
    print("Serial reader thread finished.")


# --- PLOT SETUP ---
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(1, 2, 1, projection='polar')
ax2 = fig.add_subplot(1, 2, 2)
mpu_text = fig.text(0.5, 0.02, 'Initializing...', ha='center', fontsize=12, color='white')
fig.tight_layout(rect=[0, 0.05, 1, 1])

# --- GLOBAL DATA HOLDERS ---
latest_data = {'detected': False}
last_detection_time = 0.0


def update(frame):
    """This function is called by the animation to redraw the plots."""
    global latest_data, last_detection_time, was_previously_detected

    # Process all available data from the queue
    while not data_queue.empty():
        line = data_queue.get_nowait()
        try:
            parts = line.split(',')
            if parts[0] == '1' and len(parts) == 7:
                latest_data = {
                    'detected': True, 'dist': float(parts[1]), 'energy': int(parts[3]),
                    'az': float(parts[6])
                }
                last_detection_time = time.time()
        except (ValueError, IndexError):
            pass

    # Determine the current detection state based on persistence
    is_currently_detected = False
    if latest_data['detected'] and (time.time() - last_detection_time <= PERSISTENCE_DURATION_SECONDS):
        is_currently_detected = True
    else:
        latest_data['detected'] = False  # Ensure the state is reset

    # --- AUDIO ALERT LOGIC (MODIFIED SECTION) ---
    # If a person is newly detected (state changed from False to True)
    if is_currently_detected and not was_previously_detected:
        # Create a detailed message with distance and energy
        distance = latest_data['dist']
        energy = latest_data['energy']
        message = f"Person detected at {distance:.1f} meters, with energy {energy}"

        print(f"EVENT: Triggering audio alert: '{message}'")

        # Start the speech in a non-blocking thread to avoid freezing the animation
        audio_thread = threading.Thread(target=speak, args=(message,), daemon=True)
        audio_thread.start()

    # Update the state for the next frame
    was_previously_detected = is_currently_detected

    # --- PLOTTING LOGIC ---
    ax1.clear()
    ax2.clear()

    if is_currently_detected:
        # --- Polar Plot ---
        theta = np.deg2rad(latest_data['az'])
        ax1.scatter([theta], [latest_data['dist']], c='lime', s=100)

        # --- Simulated Range Profile Logic ---
        x_range = np.linspace(0, MAX_RANGE_METERS, 200)
        y_energy_profile = np.random.rand(200) * 50
        target_index = np.argmin(np.abs(x_range - latest_data['dist']))
        y_energy_profile[target_index] = latest_data['energy']

        ax2.plot(x_range, y_energy_profile, color='deepskyblue')
        ax2.plot(latest_data['dist'], latest_data['energy'], 'o', color='orange')

        mpu_str = f"Target: {latest_data['dist']:.2f}m at {latest_data['az']:.1f}° | Energy: {latest_data['energy']}"
        mpu_text.set_text(mpu_str)
    else:
        mpu_text.set_text("Scanning... No person detected.")

    # --- Set plot limits and labels every frame ---
    ax1.set_title('X-Y Scatter Plot')
    ax1.set_ylim(0, MAX_RANGE_METERS)
    ax1.set_theta_zero_location('N')
    ax1.set_theta_direction(-1)
    ax1.set_yticklabels([])

    ax2.set_title('Range Profile')
    ax2.set_ylim(0, 100000)
    ax2.set_xlim(0, MAX_RANGE_METERS)
    ax2.set_xlabel('Range (meters)')
    ax2.set_ylabel('Energy')


# --- MAIN EXECUTION ---
if __name__ == '__main__':
    reader_thread = threading.Thread(target=serial_reader, args=(SERIAL_PORT, BAUD_RATE, data_queue), daemon=True)
    reader_thread.start()

    ani = animation.FuncAnimation(fig, update, interval=100, cache_frame_data=False)

    print("Starting visualization. Close the plot window to exit.")
    plt.show()

    print("Visualization finished.")