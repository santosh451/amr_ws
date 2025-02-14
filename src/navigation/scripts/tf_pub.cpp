#include <memory>
#include <rclcpp/rclcpp.hpp>
#include <tf2_ros/static_transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

class StaticTFPublisher : public rclcpp::Node
{
public:
    StaticTFPublisher() : Node("static_tf_publisher")
    {
        broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

        // Publish static transform from map -> odom
        publish_static_tf("map", "odom", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0);

        // Publish static transform from odom -> base_link
        publish_static_tf("odom", "base_link", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0);

        RCLCPP_INFO(this->get_logger(), "Published static transforms: map → odom, odom → base_link");
    }

private:
    std::shared_ptr<tf2_ros::StaticTransformBroadcaster> broadcaster_;

    void publish_static_tf(
        const std::string &parent_frame,
        const std::string &child_frame,
        double x, double y, double z,
        double qx, double qy, double qz, double qw)
    {
        geometry_msgs::msg::TransformStamped transform_stamped;
        transform_stamped.header.stamp = this->now();
        transform_stamped.header.frame_id = parent_frame;
        transform_stamped.child_frame_id = child_frame;
        transform_stamped.transform.translation.x = x;
        transform_stamped.transform.translation.y = y;
        transform_stamped.transform.translation.z = z;
        transform_stamped.transform.rotation.x = qx;
        transform_stamped.transform.rotation.y = qy;
        transform_stamped.transform.rotation.z = qz;
        transform_stamped.transform.rotation.w = qw;

        broadcaster_->sendTransform(transform_stamped);
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    
    // Create node and execute it immediately
    auto node = std::make_shared<StaticTFPublisher>();
    
    // Ensure messages are published before shutdown
    rclcpp::sleep_for(std::chrono::milliseconds(100));
    
    // rclcpp::shutdown();
    return 0;
}
