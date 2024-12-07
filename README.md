# Efficient Data Stream Anomaly Detection System

A comprehensive project designed to detect anomalies in continuous data streams using a Z-Score-based algorithm. The system dynamically adapts to evolving data patterns, identifying irregularities in real-time with minimal computational overhead. It includes components for data simulation, anomaly detection, optimization, and visualization.

## Design Process and Methods

### Data Stream Simulation
- **Purpose:** To generate a realistic data stream simulating conditions like seasonality, concept drift, random noise, and anomalies.
- **Key Features:**
  - Seasonal patterns modeled using a sine wave.
  - Gradual concept drift through incremental shifts in the data stream.
  - Gaussian random noise to mimic natural variations.
  - Randomly injected anomalies representing extreme outliers or deviations.

### Anomaly Detection
- **Algorithm:** Z-Score-based anomaly detection with a rolling window.
- **Key Features:**
  - **Dynamic Threshold:** Adjusts based on recent anomalies and adapts to evolving data.
  - **Rolling Statistics:** Maintains a moving average and standard deviation for efficiency.
  - **Early Stop Mechanism:** Skips calculations for insignificant deviations, improving performance.
  - **Anomaly Buffer:** Ensures consecutive anomalies do not skew subsequent statistical calculations.

### Optimization
- **Techniques Implemented:**
  - **Efficient Data Structure:** A Python deque is used for the rolling window, allowing O(1) operations for adding and removing data points.
  - **Online Updates:** Incremental updates to mean and standard deviation reduce computational overhead.
  - **Dynamic Threshold Reset:** Automatically resets sensitivity after anomalies to maintain robust detection.

### Visualization
- **Tool Used:** Matplotlib for real-time plotting.
- **Features:**
  - A dynamic line plot showing the data stream.
  - Anomalies highlighted with red markers.
  - Real-time updates for continuous monitoring and analysis.

## Testing and Results

### Real-Time Anomaly Detection in Action
The system was tested in real time using a data stream containing random noise, seasonal patterns, and occasional anomalies. Under default conditions, the system successfully detected and flagged anomalies as they occurred. Key parameters:
- **Noise level:** Default (0.5)
- **Anomaly chance:** Default (0.05)

### Testing Under Challenging Conditions
To evaluate the system’s robustness, it was further tested with increased noise and anomaly rates, simulating more volatile data conditions. The system maintained its adaptability and accurately flagged anomalies. Key parameters:
- **Noise level:** Doubled (1.0)
- **Anomaly chance:** Doubled (0.1)

These tests demonstrated the system’s ability to handle a variety of conditions, ensuring reliability across different environments and conditions.
