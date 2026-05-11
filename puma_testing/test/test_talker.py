import pytest
from puma_testing.puma_testing.talker import MinimalPublisher
import rclpy

def test_node_init():
    rclpy.init()
    node = MinimalPublisher()
    # Тест: чи створився об'єкт ноди?
    assert node is not None
    # Тест: чи правильне ім'я ноди?
    assert node.get_name() == 'minimal_publisher'
    node.destroy_node()
    rclpy.shutdown()