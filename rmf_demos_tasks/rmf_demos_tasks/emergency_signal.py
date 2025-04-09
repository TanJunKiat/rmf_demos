#!/usr/bin/env python3

# Copyright 2025 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Publish an emergency signal."""

import argparse
import sys

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy as Durability
from rclpy.qos import QoSProfile
from rclpy.qos import QoSReliabilityPolicy as Reliability

from rmf_fleet_msgs.msg import EmergencySignal

###############################################################################

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False

class EmergencySignalPublisher(Node):
    """Emergency signal publisher."""

    def __init__(self, argv=sys.argv):
        """Initialize the emergency signal publisher."""
        super().__init__('emergency_signal_publisher')
        qos_profile = QoSProfile(
            depth=10,
            durability=Durability.VOLATILE,
            reliability=Reliability.RELIABLE
        )
        self.publisher = self.create_publisher(EmergencySignal, 'emergency_signal', qos_profile)
        
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'is_emergency',
            type=str2bool,
            help='Emergency message to publish (true or false)',
        )

        parser.add_argument(
            '-f',
            '--fleet',
            type=str,
            help='Fleets to trigger',
            nargs='+',
        )

        self.args = parser.parse_args(argv[1:])
        msg = EmergencySignal()
        msg.is_emergency = self.args.is_emergency
        self.get_logger().info('Publishing emergency signal: %s' % msg.is_emergency)
        if self.args.fleet is not None:
            msg.fleet_names = self.args.fleet
            self.get_logger().info('Fleets: %s' % msg.fleet_names)
        else:
            self.get_logger().info('No fleets specified, sending to all fleets')
        self.publisher.publish(msg)

###############################################################################


def main(argv=sys.argv):
    """Publish an emergency signal."""
    rclpy.init(args=sys.argv)
    args_without_ros = rclpy.utilities.remove_ros_args(sys.argv)
    signal_publisher = EmergencySignalPublisher(args_without_ros)
    signal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main(sys.argv)
