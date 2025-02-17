#include <rclcpp/rclcpp.hpp>
#include <nav2_msgs/action/navigate_to_pose.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

class NavigationNode : public rclcpp::Node
{
public:
    NavigationNode() : Node("navigation_node")
    {
        this->client_ptr_ = rclcpp_action::create_client<nav2_msgs::action::NavigateToPose>(
            this,
            "navigate_to_pose");

        this->initial_pose_publisher_ = this->create_publisher<geometry_msgs::msg::PoseStamped>(
            "initialpose", 10);

        // Set initial pose
        this->set_initial_pose();

        // Wait for the action server to be available
        while (!this->client_ptr_->wait_for_action_server(std::chrono::seconds(1))) {
            if (!rclcpp::ok()) {
                RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for action server.");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "Waiting for action server...");
        }

        // Send goal pose
        this->send_goal();
    }

private:
    void set_initial_pose()
    {
        auto initial_pose = geometry_msgs::msg::PoseStamped();
        initial_pose.header.frame_id = "map";
        initial_pose.header.stamp = this->now();
        initial_pose.pose.position.x = 0.0;
        initial_pose.pose.position.y = 0.0;
        initial_pose.pose.position.z = 0.0;
        initial_pose.pose.orientation.w = 1.0;

        RCLCPP_INFO(this->get_logger(), "Publishing initial pose");
        this->initial_pose_publisher_->publish(initial_pose);
    }

    void send_goal()
    {
        auto goal_msg = nav2_msgs::action::NavigateToPose::Goal();
        goal_msg.pose.header.frame_id = "map";
        goal_msg.pose.header.stamp = this->now();
        goal_msg.pose.pose.position.x = -29.0;
        goal_msg.pose.pose.position.y = -5.0;
        goal_msg.pose.pose.orientation.w = 1.0;

        RCLCPP_INFO(this->get_logger(), "Sending goal");
        auto send_goal_options = rclcpp_action::Client<nav2_msgs::action::NavigateToPose>::SendGoalOptions();
        send_goal_options.goal_response_callback = 
            std::bind(&NavigationNode::goal_response_callback, this, std::placeholders::_1);
        send_goal_options.result_callback = 
            std::bind(&NavigationNode::result_callback, this, std::placeholders::_1);
        this->client_ptr_->async_send_goal(goal_msg, send_goal_options);
    }

    void goal_response_callback(const rclcpp_action::ClientGoalHandle<nav2_msgs::action::NavigateToPose>::SharedPtr & goal_handle)
    {
        if (!goal_handle) {
            RCLCPP_ERROR(this->get_logger(), "Goal was rejected by server");
        } else {
            RCLCPP_INFO(this->get_logger(), "Goal accepted by server, waiting for result");
        }
    }

    void result_callback(const rclcpp_action::ClientGoalHandle<nav2_msgs::action::NavigateToPose>::WrappedResult & result)
    {
        switch (result.code) {
            case rclcpp_action::ResultCode::SUCCEEDED:
                RCLCPP_INFO(this->get_logger(), "Goal succeeded");
                break;
            case rclcpp_action::ResultCode::ABORTED:
                RCLCPP_ERROR(this->get_logger(), "Goal was aborted");
                break;
            case rclcpp_action::ResultCode::CANCELED:
                RCLCPP_ERROR(this->get_logger(), "Goal was canceled");
                break;
            default:
                RCLCPP_ERROR(this->get_logger(), "Unknown result code");
                break;
        }
        rclcpp::shutdown();
    }

    rclcpp_action::Client<nav2_msgs::action::NavigateToPose>::SharedPtr client_ptr_;
    rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr initial_pose_publisher_;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NavigationNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
