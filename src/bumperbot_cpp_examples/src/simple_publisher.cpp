//客户端库
#include <rclcpp/rclcpp.hpp>
//字符串消息
#include <std_msgs/msg/string.hpp>
//时间处理
#include <chrono>

//时间命名空间
using namespace std::chrono_literals;
//继承Node类
class SimplePublisher : public rclcpp::Node
{
public:
  SimplePublisher() : Node("simple_publisher"), counter_(0)
  {
    //创建发布者
    pub_ = create_publisher<std_msgs::msg::String>("chatter", 10);
    //创建定时器
    timer_ = create_wall_timer(1s, std::bind(&SimplePublisher::timerCallback, this));
    //日志
    RCLCPP_INFO(get_logger(), "Publishing at 1 Hz");
  }

  void timerCallback()
  {
    //创建消息
    auto message = std_msgs::msg::String();
    //消息内容
    message.data = "Hello ROS 2 - counter:" + std::to_string(counter_++);
    
    pub_->publish(message);
  }

private:
  //保存publisher
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr pub_;
  //保存定时器
  rclcpp::TimerBase::SharedPtr timer_;
  //计数器
  unsigned int counter_;
};


int main(int argc, char* argv[])
{
//初始化
  rclcpp::init(argc, argv);
  auto node = std::make_shared<SimplePublisher>();

//持续处理回调
  rclcpp::spin(node);
  
  rclcpp::shutdown();
  return 0;
}