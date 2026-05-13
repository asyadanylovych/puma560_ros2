"""
Модуль тестового вузла MinimalPublisher для верифікації ROS 2.

Цей модуль містить базову реалізацію вузла-видавця.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    """Тестовий видавець, що публікує повідомлення у топік."""

    def __init__(self):
        """Ініціалізує вузол та створює видавця."""
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        self.get_logger().info('Talker Node has been started!')

    def send_hello(self):
        """Публікує привітальне повідомлення."""
        msg = String()
        msg.data = 'Hello from Diploma Project'
        self.publisher_.publish(msg)

    def process_data(self, data):
        """Обробляє вхідні дані та повертає рядок."""
        if data is None:
            raise ValueError('Вхідні дані не можуть бути None')
        return str(data)


def main(args=None):
    """Головна функція запуску тестового видавця."""
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    minimal_publisher.send_hello()
    minimal_publisher.destroy_node()
    rclpy.shutdown()
