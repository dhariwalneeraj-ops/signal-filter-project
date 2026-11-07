#include "MovingAverageFilter.hpp"

#include <algorithm>
#include <stdexcept>

MovingAverageFilter::MovingAverageFilter(std::size_t windowSize)
    : windowSize_(windowSize),
      buffer_(windowSize, 0.0),
      currentIndex_(0),
      runningSum_(0.0) {
    if (windowSize == 0) {
        throw std::invalid_argument("MovingAverageFilter window size must be greater than zero.");
    }
}

double MovingAverageFilter::update(double newSample) {
    // Remove the sample that is leaving the window.
    runningSum_ -= buffer_[currentIndex_];

    // Replace it with the newest sample and update the running sum.
    buffer_[currentIndex_] = newSample;
    runningSum_ += newSample;

    // Advance and wrap the index to implement a circular buffer.
    currentIndex_ = (currentIndex_ + 1) % windowSize_;

    return runningSum_ / static_cast<double>(windowSize_);
}

void MovingAverageFilter::reset() {
    std::fill(buffer_.begin(), buffer_.end(), 0.0);
    currentIndex_ = 0;
    runningSum_ = 0.0;
}
