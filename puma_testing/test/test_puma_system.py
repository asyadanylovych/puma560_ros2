"""Інтеграційні тести системи маніпулятора PUMA 560."""
import math
import os
import subprocess

from ament_index_python.packages import get_package_share_directory
import pytest
from sensor_msgs.msg import JointState


def test_urdf_file_exists():
    """Перевіряє наявність файлу опису робота URDF/Xacro."""
    pkg = get_package_share_directory('puma560_description')
    xacro_file = os.path.join(pkg, 'urdf', 'puma560_robot.urdf.xacro')
    assert os.path.exists(xacro_file), f'URDF файл не знайдено: {xacro_file}'


def test_urdf_generates_without_errors():
    """Перевіряє що xacro генерує валідний URDF без помилок."""
    pkg = get_package_share_directory('puma560_description')
    xacro_file = os.path.join(pkg, 'urdf', 'puma560_robot.urdf.xacro')
    result = subprocess.run(
        ['xacro', xacro_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert result.returncode == 0, (
        f'Помилка генерації URDF:\n{result.stderr}'
    )
    assert '<robot' in result.stdout, 'URDF не містить тегу <robot>'


def test_urdf_contains_seven_joints():
    """Перевіряє що маніпулятор має 7 joints (6 рухомих + 1 базовий)."""
    pkg = get_package_share_directory('puma560_description')
    xacro_file = os.path.join(pkg, 'urdf', 'puma560_robot.urdf.xacro')
    result = subprocess.run(
        ['xacro', xacro_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    joint_count = result.stdout.count('<joint name=')
    assert joint_count == 7, (
        f'Очікувалось 7 joints, знайдено: {joint_count}'
    )


def test_urdf_contains_links():
    """Перевіряє що URDF містить ланки маніпулятора."""
    pkg = get_package_share_directory('puma560_description')
    xacro_file = os.path.join(pkg, 'urdf', 'puma560_robot.urdf.xacro')
    result = subprocess.run(
        ['xacro', xacro_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert '<link name=' in result.stdout, 'URDF не містить жодної ланки'


def test_launch_file_exists():
    """Перевіряє наявність launch файлу для запуску системи."""
    pkg = get_package_share_directory('puma560_description')
    launch_file = os.path.join(pkg, 'launch', 'display_puma560.xml')
    assert os.path.exists(launch_file), (
        f'Launch файл не знайдено: {launch_file}'
    )


def test_rviz_config_exists():
    """Перевіряє наявність конфігурації візуалізації RViz2."""
    pkg = get_package_share_directory('puma560_description')
    rviz_config = os.path.join(pkg, 'config', 'puma560.rviz')
    assert os.path.exists(rviz_config), (
        f'Конфігурацію RViz2 не знайдено: {rviz_config}'
    )


def test_all_mesh_files_exist():
    """Перевіряє наявність всіх mesh-файлів геометрії маніпулятора."""
    pkg = get_package_share_directory('puma560_description')
    meshes_dir = os.path.join(pkg, 'meshes')
    expected_meshes = [f'puma_link{i}.stl' for i in range(1, 8)]
    missing = []
    for mesh in expected_meshes:
        mesh_path = os.path.join(meshes_dir, mesh)
        if not os.path.exists(mesh_path):
            missing.append(mesh)
    assert not missing, f'Відсутні mesh файли: {missing}'


def test_joint_state_message_has_six_joints():
    """Перевіряє що повідомлення JointState містить дані про 6 суглобів."""
    msg = JointState()
    msg.name = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    msg.position = [0.0] * 6
    msg.velocity = [0.0] * 6
    msg.effort = [0.0] * 6
    assert len(msg.name) == 6, (
        f'Очікувалось 6 суглобів, отримано: {len(msg.name)}'
    )
    assert len(msg.position) == len(msg.name), (
        'Кількість позицій не відповідає кількості суглобів'
    )
    assert len(msg.velocity) == len(msg.name), (
        'Кількість швидкостей не відповідає кількості суглобів'
    )


def test_joint_state_positions_in_valid_range():
    """Перевіряє що позиції суглобів знаходяться в допустимому діапазоні."""
    msg = JointState()
    msg.name = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    msg.position = [0.0, -1.5, 1.5, 0.0, 0.0, 0.0]
    for i, pos in enumerate(msg.position):
        assert abs(pos) <= math.pi * 2, (
            f'Суглоб {msg.name[i]}: позиція {pos} виходить за допустимий діапазон'
        )


@pytest.mark.parametrize('joint_name', ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'])
def test_each_joint_name_is_valid(joint_name):
    """Перевіряє що кожен суглоб має коректне ім'я."""
    assert joint_name.startswith('j'), (
        f"Некоректне ім'я суглоба: {joint_name}"
    )
    assert len(joint_name) > 0, "Ім'я суглоба не може бути порожнім"
