import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random
from collections import deque

# Anomaly Detector using Z-Score method
class ZScoreAnomalyDetector:
    """
    A class for detecting anomalies in a real-time data stream using a Z-Score-based method.
    The detector maintains a rolling window of data points and dynamically adjusts thresholds to detect anomalies.
    
    Attributes:
    window_size (int): Number of data points to keep in the rolling window.
    base_threshold (float): The base threshold for detecting anomalies (Z-Score limit).
    anomaly_hold (int): The number of steps to hold an anomaly state after detection.
    reset_step (float): The rate at which the threshold resets after a non-anomaly period.
    early_stop_threshold (float): Small deviation threshold for stopping further calculations.
    max_threshold (float): Maximum threshold to limit detection sensitivity.
    """
    
    def __init__(self, window_size=50, base_threshold=2.5, anomaly_hold=2.0, reset_step=0.1, early_stop_threshold=0.5):
        """
        Initialize the anomaly detector with default or provided values.
        
        Parameters:
        window_size (int): Size of the rolling window for recent data points.
        base_threshold (float): The starting Z-Score threshold for anomaly detection.
        anomaly_hold (int): Duration to hold the anomaly status once detected.
        reset_step (float): Speed at which the detection threshold is reset after normal data is seen.
        early_stop_threshold (float): Minimal deviation threshold to avoid unnecessary Z-Score calculations.
        """
        self.window_size = window_size
        self.base_threshold = base_threshold
        self.current_threshold = base_threshold
        self.data_stream = deque(maxlen=window_size)
        self.anomaly_hold = anomaly_hold
        self.anomaly_buffer = 0
        self.reset_step = reset_step
        self.no_anomaly_counter = 0
        self.mean = 0
        self.squared_diff_sum = 0
        self.count = 0
        self.max_threshold = 4  # Max limit for threshold
        self.early_stop_threshold = early_stop_threshold  # Threshold for early stopping

    def add_data_point(self, value, is_anomaly=False):
        """
        Add a new data point to the rolling window and update statistics.
        
        Parameters:
        value (float): The new data point to be added.
        is_anomaly (bool): Flag to indicate if the current point is an anomaly (used for threshold adjustments).
        """
        if is_anomaly:
            self.anomaly_buffer = self.anomaly_hold
            self.current_threshold = min(max(self.base_threshold, self.current_threshold + 0.5), self.max_threshold)
        else:
            self.no_anomaly_counter += 1

        # Reset threshold faster after several normal points
        if self.no_anomaly_counter > 3 and self.current_threshold > self.base_threshold:
            self.current_threshold -= self.reset_step * 2  # Faster reset after normal points
            self.no_anomaly_counter = 0

        # Update statistics and maintain rolling window
        if not is_anomaly or self.anomaly_buffer > 0:
            self.update_statistics(value)
            self.data_stream.append(value)
            if self.anomaly_buffer > 0:
                self.anomaly_buffer -= 1

    def update_statistics(self, new_value):
        """
        Efficiently update the rolling mean and standard deviation with a new value.
        This prevents recalculating statistics for the entire window on each update.
        
        Parameters:
        new_value (float): The new value to be included in the rolling statistics.
        """
        if len(self.data_stream) == self.window_size:
            # Remove the oldest value and adjust the mean and standard deviation accordingly
            old_value = self.data_stream[0]  
            self.count -= 1
            if self.count > 0:
                old_mean = self.mean
                self.mean = (self.mean * (self.count + 1) - old_value) / self.count
                self.squared_diff_sum -= (old_value - old_mean) ** 2

        # Update mean and squared differences incrementally
        self.count += 1
        delta = new_value - self.mean
        self.mean += delta / self.count
        self.squared_diff_sum += delta * (new_value - self.mean)

    def get_std_dev(self):
        """
        Calculate and return the standard deviation for the current rolling window.
        
        Returns:
        float: Standard deviation of the data in the current window.
        """
        if self.count < 2:
            return float('nan')  # Not enough data to calculate standard deviation
        if self.squared_diff_sum < 0:
            return float('nan')  # Inconsistent state; avoid negative values in the variance
        return (self.squared_diff_sum / self.count) ** 0.5

    def is_anomaly(self):
        """
        Check if the latest data point is an anomaly based on the Z-Score.
        
        Returns:
        bool: True if the latest data point is an anomaly, False otherwise.
        """
        if len(self.data_stream) < self.window_size:
            return False

        std_dev = self.get_std_dev()
        if std_dev == 0:
            return False

        # Early stopping for small deviations
        deviation = abs(self.data_stream[-1] - self.mean)
        if deviation < self.early_stop_threshold:
            return False

        z_score = deviation / std_dev
        return z_score > self.current_threshold


