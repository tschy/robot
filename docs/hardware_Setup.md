# Robotic Leg Project: Hardware Inventory & Setup

## 1. Hardware Inventory

### Core Control & Computing
- **Raspberry Pi 5**: Main controller for kinematics and logic.
- **PCA9685 16-Channel PWM Servo Driver**: PWM signal generator; isolates servos from RPi5 GPIO pins.
- **Raspberry Pi Connection Cable**: Connects RPi5 to the driver board.

### Actuation & Power
- **3x 9g Micro Servo Motors (4.8V)**: Hip and knee joint actuators.
- **Velleman Battery Box (4x AA)**: External power source for servos.
- **4x VOLTCRAFT NiMH Mignon-Akkus (1100 mAh)**: Rechargeable battery cells.
- **VOLTCRAFT VC-BC-4100 Charger**: Battery maintenance.

### Miscellaneous
- **Jumper Wires**: For I2C bus and power distribution.
- **Common Ground Wire**: Essential for stable logic reference between battery, driver, and Pi.

---

## 2. System Architecture



### Wiring Requirements
1. **I2C Bus**: Connect RPi5 `SDA`/`SCL` to PCA9685 `SDA`/`SCL`.
2. **Logic Power**: PCA9685 `VCC` connects to RPi5 `3.3V`.
3. **Servo Power**: Battery `V+` to PCA9685 `V+` terminal.
4. **Common Ground**: Connect Battery `GND`, PCA9685 `GND`, and RPi5 `GND` together.

---

## 3. RPi5 Setup Checklist

- [ ] **Enable I2C**: 
      Run `sudo raspi-config` -> `Interface Options` -> `I2C` -> `Enable`.
- [ ] **Install Libraries**: 
      ```bash
      pip3 install adafruit-circuitpython-pca9685 adafruit-circuitpython-servokit
      ```
- [ ] **Verify Connection**: 
      Run `i2cdetect -y 1`. Address `0x40` must be visible.

---

## 4. Safety Warnings
* **Power Isolation**: Never power servos directly from the RPi5 5V pin. Always use the external battery pack on the PCA9685 `V+` terminal.
* **Grounding**: Always ensure a common ground to prevent signal noise or damage to the RPi5.