#pragma once

#include <cstddef>
#include <vector>

/**
 * @brief Fixed-window moving-average FIR filter.
 *
 * Uses a circular buffer and running sum to process each sample in O(1) time.
 * The buffer is allocated during construction and is not resized during update().
 *
 * Startup policy: the buffer is initialized with zeros, so the first windowSize-1
 * outputs include zero-valued history. This is a simple fixed-denominator policy.
 */
class MovingAverageFilter {
public:
    explicit MovingAverageFilter(std::size_t windowSize);

    /**
     * Insert a new sample and return the moving-average output.
     * @throws std::invalid_argument if the configured window size is zero
     */
    double update(double newSample);

    /// Clear the filter state; subsequent outputs again include zero-valued history.
    void reset();

    [[nodiscard]] std::size_t windowSize() const noexcept { return windowSize_; }

private:
    std::size_t windowSize_;
    std::vector<double> buffer_;
    std::size_t currentIndex_;
    double runningSum_;
};
