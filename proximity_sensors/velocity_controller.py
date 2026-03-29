import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String
import math

SWEEP_JOINTS = [0, 1, 2]
SWEEP_AMPLITUDE = 0.3
SWEEP_SPEED = 0.005
HOME = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

class VelocityController:
    def __init__(self):
        rospy.init_node('velocity_controller')

        self.joint_pub = rospy.Publisher('/joint_states', JointState, queue_size=10)

        rospy.Subscriber('proximity/d7/warning', String, self.warning_callback_d7, queue_size=10)
        rospy.Subscriber('proximity/a4/warning', String, self.warning_callback_a4, queue_size=10)

        self.warning_d7 = 'CLEAR'
        self.warning_a4 = 'CLEAR'
        self.positions = HOME.copy()
        self.phase = 0.0

        self.timer = rospy.Timer(rospy.Duration(0.05), self.control_loop)
        rospy.loginfo('Velocity controller started')

    def warning_callback_d7(self, msg):
        self.warning_d7 = msg.data

    def warning_callback_a4(self, msg):
        self.warning_a4 = msg.data

    def combined_warning(self):
        # Worst case of the two sensors wins
        warnings = [self.warning_d7, self.warning_a4]
        if 'STOP' in warnings:
            return 'STOP'
        if 'SLOW' in warnings:
            return 'SLOW'
        return 'CLEAR'

    def control_loop(self, event):
        warning = self.combined_warning()

        if warning == 'STOP':
            pass
        elif warning == 'SLOW':
            self.phase += SWEEP_SPEED * 0.5
            self._update_positions()
        else:
            self.phase += SWEEP_SPEED
            self._update_positions()

        msg = JointState()
        msg.header.stamp = rospy.Time.now()
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

def main():
    node = VelocityController()
    rospy.spin()

if __name__ == '__main__':
    main()