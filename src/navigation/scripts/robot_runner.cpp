#include <rclcpp/rclcpp.hpp>
#include <nav2_msgs/action/navigate_to_pose.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>

class MultiGoalNavigationNode : public rclcpp::Node
{
public:
    using NavigateToPose = nav2_msgs::action::NavigateToPose;
    using GoalHandleNav = rclcpp_action::ClientGoalHandle<NavigateToPose>;

    MultiGoalNavigationNode() : Node("multi_goal_navigation_node"), goal_index_(0)
    {
        this->client_ptr_ = rclcpp_action::create_client<NavigateToPose>(this, "navigate_to_pose");

        this->initial_pose_publisher_ = this->create_publisher<geometry_msgs::msg::PoseStamped>("initialpose", 10);

        this->set_initial_pose();

        while (!this->client_ptr_->wait_for_action_server(std::chrono::seconds(2))) {
            if (!rclcpp::ok()) {
                RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for action server.");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "Waiting for Nav2 action server");
        }

        goals_ = {
            {8.0, 2.0, 1.0},
            {-18.0, -10.0, 1.0},
            {7.0, -3.0, 1.0},
            {0.0, 0.0, 1.0}
        };

        send_next_goal();
    }

private:
    void set_initial_pose()
    {
        auto initial_pose = geometry_msgs::msg::PoseStamped();
        initial_pose.header.frame_id = "map";
        initial_pose.header.stamp = this->now();
        initial_pose.pose.position.x = 0.0;
        initial_pose.pose.position.y = 0.0;
        initial_pose.pose.orientation.w = 1.0;

        RCLCPP_INFO(this->get_logger(), "Publishing initial pose");
        this->initial_pose_publisher_->publish(initial_pose);
    }

    void send_next_goal()
    {
        if (goal_index_ >= goals_.size()) {
            RCLCPP_INFO(this->get_logger(), "All goals reached! Navigation completed.");
            rclcpp::shutdown();
            return;
        }

        auto goal_msg = NavigateToPose::Goal();
        goal_msg.pose.header.frame_id = "map";
        goal_msg.pose.header.stamp = this->now();
        goal_msg.pose.pose.position.x = goals_[goal_index_][0];
        goal_msg.pose.pose.position.y = goals_[goal_index_][1];
        goal_msg.pose.pose.orientation.w = goals_[goal_index_][2];

        RCLCPP_INFO(this->get_logger(), "Sending goal %d: (%.2f, %.2f)", goal_index_ + 1, goals_[goal_index_][0], goals_[goal_index_][1]);

        auto send_goal_options = rclcpp_action::Client<NavigateToPose>::SendGoalOptions();
        send_goal_options.goal_response_callback = std::bind(&MultiGoalNavigationNode::goal_response_callback, this, std::placeholders::_1);
        send_goal_options.result_callback = std::bind(&MultiGoalNavigationNode::result_callback, this, std::placeholders::_1);
        
        client_ptr_->async_send_goal(goal_msg, send_goal_options);
    }

    void goal_response_callback(const std::shared_ptr<GoalHandleNav> & goal_handle)
    {
        if (!goal_handle) {
            RCLCPP_ERROR(this->get_logger(), "Goal was rejected by the server.");
        } else {
            RCLCPP_INFO(this->get_logger(), "Goal accepted by server. Waiting for result");
        }
    }

    void result_callback(const GoalHandleNav::WrappedResult & result)
    {
        if (result.code == rclcpp_action::ResultCode::SUCCEEDED) {
            RCLCPP_INFO(this->get_logger(), "Goal %d reached successfully", goal_index_ + 1);
        } else if (result.code == rclcpp_action::ResultCode::ABORTED) {
            RCLCPP_ERROR(this->get_logger(), "Goal %d was aborted", goal_index_ + 1);
        } else if (result.code == rclcpp_action::ResultCode::CANCELED) {
            RCLCPP_ERROR(this->get_logger(), "Goal %d was canceled", goal_index_ + 1);
        }

        goal_index_++;
        send_next_goal();
    }

    rclcpp_action::Client<NavigateToPose>::SharedPtr client_ptr_;
    rclcpp::Publisher<geometry_msgs::msg::PoseStamped>::SharedPtr initial_pose_publisher_;
    std::vector<std::array<double, 3>> goals_;
    size_t goal_index_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MultiGoalNavigationNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
