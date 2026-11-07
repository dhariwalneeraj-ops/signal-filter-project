# Real-Time Digital Signal Processing & Noise Filter Simulation

**Department:** Electrical Engineering  
**Institution:** National Institute of Technology, Kurukshetra  
**Project type:** Software-based DSP simulation  
**Language:** C++17

## Overview

This project simulates a discrete-time, low-pass moving-average FIR filter. It processes a stream of sample values representing a noisy sensor signal and produces a smoothed output. A fixed-size circular buffer stores recent samples, while a running sum avoids recalculating the entire window for every new sample.

The sample stream is synthetic and intended for demonstration; it is not captured from physical hardware.

## Features

- Moving-average finite impulse response (FIR) filter.
- Circular-buffer indexing with a fixed-size buffer.
- Running-sum update for **O(1) time per sample**.
- Object-oriented class with `update()` and `reset()` methods.
- Console comparison of raw and filtered samples.
- CMake build configuration and a detailed project report.

## Directory layout

```text
signal-filter-project/
├── include/
│   └── MovingAverageFilter.hpp
├── src/
│   ├── MovingAverageFilter.cpp
│   └── main.cpp
├── docs/
│   └── project_report.md
├── CMakeLists.txt
└── README.md
```

## Requirements

- A C++17-compatible compiler (GCC, Clang, or MSVC).
- CMake 3.16 or later (optional if compiling directly).

## Build and run

### Option A: Compile directly with GCC

Run from the project root:

```bash
g++ -std=c++17 -Wall -Wextra -Wpedantic -Iinclude src/main.cpp src/MovingAverageFilter.cpp -o signal_filter
./signal_filter
```

On Windows with MinGW, run `signal_filter.exe` instead of `./signal_filter`.

### Option B: Use CMake

```bash
cmake -S . -B build
cmake --build build
```

Run the executable:
- Linux/macOS: `./build/signal_filter`
- Windows: `build\\Debug\\signal_filter.exe` for a typical Visual Studio generator, or the corresponding path under `build\\Release`.

## Algorithm

For window length \(N\), the moving average is

\[
y[n] = \\frac{1}{N}\\sum_{k=0}^{N-1}x[n-k].
\]

The implementation maintains the sum of the window. For each new sample, it subtracts the outgoing sample, inserts the new sample, and adds it to the sum. It then divides by \(N\).

- **Time complexity:** O(1) per sample.
- **Space complexity:** O(N) for the buffer.
- **Runtime allocations:** the buffer is allocated during construction and is not resized in `update()`.

The project uses zero-initialized buffer values during startup. Therefore, the first \(N-1\) outputs are divided by the full window length and include zero-valued history. This startup behavior is intentional and documented in the code.

## Important interpretation

A moving-average filter smooths rapid changes, but it does not identify whether a spike is noise or a genuine event. It can attenuate a short disturbance while also delaying changes in the underlying signal. Filter window length controls the trade-off between smoothing and response delay.

## Author details

- **Name:** Neeraj
- **Roll number:** 123104020
- **Department:** Electrical Engineering
- **Institution:** National Institute of Technology, Kurukshetra

Update personal or institutional details if this project is reused in another context.
