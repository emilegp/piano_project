import threading
import time
import random
from collections import deque

# Function to simulate piezoelectric sensor readings
def read_sensor_data(buffer, pre_points, post_points, threshold):
    post_impulse_data_needed = 0  # Counter to track how many post-impulse points to capture
    
    while True:
        # Simulate reading from the piezoelectric sensor (replace with actual sensor code)
        signal = random.uniform(0, 1)  # Simulating sensor reading
        buffer.append(signal)  # Add current signal to the rolling buffer

        # Check if we are capturing post-impulse data
        if post_impulse_data_needed > 0:
            post_impulse_data_needed -= 1  # Decrease the count of needed post-impulse data
            if post_impulse_data_needed == 0:
                print("Finished capturing post-impulse data")
                print(f"Captured signal: {list(buffer)}")
                process_signal(list(buffer))
        
        # Detect impulse (if not already capturing post-impulse data)
        elif signal > threshold:
            print(f"Impulse detected with signal: {signal}")
            post_impulse_data_needed = post_points  # Set how many points to capture after impulse
            print("Capturing post-impulse data...")

        time.sleep(0.05)  # Simulate sensor read delay (adjust based on your sensor's sampling rate)

# Function to process the signal after the full buffer is captured
def process_signal(signal):
    print(f"Processing captured signal of length {len(signal)}")
    # Placeholder for signal processing logic (e.g., comparing with prerecorded signals)
    pass

# Parameters for buffer size
pre_points = 50  # Number of data points to store before the impulse
post_points = 50  # Number of data points to capture after the impulse
threshold = 0.9  # Impulse detection threshold

# Create a circular buffer to hold pre- and post-impulse data (total buffer size = pre_points + post_points)
buffer = deque(maxlen=pre_points + post_points)

# Start a thread to continuously read sensor data
sensor_thread = threading.Thread(target=read_sensor_data, args=(buffer, pre_points, post_points, threshold))
sensor_thread.start()

# Main program (could perform other tasks while sensor data is being read)
while True:
    print("Main program running...")
    time.sleep(2)
