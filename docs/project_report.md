# Project Report: Real-Time Digital Signal Processing & Noise Filter Simulation

## Submitted by

- **Name:** Neeraj
- **Roll No.:** 123104020
- **Department:** Electrical Engineering
- **Institution:** National Institute of Technology, Kurukshetra

## Acknowledgement

I would like to express my sincere gratitude to the academic mentors and peers whose guidance and technical discussions supported the development of this project. The project provided an opportunity to connect programming and algorithm design with core electrical engineering concepts in digital signal processing.

## Abstract

This project implements a software-based moving-average low-pass FIR filter in C++. A synthetic sequence of sensor-like measurements, including ordinary fluctuations and illustrative transient disturbances, is passed through a fixed-window filter. The implementation combines a circular buffer with a running sum so each incoming sample can be processed in constant time, O(1), without shifting the buffer or recalculating the complete window. The program prints raw and filtered values for comparison. The buffer is allocated at initialization and is not resized during sample updates. The project demonstrates basic time-domain filtering, algorithmic optimization, and modular C++ implementation. No physical sensor acquisition or hardware real-time deadline testing is claimed.

## 1. Introduction

Measurements from sensors and electrical systems may contain noise, ripple, or abrupt disturbances. Digital filtering processes sampled data to reduce unwanted variations and make slower trends easier to observe. A moving-average filter is a simple finite impulse response (FIR) filter that averages a fixed number of recent samples.

### Objectives

1. Implement a moving-average FIR filter in C++.
2. Use a circular buffer to retain a fixed number of recent samples.
3. Use a running sum to reduce per-sample computation.
4. Compare synthetic raw measurements with filtered outputs.
5. Document the filter's behavior, complexity, assumptions, and limitations.

### Tools and technologies

- **Language:** C++17
- **Core concepts:** Digital signal processing, FIR filtering, circular buffers, running sums, object-oriented programming
- **Build tools:** GCC or another C++17 compiler; CMake (optional)
- **Input:** Synthetic sample values stored in a vector
- **Output:** Console table of raw and filtered samples

## 2. Theory

### 2.1 Moving-average FIR filter

For input \(x[n]\) and window size \(N\), the output is

\[
y[n] = \frac{1}{N}\sum_{k=0}^{N-1}x[n-k].
\]

This averages the current sample and the previous \(N-1\) samples. The filter is an FIR filter because its output is a finite weighted sum of present and past inputs and does not use previous outputs as feedback.

For this project, all coefficients are equal to \(1/N\). The filter smooths short-term fluctuations, but a larger window also increases response delay and can soften rapid genuine changes.

### 2.2 Running-sum optimization

Let \(S[n]\) be the sum of the current window. Once the window is full, the sum can be updated as

\[
S[n] = S[n-1] + x[n] - x[n-N].
\]

The output is

\[
y[n] = \frac{S[n]}{N}.
\]

The implementation achieves this update by subtracting the value stored at the current circular-buffer position, replacing it with the new sample, and adding the new sample to the running sum. This same update also works during startup because the buffer is initialized to zeros.

### 2.3 Circular buffer

A circular buffer is a fixed-size array whose index wraps to the beginning when it reaches the end:

```cpp
currentIndex = (currentIndex + 1) % windowSize;
```

It avoids shifting all elements after every sample. The buffer storage is allocated when the filter object is constructed and is not resized by `update()`.

### 2.4 Complexity

- **Time per update:** O(1), because each update performs a fixed number of arithmetic operations and index updates.
- **Storage:** O(N), because N samples are retained.
- **Construction:** O(N), to initialize the buffer.
- **Runtime allocation in update:** none from the buffer itself; the vector is created and sized in the constructor.

The algorithm is computationally efficient, but this simulation alone does not establish a hard real-time guarantee. Actual real-time behavior depends on the target platform, scheduling, I/O, and timing requirements.

## 3. System Design

### 3.1 Processing flow

```text
Synthetic raw samples
        |
        v
MovingAverageFilter::update(sample)
        |
        +--> Subtract outgoing sample
        |
        +--> Replace circular-buffer entry
        |
        +--> Add incoming sample to running sum
        |
        +--> Advance circular-buffer index
        |
        v
Divide running sum by window size
        |
        v
Print raw and filtered values
```

