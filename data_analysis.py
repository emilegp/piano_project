import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

# Load the MATLAB data file
data = sio.loadmat('Sim1.mat')
sensor_data = data['sensor_data'].flatten()  # Flatten to ensure it's a 1D array

# Time array in milliseconds
time_array = np.linspace(0, len(sensor_data) * 5e-7 * 1e3, len(sensor_data))

# Plot the signal
plt.figure()
plt.plot(time_array, sensor_data)
plt.xlabel('Time [ms]')
plt.ylabel('Amplitude')
plt.title("Amplitude of the Signal")
plt.show()

# Calculate contrast
peak_value = np.max(sensor_data)
trough_value = np.min(sensor_data)
contrast = peak_value - trough_value

print(f"Peak Value: {peak_value}")
print(f"Trough Value: {trough_value}")
print(f"Contrast: {contrast}")

# chercher curve fit et largeur a mi-hauteur
