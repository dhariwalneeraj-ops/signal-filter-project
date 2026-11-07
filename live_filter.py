import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parameters
window_size = 5
n_steps = 60

# Data buffers for live plotting
x_data = []
raw_data = []
filtered_data = []

# Moving average buffer history
history = [0.0] * window_size

def update(frame):
    if frame >= n_steps:
        ani.event_source.stop()
        return

    # Simulate live incoming raw sensor data (with noise and occasional spikes)
    base = 10 + 2 * np.sin(frame * 0.2)
    noise = np.random.normal(0, 0.3)
    raw = base + noise
    
    if frame == 20:  # Inject a sudden spike
        raw += 15.0
    elif frame == 40:  # Inject a sudden drop
        raw -= 10.0

    # Update moving average filter buffer
    history.pop(0)
    history.append(raw)
    filtered = sum(history) / window_size

    # Append to plot lists
    x_data.append(frame)
    raw_data.append(raw)
    filtered_data.append(filtered)

    # Refresh plot lines
    line_raw.set_data(x_data, raw_data)
    line_filtered.set_data(x_data, filtered_data)
    
    # Adjust axis dynamically
    ax.set_xlim(0, max(15, frame + 2))
    return line_raw, line_filtered

# Set up the live plot window
fig, ax = plt.subplots(figsize=(10, 5))
line_raw, = ax.plot([], [], label='Live Raw Sensor Input', color='lightgray', marker='o', markersize=4)
line_filtered, = ax.plot([], [], label='Real-Time Filtered Output', color='royalblue', linewidth=2.5)

ax.set_ylim(0, 30)
ax.set_title('Real-Time DSP Signal Filter Simulation', fontsize=12, fontweight='bold')
ax.set_xlabel('Sample Step')
ax.set_ylabel('Amplitude')
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.6)

# Run animation loop (interval = 200 milliseconds per step)
ani = FuncAnimation(fig, update, frames=n_steps, interval=200, blit=False, repeat=False)

plt.show()