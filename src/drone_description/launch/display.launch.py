from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution 
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
  
    urdf_file_path = PathJoinSubstitution([
        get_package_share_directory('drone_description'),
        'drone1',
        'main.urdf.xacro' 
    ])

    rviz_conf = PathJoinSubstitution([
        get_package_share_directory('drone_description'),
        'rviz',
        'drone_conf.rviz'
    ])

    robot_description_content = Command([
        'xacro ',
        urdf_file_path
    ])
    robot_description = ParameterValue(
        robot_description_content,
        value_type=str
    )
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
        output='screen' 
    )
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_conf],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz2_node
    ])

