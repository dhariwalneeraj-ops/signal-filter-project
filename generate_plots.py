import numpy as np
import matplotlib.pyplot as plt

# Set style for professional publication-ready figures
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=300)

# ==========================================
# SUBPLOT 1: C++ Simulation Discrete Results
# ==========================================
raw_cpp = [10.0, 10.2, 10.1, 10.5, 25.0, 10.3, 10.1, 9.9, 10.2, 5.0, 10.0, 10.1, 10.2, 10.0, 10.1]
window_size = 5
filtered_cpp = []
buf = [0.0] * window_size
running_sum = 0.0

for x in raw_cpp:
    running_sum -= buf[0]
    buf.pop(0)
    buf.append(x)
    running_sum += x
    filtered_cpp.append(running_sum / window_size)

steps = np.arange(1, len(raw_cpp) + 1)

# Plotting C++ Results
ax1.plot(steps, raw_cpp, color='#e74c3c', marker='o', markersize=6, linestyle='--', linewidth=1.5, alpha=0.85, label='Raw Sensor Input x[n]')
ax1.plot(steps, filtered_cpp, color='#2980b9', marker='s', markersize=6, linestyle='-', linewidth=2.5, label=f'Moving Average Output y[n] (N={window_size})')

# Annotations
ax1.annotate('Startup Phase\n(Zero-padded history)', xy=(2, filtered_cpp[1]), xytext=(2, 15),
             arrowprops=dict(facecolor='#7f8c8d', arrowstyle='->', lw=1.2),
             fontsize=9, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#ecf0f1", ec="#bdc3c7", lw=1))

ax1.annotate('Positive Spike Attenuation\n(25.0 -> 13.16)', xy=(5, raw_cpp[4]), xytext=(5.5, 23),
             arrowprops=dict(facecolor='#c0392b', arrowstyle='->', lw=1.2),
             fontsize=9, fontweight='bold', color='#c0392b', bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2e9", ec="#e67e22", lw=1))

ax1.annotate('Negative Disturbance Smoothed\n(5.0 -> 9.10)', xy=(10, raw_cpp[9]), xytext=(10.5, 4.0),
             arrowprops=dict(facecolor='#27ae60', arrowstyle='->', lw=1.2),
             fontsize=9, fontweight='bold', color='#27ae60', bbox=dict(boxstyle="round,pad=0.3", fc="#eafaf1", ec="#2ecc71", lw=1))

ax1.set_title('Part 1: C++ Simulation Output — Sample-by-Sample Response (Window N = 5)', fontsize=13, fontweight='bold', pad=12)
ax1.set_xlabel('Discrete Time Step (n)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Signal Amplitude', fontsize=11, fontweight='bold')
ax1.set_xticks(steps)
ax1.set_ylim(0, 28)
ax1.grid(True, linestyle=':', alpha=0.6, color='#95a5a6')
ax1.legend(loc='upper right', framealpha=0.95, facecolor='white', edgecolor='#bdc3c7', fontsize=10)


# ==========================================
# SUBPLOT 2: Continuous Sensor Stream Simulation
# ==========================================
np.random.seed(42)
n_stream = 70
t = np.arange(n_stream)

# Underlying true signal + Gaussian noise
true_signal = 10.0 + 3.0 * np.sin(t * 0.15)
noise = np.random.normal(0, 0.7, n_stream)
raw_stream = true_signal + noise

# Add sudden anomalous spikes
raw_stream[22] += 12.0
raw_stream[48] -= 8.0

# Apply FIR Filter
filtered_stream = []
stream_buf = [0.0] * window_size
s_sum = 0.0

for val in raw_stream:
    s_sum -= stream_buf[0]
    stream_buf.pop(0)
    stream_buf.append(val)
    s_sum += val
    filtered_stream.append(s_sum / window_size)

ax2.plot(t, true_signal, color='#27ae60', linestyle=':', linewidth=2.0, alpha=0.9, label='True Underlying Signal (Ideal)')
ax2.plot(t, raw_stream, color='#95a5a6', marker='.', markersize=5, linestyle='-', linewidth=1.0, alpha=0.7, label='Noisy Sensor Signal + Transient Anomalies')
ax2.plot(t, filtered_stream, color='#1f77b4', linestyle='-', linewidth=2.8, label=f'Real-Time Filtered Signal (N={window_size})')

# Annotate spike smoothing
ax2.annotate('Transient Spike Suppressed', xy=(22, raw_stream[22]), xytext=(24, 21),
             arrowprops=dict(facecolor='#e74c3c', arrowstyle='->', lw=1.2),
             fontsize=9, fontweight='bold', color='#c0392b', bbox=dict(boxstyle="round,pad=0.3", fc="#fdf2e9", ec="#e74c3c", lw=1))

ax2.annotate('Sensor Drop Smoothed', xy=(48, raw_stream[48]), xytext=(49, 1.5),
             arrowprops=dict(facecolor='#2980b9', arrowstyle='->', lw=1.2),
             fontsize=9, fontweight='bold', color='#2980b9', bbox=dict(boxstyle="round,pad=0.3", fc="#ebf5fb", ec="#3498db", lw=1))

ax2.set_title('Part 2: Dynamic Continuous Noise Filtering Simulation', fontsize=13, fontweight='bold', pad=12)
ax2.set_xlabel('Sample Index (t)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Amplitude', fontsize=11, fontweight='bold')
ax2.set_ylim(-1, 26)
ax2.grid(True, linestyle=':', alpha=0.6, color='#95a5a6')
ax2.legend(loc='upper right', framealpha=0.95, facecolor='white', edgecolor='#bdc3c7', fontsize=10)

plt.tight_layout(pad=3.0)
output_path = 'assets/simulation_results.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Successfully generated {output_path}")
