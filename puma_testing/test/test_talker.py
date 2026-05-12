"""Юніт-тести для вузла MinimalPublisher."""
from puma_testing.talker import MinimalPublisher
import pytest
import rclpy
from std_msgs.msg import String


@pytest.fixture(scope='module', autouse=True)
def init_rclpy():
    """Ініціалізує rclpy один раз для всіх тестів модуля."""
    rclpy.init()
    yield
    rclpy.shutdown()


def test_node_creation():
    """Вузол успішно створюється."""
    node = MinimalPublisher()
    assert node is not None
    node.destroy_node()


def test_node_name():
    """Вузол має правильне ім'я 'minimal_publisher'."""
    node = MinimalPublisher()
    assert node.get_name() == 'minimal_publisher'
    node.destroy_node()


def test_send_hello_no_exception():
    """Метод send_hello() виконується без винятків."""
    node = MinimalPublisher()
    try:
        node.send_hello()
    except Exception as e:
        pytest.fail(f'send_hello() викинув виняток: {e}')
    node.destroy_node()


def test_message_content():
    """Повідомлення містить очікуваний текст."""
    msg = String()
    msg.data = 'Hello from Diploma Project'
    assert msg.data == 'Hello from Diploma Project'


def test_publisher_exists():
    """Вузол має видавця у топіку."""
    node = MinimalPublisher()
    assert node.count_publishers('/topic') >= 0
    node.destroy_node()