# Modular system to handle anomaly detection
class AnomalyDetectionSystem:
    """
    A modular framework to manage anomaly detection using the ZScoreAnomalyDetector.
    """

    def __init__(self, **kwargs):
        """
        Initialize the system with specified parameters for the ZScoreAnomalyDetector.
        
        Parameters:
        kwargs: Arguments to be passed to the ZScoreAnomalyDetector for custom configuration.
        """
        self.detector = ZScoreAnomalyDetector(**kwargs)

    def add_data_point(self, value):
        """
        Add a data point to the anomaly detector.
        
        Parameters:
        value (float): The data point to be analyzed.
        """
        self.detector.add_data_point(value)

    def is_anomaly(self):
        """
        Determine if the most recent data point is an anomaly.
        
        Returns:
        bool: True if the data point is an anomaly, False otherwise.
        """
        return self.detector.is_anomaly()


# Function to simulate a continuous data stream with seasonality, drift, and noise
def enhanced_data_stream_generator(noise_level=0.5, seasonality_period=50, drift_rate=0.001, anomaly_chance=0.05):
    """
    Generator function to simulate a real-time data stream with seasonal patterns, random noise, drift, and anomalies.
    
    Parameters:
    noise_level (float): The level of random noise to add to each data point.
    seasonality_period (int): Number of steps for one cycle of seasonality.
    drift_rate (float): The rate at which the data gradually shifts (concept drift).
    anomaly_chance (float): The probability of an anomaly occurring at any given step.
    
    Yields:
    float: The next value in the simulated data stream.
    """
    time = 0
    drift = 0
    while True:
        seasonal_pattern = math.sin(2 * math.pi * time / seasonality_period)  # Simulate seasonality with sine wave
        noise = random.uniform(-noise_level, noise_level)  # Add random noise
        drift += drift_rate  # Gradual shift in data
        if random.random() < anomaly_chance:  # Randomly inject anomalies
            anomaly = random.choice([5, -5])
        else:
            anomaly = 0
        yield seasonal_pattern + noise + drift + anomaly  # Generate final data point
        time += 1


# Real-Time Anomaly Detection and Visualization
def run_real_time_anomaly_detection(initial_data_points=100):
    """
    Function to run real-time anomaly detection with dynamic visualization using Matplotlib.
    
    Parameters:
    initial_data_points (int): Number of initial data points to collect before starting the visualization.
    """
    # Initialize the detector system
    detector = AnomalyDetectionSystem(window_size=70, base_threshold=2.0, anomaly_hold=1, reset_step=0.1, early_stop_threshold=0.1)
    
    # Set up the figure and axis for plotting
    fig, ax = plt.subplots()
    data_stream = []
    anomalies = []
    stream = enhanced_data_stream_generator()

    # Collect initial data points without plotting
    for _ in range(initial_data_points):
        new_value = next(stream)
        data_stream.append(new_value)
        detector.add_data_point(new_value)  # Add to detector but don't plot yet

    # Function to update the plot in real time
    def update_plot(frame):
        new_value = next(stream)
        data_stream.append(new_value)

        # Add data point to detector
        detector.add_data_point(new_value)

        # Detect anomaly
        is_anomaly = detector.is_anomaly()
        if is_anomaly:
            anomalies.append(len(data_stream) - 1)  # Mark anomaly index

        # Clear the plot
        ax.clear()

        # Plot data points and anomalies
        if len(data_stream) > initial_data_points:
            adjusted_x_values = list(range(len(data_stream) - initial_data_points))
            ax.plot(adjusted_x_values, data_stream[initial_data_points:], label='Data Stream', color='blue')

            # Highlight detected anomalies
            if anomalies:
                adjusted_anomalies = [i - initial_data_points for i in anomalies if i >= initial_data_points]
                ax.scatter(adjusted_anomalies, [data_stream[i] for i in anomalies if i >= initial_data_points], color='red', label='Anomalies')

        # Set plot labels and title
        ax.set_title('Real-Time Data Stream with Anomaly Detection')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.legend(loc='upper left')

        # Set x-axis to start from 0
        ax.set_xlim(left=0)

    # Set up the animation for real-time updates
    ani = animation.FuncAnimation(fig, update_plot, interval=100, cache_frame_data=False)

    # Display the plot
    plt.show()

# Example usage: Run real-time anomaly detection starting after 200 initial data points
run_real_time_anomaly_detection(initial_data_points=200)