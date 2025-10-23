# Search & Rescue (S&R) Radar System 📡

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A proof-of-concept system using an Arduino, mmWave radar, and an MPU6050 to detect the presence of humans in disaster scenarios. The system features a real-time Python visualization and audio alerts.

The goal of this project is to create a sensor package that could be mounted on a drone to help first responders quickly locate individuals trapped under rubble after an earthquake or other structural collapse.


---

## 🎯 Key Features

* **Human Detection:** Uses a DFRobot C4001 mmWave radar to detect human presence, even through obstacles.
* **Real-time Visualization:** A Python-based GUI displays target location on a polar plot and signal energy on a range profile graph.
* **Orientation Sensing:** An MPU6050 provides orientation data, which can be used to map detections in 3D space.
* **Audio Alerts:** The system uses text-to-speech to announce when a person is detected, providing their distance and signal strength.
* **Serial Communication:** Efficient, clean data transfer from the Arduino sensor hub to the Python visualization client.

---

## 🛠️ Hardware & Software Requirements

### Hardware Components
* **Microcontroller:** Arduino Uno (or any similar board)
* **Primary Sensor:** DFRobot C4001 mmWave Radar Sensor
* **Orientation Sensor:** MPU6050 6-Axis Gyroscope & Accelerometer
* Jumper Wires & Breadboard

### Software & Libraries
* [Arduino IDE](https://www.arduino.cc/en/software)
* Python 3.x
* **Arduino Libraries:**
    * `DFRobot_C4001`
    * `MPU6050_tockn`
    * `Wire`
    * `SoftwareSerial`
* **Python Libraries:**
    * `pyserial`
    * `matplotlib`
    * `numpy`
    * `pyttsx3`

---

## 🚀 Getting Started

Follow these steps to get the project running on your own hardware.

### 1. Hardware Setup

1.  **Wire the Components:** Connect the C4001 radar and MPU6050 sensor to your Arduino.
    * **C4001 Radar:**
        * `VCC` -> Arduino `5V`
        * `GND` -> Arduino `GND`
        * `TX` -> Arduino Pin `8` (SoftwareSerial RX)
        * `RX` -> Arduino Pin `9` (SoftwareSerial TX)
    * **MPU6050 Sensor:**
        * `VCC` -> Arduino `5V`
        * `GND` -> Arduino `GND`
        * `SCL` -> Arduino `A5`
        * `SDA` -> Arduino `A4`

2.  **Circuit Diagram:** See the complete wiring diagram below:

    ```
    Search & Rescue Radar System - Circuit Diagram
    ===============================================

    Arduino Uno Connections:
    ------------------------

                        Arduino Uno
                        ┌─────────────┐
                        │             │
                        │  ┌─────────┐│
                        │  │   USB   ││
                        │  └─────────┘│
                        │             │
                        │  ┌─────────┐│
                        │  │  Reset  ││
                        │  └─────────┘│
                        │             │
                        │  ┌─────────┐│
                        │  │   A5    ││ ←─── SCL (MPU6050)
                        │  └─────────┘│
                        │  ┌─────────┐│
                        │  │   A4    ││ ←─── SDA (MPU6050)
                        │  └─────────┘│
                        │             │
                        │  ┌─────────┐│
                        │  │   Pin 8 ││ ←─── TX (C4001 Radar)
                        │  └─────────┘│
                        │  ┌─────────┐│
                        │  │   Pin 9 ││ ←─── RX (C4001 Radar)
                        │  └─────────┘│
                        │             │
                        │  ┌─────────┐│
                        │  │   5V    ││ ←─── VCC (Both sensors)
                        │  └─────────┘│
                        │  ┌─────────┐│
                        │  │   GND   ││ ←─── GND (Both sensors)
                        │  └─────────┘│
                        │             │
                        └─────────────┘

    Component Connections:
    ----------------------

    1. DFRobot C4001 mmWave Radar:
       ┌─────────────────┐
       │   C4001 Radar   │
       │                 │
       │  VCC ───────────┼─── 5V (Arduino)
       │  GND ───────────┼─── GND (Arduino)
       │  TX  ───────────┼─── Pin 8 (Arduino)
       │  RX  ───────────┼─── Pin 9 (Arduino)
       └─────────────────┘

    2. MPU6050 6-Axis Sensor:
       ┌─────────────────┐
       │    MPU6050      │
       │                 │
       │  VCC ───────────┼─── 5V (Arduino)
       │  GND ───────────┼─── GND (Arduino)
       │  SCL ───────────┼─── A5 (Arduino)
       │  SDA ───────────┼─── A4 (Arduino)
       └─────────────────┘
    ```

    For a more detailed diagram, see [`circuit_diagram.txt`](circuit_diagram.txt) in the repository root.

### 2. Software Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/PrimalSky0019/Search-And-Rescue-Drone.git](https://github.com/PrimalSky0019/Search-And-Rescue-Drone.git)
    cd Search-And-Rescue-Drone
    ```

2.  **Install Python Dependencies:**
    ```bash
    pip install pyserial matplotlib numpy pyttsx3
    ```

3.  **Upload Arduino Code:**
    * Open `arduinocode.ino` in the Arduino IDE.
    * Install the required libraries from the Library Manager.
    * Select your board and COM port.
    * Click "Upload".

### 3. Running the System

1.  **Configure the COM Port:** Find your Arduino's serial port name (e.g., `COM4` on Windows or `/dev/ttyUSB0` on Linux).
2.  **Update the Python Script:** Open `sensor_output.py` and change the `SERIAL_PORT` variable to your port name.
    ```python
    # sensor_output.py
    SERIAL_PORT = 'COM4' # <-- CHANGE THIS
    ```
3.  **Launch the Visualizer:** Run the script from your terminal.
    ```bash
    python sensor_output.py
    ```
    A plot window should appear, and the system will start scanning for targets.

---

## 📊 Demo

Here is a sample of the Python visualization in action. The left plot shows the detected person's location (distance and angle), and the right plot shows the energy of the returned signal.

*(**This is the most important part!** Record a short GIF of your screen when the program is running and detecting you. You can use a free tool like [ScreenToGif](https://www.screentogif.com/) or GIPHY Capture. Then, just drag and drop the GIF file into the README editor on GitHub.)*

[Animation of the matplotlib plots detecting a person]

---

## 💡 How It Works

The system operates in two main parts:

1.  **Arduino Sensor Hub:** The Arduino continuously polls the C4001 radar and MPU6050. If the radar detects a target with a signal energy above a set threshold, the Arduino packages the distance, energy, and MPU orientation data into a simple comma-separated string (e.g., `1,5.2,850,0.5,-1.2,89.5`). It sends this string over the USB serial port. If no target is found, it sends a `0`.

2.  **Python Visualization Client:** A Python script on the host computer listens to the serial port. It runs two main threads:
    * **Serial Reader Thread:** Constantly reads data from the Arduino so the main application never freezes.
    * **Main Thread:** Parses the incoming data and uses Matplotlib to update the plots in real-time. If a new target is detected, it triggers a text-to-speech alert in a separate thread to avoid interrupting the visualization.

---

## 🗺️ Roadmap & Future Improvements

This is an early-stage prototype. Future enhancements could include:
* [ ] Integrating with a drone's flight controller (e.g., MAVLink).
* [ ] Creating a 3D map of detections instead of a 2D plot.
* [ ] Using a more robust GUI framework like PyQt or Tkinter.
* [ ] Implementing a logging system to save detection data.

Contributions and ideas are welcome!