### 3.2 Software modules

- **`include/MovingAverageFilter.hpp`:** Declares the filter class, state variables, and public methods.
- **`src/MovingAverageFilter.cpp`:** Implements construction, sample updates, and reset behavior.
- **`src/main.cpp`:** Defines a synthetic sample stream and prints results.
- **`CMakeLists.txt`:** Defines a C++17 executable and compiler warning flags.
- **`README.md`:** Provides build and usage instructions.

### 3.3 Startup behavior

The buffer is initialized with zeros, and the output is always divided by N. Consequently, the first output is the first sample divided by N; subsequent startup outputs gradually incorporate more real samples. This fixed-denominator, zero-padded startup policy is simple and deterministic, but it initially biases the output toward zero. An alternative design could divide by the number of samples received until the buffer is full.

## 4. Test Input and Results

The program uses a window size of five and the following synthetic values:

```text
10.0, 10.2, 10.1, 10.5, 25.0,
10.3, 10.1, 9.9, 10.2, 5.0,
10.0, 10.1, 10.2, 10.0, 10.1
```

The values near 10 represent a nominal baseline. The values 25.0 and 5.0 are illustrative positive and negative disturbances. They are test values, not measurements from real hardware.

### 4.1 Expected console output

```text
========================================================
 Real-Time DSP Simulation: Moving Average FIR Filter
 Window size: 5 samples
========================================================
    Step       Raw Input     Filtered Output
--------------------------------------------------------
       1           10.00                2.00
       2           10.20                4.04
       3           10.10                6.06
       4           10.50                8.16
       5           25.00               13.16
       6           10.30               13.22
       7           10.10               13.20
       8            9.90               13.16
       9           10.20               13.10
      10            5.00                9.10
      11           10.00                9.04
      12           10.10                9.04
      13           10.20                9.10
      14           10.00                9.06
      15           10.10               10.08
========================================================
Note: startup outputs include zero-padded history.
```

### 4.2 Observations

1. **Startup transient:** The first few filtered values are lower than the input because zero-valued history is included in the average.
2. **Spike smoothing:** The 25.0 sample affects several consecutive outputs rather than appearing as a full-size jump in the filtered output.
3. **Recovery:** As the disturbed sample leaves the five-sample window, its influence disappears.
4. **Negative disturbance:** The 5.0 sample lowers the output over the following window, then its influence fades as later samples replace it.
5. **Trade-off:** Smoothing reduces rapid variations but introduces delay and does not distinguish noise from valid rapid signal changes.

These observations are based on the specified synthetic sequence. No quantitative noise-reduction percentage, measured execution time, or hardware benchmark is claimed.

## 5. Limitations and Future Improvements

- Test with recorded sensor data and compare noise statistics before and after filtering.
- Plot raw and filtered signals using MATLAB or Python.
- Compare window sizes to examine smoothing versus response delay.
- Add a startup policy that averages only samples received so far.
- Validate behavior for invalid configuration and unusual input values.
- If targeting embedded hardware, benchmark execution time and memory use on the actual platform.
- Compare the moving-average filter with other FIR designs or an IIR low-pass filter when system requirements justify it.

## 6. Conclusion

The project demonstrates a software-based moving-average FIR filter using C++ and a circular buffer. A running sum reduces the computation required for each sample to O(1), while buffer storage scales as O(N) with the selected window length. The synthetic test sequence illustrates smoothing and the temporary influence of abrupt disturbances. The work connects time-domain DSP fundamentals with efficient data handling and modular software design. Further validation with recorded signals and target hardware would be needed before making claims about a deployed real-time sensing system.

## References

1. Alan V. Oppenheim and Ronald W. Schafer, *Discrete-Time Signal Processing*, Pearson.
2. Bjarne Stroustrup, *The C++ Programming Language*, Addison-Wesley.
3. ISO C++ working draft and reference material for standard-library containers and algorithms: https://en.cppreference.com/
