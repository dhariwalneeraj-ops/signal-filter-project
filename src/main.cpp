#include "MovingAverageFilter.hpp"

#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    constexpr std::size_t windowSize = 5;

    // Simulated sensor measurements around a nominal baseline of 10 units.
    // The values 25.0 and 5.0 represent illustrative transient disturbances.
    const std::vector<double> rawSignal = {
        10.0, 10.2, 10.1, 10.5, 25.0,
        10.3, 10.1, 9.9, 10.2, 5.0,
        10.0, 10.1, 10.2, 10.0, 10.1
    };

    MovingAverageFilter filter(windowSize);

    std::cout << "========================================================\n";
    std::cout << " Real-Time DSP Simulation: Moving Average FIR Filter\n";
    std::cout << " Window size: " << windowSize << " samples\n";
    std::cout << "========================================================\n";
    std::cout << std::right << std::setw(8) << "Step"
              << std::setw(16) << "Raw Input"
              << std::setw(20) << "Filtered Output" << '\n';
    std::cout << "--------------------------------------------------------\n";

    for (std::size_t i = 0; i < rawSignal.size(); ++i) {
        const double raw = rawSignal[i];
        const double filtered = filter.update(raw);

        std::cout << std::setw(8) << (i + 1)
                  << std::setw(16) << std::fixed << std::setprecision(2) << raw
                  << std::setw(20) << std::fixed << std::setprecision(2) << filtered
                  << '\n';
    }

    std::cout << "========================================================\n";
    std::cout << "Note: startup outputs include zero-padded history.\n";
    return 0;
}
