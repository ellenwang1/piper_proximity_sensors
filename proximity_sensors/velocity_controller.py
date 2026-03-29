
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import math
import time

# Safe sweep range in radians — adjust these to suit your workspace
SWEEP_JOINTS = [0, 1, 2]        # which joints to move (0=joint1 etc)
SWEEP_AMPLITUDE = 0.3            # radians either side of home
SWEEP_SPEED = 0.005              # radians per tick — lower = slower

# Home position — arm starts and returns here
HOME = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

class VelocityController(Node):
    def __init__(self):
        super().__init__('velocity_controller')

        self.joint_pub = self.create_publisher(
            JointState, '/joint_states', 10)

        self.warning_sub = self.create_subscription(
            String, '/collision_warning',
            self.warning_callback, 10)

        # State
        self.warning = 'CLEAR'
        self.positions = HOME.copy()
        self.phase = 0.0

        # Timer — publishes at 20Hz
        self.timer = self.create_timer(0.05, self.control_loop)
        self.get_logger().info('Velocity controller started')

    def warning_callback(self, msg):
        self.warning = msg.data
        if self.warning != 'CLEAR':
            self.get_logger().warn(f'Collision warning: {self.warning}')

    def control_loop(self):
        now = self.get_clock().now().to_msg()

        if self.warning == 'STOP':
            # Publish current position repeatedly — arm holds still
            pass

        elif self.warning == 'SLOW':
            # Advance phase at half speed
            self.phase += SWEEP_SPEED * 0.5
            self._update_positions()

        else:  # CLEAR
            # Advance phase at full speed
            self.phase += SWEEP_SPEED
            self._update_positions()

        # Publish
        msg = JointState()
        msg.header.stamp = now
        msg.header.frame_id = 'piper_single'
        msg.name = ['joint1', 'joint2', 'joint3',
                    'joint4', 'joint5', 'joint6']
        msg.position = self.positions
        msg.velocity = [0.0] * 6
        msg.effort = [0.0] * 6
        self.joint_pub.publish(msg)

    def _update_positions(self):
        for i in SWEEP_JOINTS:
            self.positions[i] = SWEEP_AMPLITUDE * math.sin(self.phase)

def main(args=None):
    rclpy.init(args=args)
    node = VelocityController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()