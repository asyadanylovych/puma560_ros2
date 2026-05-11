import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.get_logger().info('Talker Node has been started!')
        
    def send_hello(self):
        msg = String()
        msg.data = 'Hello from Diploma Project'
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    minimal_publisher.send_hello()
    minimal_publisher.destroy_node()
    rclpy.shutdown()