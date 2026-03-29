import rospy
from std_msgs.msg import Int32, Float32

class SensorNode:
    def __init__(self):
        rospy.init_node('sensor_node')
        self.subscription = rospy.Subscriber('proximity_raw', Int32, self.listener_callback, queue_size=10)
        self.publisher = rospy.Publisher('proximity_filtered', Float32, queue_size=10)
        self.baseline = None
        self.baseline_samples = []
        self.calibrating = True
        rospy.loginfo('Sensor node started, calibrating baseline...')

    def listener_callback(self, msg):
        raw = float(msg.data)

        if self.calibrating:
            self.baseline_samples.append(raw)
            if len(self.baseline_samples) >= 20:
                self.baseline = sum(self.baseline_samples) / len(self.baseline_samples)
                self.calibrating = False
                rospy.loginfo(f'Baseline set: {self.baseline:.1f}')
            return

        delta = self.baseline - raw
        out = Float32()
        out.data = delta
        self.publisher.publish(out)

def main():
    node = SensorNode()
    rospy.spin()

if __name__ == '__main__':
    main()