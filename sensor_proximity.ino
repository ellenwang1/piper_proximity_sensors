#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle nh;

std_msgs::Int32 msg_d7, msg_a4;

ros::Publisher pub_d7("proximity/d7", &msg_d7);
ros::Publisher pub_a4("proximity/a4", &msg_a4);

unsigned long last_publish = 0;
const unsigned long PUBLISH_INTERVAL = 20; // match your 20ms delay

void setup() {
  nh.initNode();
  nh.advertise(pub_d7);
  nh.advertise(pub_a4);
}

void loop() {
  unsigned long now = millis();

  if (now - last_publish >= PUBLISH_INTERVAL) {
    last_publish = now;

    msg_d7.data = (int32_t)touchRead(13); // D7 = GPIO13
    msg_a4.data = (int32_t)touchRead(15); // A4 = GPIO15

    pub_d7.publish(&msg_d7);
    pub_a4.publish(&msg_a4);
  }

  nh.spinOnce();
  delay(10);
}