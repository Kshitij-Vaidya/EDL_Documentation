#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from px4_msgs.msg import VehicleAttitude
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
import math
import threading

def euler_from_quaternion(x, y, z, w):
    """Convert quaternion to Euler angles (roll, pitch, yaw)."""
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = max(min(t2, +1.0), -1.0)  # Clamp t2 within [-1, 1]
    pitch_y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)

    return roll_x, pitch_y, yaw_z

class ForcePublisher(Node):
    def __init__(self):
        super().__init__('force_publisher')

        # QoS profiles
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        qos_profile_2 = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )

        # Publishers & Subscribers
        self.force_pub = self.create_publisher(Wrench, '/gazebo_ros_force', qos_profile_2)
        self.vehicle_attitude_subscriber = self.create_subscription(
            VehicleAttitude, '/fmu/out/vehicle_attitude', self.vehicle_attitude_callback, qos_profile
        )

        # Force message
        self.force = Wrench()
        self.force_val = 0.0  # Default force value

        # Start user input thread
        self.input_thread = threading.Thread(target=self.get_user_input, daemon=True)
        self.input_thread.start()

    def get_user_input(self):
        """Runs in a separate thread to take user input asynchronously."""
        while rclpy.ok():
            try:
                user_input = float(input("Enter a force value: "))  # Convert input to float
                self.force_val = user_input
                self.get_logger().info(f"Force value updated: {self.force_val}")
            except ValueError:
                self.get_logger().warn("Invalid input! Please enter a number.")

    def vehicle_attitude_callback(self, msg):
        """Callback for vehicle attitude data."""
        _, _, angle = euler_from_quaternion(msg.q[1], msg.q[2], msg.q[3], msg.q[0])
        self.spray_control(angle)

    def spray_control(self, angle):
        """Computes force components and publishes to Gazebo."""
        self.force.force.x = -self.force_val * math.sin(angle)
        self.force.force.y = self.force_val * math.cos(angle)
        if(self.force_val):
            self.force.force.z = -6.9776
        else: 
            self.force.force.z = 0.0
        self.force_pub.publish(self.force)

def main(args=None):
    rclpy.init(args=args)
    node = ForcePublisher()
    rclpy.spin(node)  # Keep node alive
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
