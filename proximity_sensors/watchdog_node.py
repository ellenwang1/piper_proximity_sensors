import rospy
from std_msgs.msg import Float32, String

SLOW_THRESHOLD = 3.0
STOP_THRESHOLD = 10.0

class WatchdogNode:
    def __init__(self, input_topic, output_topic):
        self.subscription = rospy.Subscriber(input_topic, Float32, self.listener_callback, queue_size=10)
        self.publisher = rospy.Publisher(output_topic, String, queue_size=10)
        rospy.loginfo(f'Watchdog node started on {input_topic}')

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
            rospy.logwarn(f'Collision warning: {warning.data} (delta={delta:.1f})')

def main():
    rospy.init_node('watchdog_node')
    WatchdogNode('proximity/d7/filtered', 'proximity/d7/warning')
    WatchdogNode('proximity/a4/filtered', 'proximity/a4/warning')
    rospy.spin()

if __name__ == '__main__':
    main()