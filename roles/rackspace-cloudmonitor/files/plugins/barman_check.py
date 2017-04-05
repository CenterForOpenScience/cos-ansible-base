#!/usr/bin/env python
"""Rackspace Cloud Monitoring Plugin for Check Barman Status."""

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
# This plugin monitors the Barman container via the 'barman check' command.
# By default the monitor fails if the check does not complete successfully.
#
# Requires:
# Python 2.7
# docker-py: https://github.com/docker/docker-py
#
#
# Usage:
# Place script in /usr/lib/rackspace-monitoring-agent/plugins.
# Ensure file is executable (755).
#
# Set up a Cloud Monitoring Check of type agent.plugin to run
#
# barman_check.py -u <URL> -c <container> -d <database>
#
# The URL is optional and can be a TCP or Unix socket, e.g.
#
# barman_check.py -u tcp://0.0.0.0:2376
# or
# barman_check.py -u unix://var/run/docker.sock
#
# The default URL is unix://var/run/docker.sock.
#
# The container can be name or id
# barman_check.py -c barman
# or
# barman_check.py -c b534aab12cb2
#
# The default name is barman
#
# The database is the database server name configured in barman
# barman_check.py -d pg_osf
#
# The default name is pg_osf
#
# There is no need to define specific custom alert criteria.
# As stated, the monitor fails if the stats cannot be collected.
# It is possible to define custom alert criteria with the reported
# metrics if desired.
#


import json
import optparse
import sys

from docker import Client
from docker.errors import APIError


class DockerService(object):
    """Create an object for a Docker service. Assume it is stopped."""

    def __init__(self, url, container, database):

        self.url = url
        self.container = container
        self.command = 'barman check ' + database

    def slugify(value):
        """
        Converts to lowercase, removes non-word characters (alphanumerics and
        underscores) and converts spaces to hyphens. Also strips leading and
        trailing whitespace.
        """
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return mark_safe(re.sub('[-\s]+', '-', value))
        slugify = allow_lazy(slugify, six.text_type)
        
    def barman_check(self):
        """Connect to the Barman Docker object and check configuration. Error out on failure."""

        docker_client = Client(base_url=self.url)

        try:
            # TODO: verify that the barman container is running
            docker_client.inspect_container(self.container)
        except Exception:
            print('stats err failed when inspecting the container.')
            sys.exit(1)

        try:
            exec_id = docker_client.exec_create(self.container, self.command)
            response = docker_client.exec_start(exec_id)
        except Exception:
            print('stats err failed to execute barman check command in the container.')
            sys.exit(1)

        failed = False
        for line in response.splitlines()[1:]:
            check, value = line.strip().split(': ', 1)
            slug = check.lower().replace(' ', '_').replace('-', '_')
            print('metric {} string {}'.format(slug, value))
            if value.startswith('FAILED'):
                failed = True
        if failed:
            print('status err failure in barman check')
            sys.exit(1)
        print('status ok all checks passed')

        
def main():
    """Instantiate a DockerService and Check Barman Configuration"""

    parser = optparse.OptionParser()

    parser.add_option(
        '-u',
        '--url',
        default='unix://var/run/docker.sock',
        help='URL for Docker service (Unix or TCP socket).'
    )

    parser.add_option(
        '-c',
        '--container',
        default='barman',
        help='Name or Id of container that you want to monitor'
    )

    parser.add_option(
        '-d',
        '--database',
        default='pg_osf',
        help='Name of the database server for barman backup'
    )

    (opts, args) = parser.parse_args()

    docker_service = DockerService(opts.url, opts.container, opts.database)
    docker_service.barman_check()


if __name__ == '__main__':
    main()
