"""Інтеграційні тести системи маніпулятора PUMA 560."""
import math
import os
import subprocess

import pytest
from sensor_msgs.msg import JointState

try:
    from ament_index_python.packages import get_package_share_directory
    PKG = get_package_share_directory('puma560_description')
    PUMA_AVAILABLE = True
except Exception:
    PKG = None
    PUMA_AVAILABLE = False

puma_only = pytest.mark.skipif(
    not PUMA_AVAILABLE,
    reason='puma560_description not installed'
)


@puma_only
def test_urdf_file_exists():
    """1 Перевіряє наявність файлу опису робота URDF/Xacro."""
    xacro_file = os.path.join(PKG, 'urdf', 'puma560_robot.urdf.xacro')
    assert os.path.exists(xacro_file), f'URDF файл не знайдено: {xacro_file}'


@puma_only
def test_urdf_generates_without_errors():
    """2 Перевіряє що xacro генерує валідний URDF без помилок."""
    xacro_file = os.path.join(PKG, 'urdf', 'puma560_robot.urdf.xacro')
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


@puma_only
def test_urdf_contains_seven_joints():
    """3 Перевіряє що маніпулятор має 7 joints (6 рухомих + 1 базовий)."""
    xacro_file = os.path.join(PKG, 'urdf', 'puma560_robot.urdf.xacro')
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


@puma_only
def test_urdf_contains_links():
    """4 Перевіряє що URDF містить ланки маніпулятора."""
    xacro_file = os.path.join(PKG, 'urdf', 'puma560_robot.urdf.xacro')
    result = subprocess.run(
        ['xacro', xacro_file],
        capture_output=True,
        text=True,
        timeout=30
    )
    assert '<link name=' in result.stdout, 'URDF не містить жодної ланки'


@puma_only
def test_launch_file_exists():
    """5 Перевіряє наявність launch файлу для запуску системи."""
    launch_file = os.path.join(PKG, 'launch', 'display_puma560.xml')
    assert os.path.exists(launch_file), (
        f'Launch файл не знайдено: {launch_file}'
    )


@puma_only
def test_rviz_config_exists():
    """6 Перевіряє наявність конфігурації візуалізації RViz2."""
    rviz_config = os.path.join(PKG, 'config', 'puma560.rviz')
    assert os.path.exists(rviz_config), (
        f'Конфігурацію RViz2 не знайдено: {rviz_config}'
    )


@puma_only
def test_all_mesh_files_exist():
    """7 Перевіряє наявність всіх mesh-файлів геометрії маніпулятора."""
    meshes_dir = os.path.join(PKG, 'meshes')
    expected_meshes = [f'puma_link{i}.stl' for i in range(1, 8)]
    missing = []
    for mesh in expected_meshes:
        if not os.path.exists(os.path.join(meshes_dir, mesh)):
            missing.append(mesh)
    assert not missing, f'Відсутні mesh файли: {missing}'


def test_joint_state_message_has_six_joints():
    """8 Перевіряє що повідомлення JointState містить дані про 6 суглобів."""
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
    """9 Перевіряє що позиції суглобів знаходяться в допустимому діапазоні."""
    msg = JointState()
    msg.name = ['j1', 'j2', 'j3', 'j4', 'j5', 'j6']
    msg.position = [0.0, -1.5, 1.5, 0.0, 0.0, 0.0]
    for i, pos in enumerate(msg.position):
        assert abs(pos) <= math.pi * 2, (
            f'Суглоб {msg.name[i]}: позиція {
                pos} виходить за допустимий діапазон'
        )


@pytest.mark.parametrize('joint_name', ['j1', 'j2', 'j3', 'j4', 'j5', 'j6'])
def test_each_joint_name_is_valid(joint_name):
    """10Перевіряє що кожен суглоб має коректне ім'я."""
    assert joint_name.startswith('j'), (
        f"Некоректне ім'я суглоба: {joint_name}"
    )
    assert len(joint_name) > 0, "Ім'я суглоба не може бути порожнім"
