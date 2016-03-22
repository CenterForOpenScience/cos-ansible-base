#!/usr/bin/env python
"""Rackspace Cloud Monitoring Plugin for Docker Stats."""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# -----
#
# This plugin monitors the Docker containers via the 'docker inspect' command.
# By default the monitor fails if the check does not complete successfully.
#
# Requires:
# Python 2.6 or greater
# docker-py: https://github.com/docker/docker-py
#
# Usage:
# Place script in /usr/lib/rackspace-monitoring-agent/plugins.
# Ensure file is executable (755).
#
# Set up a Cloud Monitoring Check of type agent.plugin to run
#
# docker_stats_check.py -u <URL> -c <container>
#
# The URL is optional and can be a TCP or Unix socket, e.g.
#
# docker_stats_check.py -u tcp://0.0.0.0:2376
# or
# docker_stats_check.py -u unix://var/run/docker.sock
#
# The default URL is unix://var/run/docker.sock.
#
# The container can be name or id
# docker_stats_check.py -u unix://var/run/docker.sock -c agitated_leakey
# or
# docker_stats_check.py -u unix://var/run/docker.sock -c 1f3b3b8f0fcc
#
# There is no need to define specific custom alert criteria.
# As stated, the monitor fails if the stats cannot be collected.
# It is possible to define custom alert criteria with the reported
# metrics if desired.
#

import sys
from docker import Client
from optparse import OptionParser
from subprocess import call
import json

class DockerService(object):
    """Create an object for a Docker service. Assume it is stopped."""

    def __init__(self, url, container):

        self.url = url
        self.container = container
        self.docker_running = False

    def docker_stats(self):
        """Connect to the Docker object and get stats. Error out on failure."""

        docker_conn = Client(base_url=self.url)

        try:
            stats = docker_conn.inspect_container(self.container)
            self.docker_running = True
        # Apologies for the broad exception, it just works here.
        except Exception:
            self.docker_running = False

        if self.docker_running:
            print 'status ok succeeded in obtaining docker container details.'
            container_state = stats['State']
            print 'metric container_running string', container_state['Running']
            print 'metric container_restarting string', container_state['Restarting']
            print 'metric container_oomkilled string', container_state['OOMKilled']
            sys.exit(0)
        else:
            print 'status err failed to obtain docker container stats.'
            sys.exit(1)


def main():
    """Instantiate a DockerStats object and collect stats."""

    parser = OptionParser()
    parser.add_option('-u', '--url', default='unix://var/run/docker.sock',
                      help='URL for Docker service (Unix or TCP socket).')
    parser.add_option('-c', '--container',
                      help='Name or Id of container that you want to monitor')
    (opts, args) = parser.parse_args()
    if opts.container is None:
        parser.error("options -c is mandatory")

    docker_service = DockerService(opts.url, opts.container)
    docker_service.docker_stats()

if __name__ == '__main__':
    main()
