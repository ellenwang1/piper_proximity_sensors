import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, Float32

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.subscription = self.create_subscription(
            Int32,
            'proximity_raw',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Float32, 'proximity_filtered', 10)
        self.baseline = None
        self.baseline_samples = []
        self.calibrating = True
        self.get_logger().info('Sensor node started, calibrating baseline...')

    def listener_callback(self, msg):
        raw = float(msg.data)

        # Collect 20 samples for baseline
        if self.calibrating:
            self.baseline_samples.append(raw)
            if len(self.baseline_samples) >= 20:
                self.baseline = sum(self.baseline_samples) / len(self.baseline_samples)
                self.calibrating = False
                self.get_logger().info(f'Baseline set: {self.baseline:.1f}')
            return

        # Publish how far below baseline we are (positive = object detected)
        delta = self.baseline - raw
        out = Float32()
        out.data = delta
        self.publisher.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
