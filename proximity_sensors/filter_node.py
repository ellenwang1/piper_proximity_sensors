import rospy
from std_msgs.msg import Int32, Float32

BASELINE_SAMPLES = 20
DRIFT_RATE = 0.01

class FilterNode:
    def __init__(self, input_topic, output_topic):
        self.subscription = rospy.Subscriber(input_topic, Int32, self.listener_callback, queue_size=10)
        self.publisher = rospy.Publisher(output_topic, Float32, queue_size=10)
        self.baseline = None
        self.baseline_samples = []
        self.calibrating = True
        rospy.loginfo(f'Filter node started on {input_topic}, calibrating baseline...')

    def listener_callback(self, msg):
        raw = float(msg.data)

        if self.calibrating:
            self.baseline_samples.append(raw)
            if len(self.baseline_samples) >= BASELINE_SAMPLES:
                self.baseline = sum(self.baseline_samples) / len(self.baseline_samples)
                self.calibrating = False
                rospy.loginfo(f'Baseline set: {self.baseline:.1f}')
            return

        self.baseline = self.baseline * (1.0 - DRIFT_RATE) + raw * DRIFT_RATE
        delta = self.baseline - raw
        out = Float32()
        out.data = max(0.0, delta)
        self.publisher.publish(out)

def main():
    rospy.init_node('filter_node')
    FilterNode('proximity/d7', 'proximity/d7/filtered')
    FilterNode('proximity/a4', 'proximity/a4/filtered')
    rospy.spin()

if __name__ == '__main__':
    main()