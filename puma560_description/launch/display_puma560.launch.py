import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, Command, FindExecutable
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Получаем путь к пакету
    pkg_share = FindPackageShare(
        'puma560_description').find('puma560_description')

    # Путь к xacro файлу
    xacro_file = os.path.join(pkg_share, 'urdf', 'puma560_robot.urdf.xacro')

    # Генерируем robot_description используя xacro
    robot_description = Command(
        [FindExecutable(name='xacro'), ' ', xacro_file])

    # Аргументы запуска
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    return LaunchDescription([
        # Узел robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time
            }]
        ),

        # Статический трансформ от world к link1
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='world_to_link1',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'link1']
        ),

        # GUI для управления суставами
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            parameters=[{
                'robot_description': robot_description,
                'use_sim_time': use_sim_time
            }]
        ),

        # RViz2 с предустановленной конфигурацией
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', os.path.join(pkg_share, 'config', 'puma560.rviz')]
        )
    ])
