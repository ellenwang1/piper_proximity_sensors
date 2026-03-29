import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Float32

BASELINE_SAMPLES = 20
DRIFT_RATE = 0.01  # how fast baseline tracks slow changes (0=fixed, 1=instant)

class FilterNode(Node):
    def __init__(self):
        super().__init__('filter_node')
        self.subscription = self.create_subscription(
            Int32,
            'proximity_raw',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Float32, 'proximity_filtered', 10)
        self.baseline = None
        self.baseline_samples = []
        self.calibrating = True
        self.get_logger().info('Filter node started, calibrating baseline...')

    def listener_callback(self, msg):
        raw = float(msg.data)

        # Collect samples for initial baseline
        if self.calibrating:
            self.baseline_samples.append(raw)
            if len(self.baseline_samples) >= BASELINE_SAMPLES:
                self.baseline = sum(self.baseline_samples) / len(self.baseline_samples)
                self.calibrating = False
                self.get_logger().info(f'Baseline set: {self.baseline:.1f}')
            return

        # Slowly drift baseline to track environmental changes
        # Sharp sudden changes (objects approaching) won't be absorbed
        self.baseline = self.baseline * (1.0 - DRIFT_RATE) + raw * DRIFT_RATE

        # Publish how far below baseline we are (positive = object detected)
        delta = self.baseline - raw
        out = Float32()
        out.data = max(0.0, delta)  # clamp to zero — negative means nothing detected
        self.publisher.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = FilterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()