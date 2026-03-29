#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle nh;

std_msgs::Int32 msg_t6, msg_t9;

ros::Publisher pub_t6("proximity/t6", &msg_t6);
ros::Publisher pub_t9("proximity/t9", &msg_t9);

unsigned long last_publish = 0;
const unsigned long PUBLISH_INTERVAL = 1000; // ms

void setup() {
  nh.initNode();
  nh.advertise(pub_t6);
  nh.advertise(pub_t9);
}

void loop() {
  unsigned long now = millis();

  if (now - last_publish >= PUBLISH_INTERVAL) {
    last_publish = now;

    msg_t6.data = (int32_t)touchRead(T6);
    msg_t9.data = (int32_t)touchRead(T9);

    pub_t6.publish(&msg_t6);
    pub_t9.publish(&msg_t9);
  }

  nh.spinOnce();
  delay(10);
}