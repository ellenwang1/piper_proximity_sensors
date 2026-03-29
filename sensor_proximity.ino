#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle nh;
std_msgs::Int32 msg;
ros::Publisher pub("proximity_raw", &msg);

unsigned long last_publish = 0;
const unsigned long PUBLISH_INTERVAL = 1000; // ms

void setup() {
  nh.initNode();
  nh.advertise(pub);
}

void loop() {
  unsigned long now = millis();

  if (now - last_publish >= PUBLISH_INTERVAL) {
    last_publish = now;

    long sum = 0;
    for (int i = 0; i < 10; i++) {
      sum += touchRead(T6);
      delay(2);
    }
    msg.data = (int32_t)(sum / 10);
    pub.publish(&msg);
  }

  nh.spinOnce();
  delay(10);
}