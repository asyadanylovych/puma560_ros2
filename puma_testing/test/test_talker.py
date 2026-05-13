"""
Юніт-тести для вузла MinimalPublisher.

Модуль реалізує набір ізольованих юніт-тестів для верифікації
коректності функціонування вузла-видавця ROS 2 відповідно до
методики модульного тестування на базі фреймворку pytest.
"""

from puma_testing.talker import MinimalPublisher
import pytest
import rclpy
from std_msgs.msg import String


@pytest.fixture(scope='module', autouse=True)
def init_rclpy():
    """Ініціалізує середовище rclpy один раз для всього модуля."""
    rclpy.init()
    yield
    rclpy.shutdown()


def test_node_creation():
    """Верифікує успішне створення екземпляру вузла."""
    node = MinimalPublisher()
    assert node is not None
    node.destroy_node()


def test_node_name():
    """Верифікує що вузол реєструється під коректним іменем."""
    node = MinimalPublisher()
    assert node.get_name() == 'minimal_publisher'
    node.destroy_node()


def test_send_hello_no_exception():
    """Верифікує що публікація не генерує винятків."""
    node = MinimalPublisher()
    try:
        node.send_hello()
    except Exception as e:
        pytest.fail(f'send_hello() викинув виняток: {e}')
    node.destroy_node()


def test_message_content():
    """Верифікує що вузол публікує коректний вміст."""
    node = MinimalPublisher()
    received = []

    node.create_subscription(
        String,
        'topic',
        lambda msg: received.append(msg.data),
        10
    )

    node.send_hello()
    rclpy.spin_once(node, timeout_sec=1.0)

    assert len(received) > 0
    assert received[0] == 'Hello from Diploma Project'
    node.destroy_node()


def test_publisher_exists():
    """Верифікує наявність активного видавця у топіку."""
    node = MinimalPublisher()
    assert node.count_publishers('/topic') >= 1
    node.destroy_node()
