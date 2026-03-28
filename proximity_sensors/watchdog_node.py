import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String

SLOW_THRESHOLD = 3.0   # start slowing down
STOP_THRESHOLD = 10.0  # stop immediately

class WatchdogNode(Node):
    def __init__(self):
        super().__init__('watchdog_node')
        self.subscription = self.create_subscription(
            Float32,
            'proximity_filtered',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(String, 'collision_warning', 10)
        self.get_logger().info('Watchdog node started')

    def listener_callback(self, msg):
        delta = msg.data
        warning = String()

        if delta >= STOP_THRESHOLD:
            warning.data = 'STOP'
        elif delta >= SLOW_THRESHOLD:
            warning.data = 'SLOW'
        else:
            warning.data = 'CLEAR'

        self.publisher.publish(warning)
        if warning.data != 'CLEAR':
            self.get_logger().warn(f'Collision warning: {warning.data} (delta={delta:.1f})')

def main(args=None):
    rclpy.init(args=args)
    node = WatchdogNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
