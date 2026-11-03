#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

//参数占位符
using std::placeholders::_1;

class SimpleSubscriber : public rclcpp::Node
{
public:
  SimpleSubscriber() : Node("simple_subscriber")
  {
    //创建订阅者
    sub_ = create_subscription<std_msgs::msg::String>(
        "chatter", 10, std::bind(&SimpleSubscriber::msgCallback, this, _1));
  }

private:
//保存订阅者
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;
//接收并输出消息
  void msgCallback(const std_msgs::msg::String &msg) const
  {
    RCLCPP_INFO_STREAM(this->get_logger(), "I heard: " << msg.data.c_str());
  }
};


int main(int argc, char * argv[])
{
  //初始化
  rclcpp::init(argc, argv);
  //创建运行节点 --启动
  rclcpp::spin(std::make_shared<SimpleSubscriber>());
  rclcpp::shutdown();
  return 0;
}