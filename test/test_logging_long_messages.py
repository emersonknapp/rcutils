# Copyright 2017 Open Source Robotics Foundation, Inc.
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

import os

from launch import LaunchDescription
from launch import LaunchService
from launch.actions import ExecuteProcess
from launch_testing import LaunchTestService
from launch_testing.output import create_output_test_from_file


def test_logging_long_messages():
    # Set the output format to a "verbose" format that is expected by the executable output
    os.environ['RCUTILS_CONSOLE_OUTPUT_FORMAT'] = \
        '[{severity}] [{name}]: {message} ({function_name}() at {file_name}:{line_number})'
    executable = os.path.join(os.getcwd(), 'test_logging_long_messages')
    if os.name == 'nt':
        executable += '.exe'
    ld = LaunchDescription()
    launch_test = LaunchTestService()
    action = launch_test.add_fixture_action(ld, ExecuteProcess(
        cmd=[executable], name='test_logging_long_messages', output='screen'
    ))
    output_file = os.path.join(
        os.path.dirname(__file__), 'test_logging_long_messages'
    )
    launch_test.add_output_test(
        ld, action, create_output_test_from_file(output_file)
    )

    launch_service = LaunchService()
    launch_service.include_launch_description(ld)
    return_code = launch_test.run(launch_service)
    assert return_code == 0, 'Launch failed with exit code %r' % (return_code,)


if __name__ == '__main__':
    test_logging_long_messages()
