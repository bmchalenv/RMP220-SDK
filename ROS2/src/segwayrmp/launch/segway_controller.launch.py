from launch.launch_description import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration



def generate_launch_description():
    """Generate launch description with multiple components."""
    ld = LaunchDescription()
    ld.add_action(DeclareLaunchArgument(
        'container_prefix',
        default_value='',
    ))
    ld.add_action(DeclareLaunchArgument(
        'comu_interface',
        default_value='can',
        choices=['can', 'serial'],
    ))
    ld.add_action(ComposableNodeContainer(
            name='segway_container',
            namespace='',
            prefix=LaunchConfiguration('container_prefix'),
            package='rclcpp_components',
            executable='component_container_mt',
            composable_node_descriptions=[
                ComposableNode(
                    package='segwayrmp',
                    plugin='robot::Chassis',
                    namespace='chassis',
                    name='segway_chassis',
                    parameters=[{
                        'comu_interface': LaunchConfiguration('comu_interface'),
                    }]
                ),
                ComposableNode(
                    package='segwayrmp',
                    plugin='segway::SegwayController',
                    namespace='chassis',
                    name='segway_controller',
                    remappings=[
                        ('in_cmd_vel', '/twist_mux/cmd_vel'),
                        ('out_cmd_vel', 'cmd_vel')
                    ]
                ),
            ],
            output='screen',
    ))

    return ld