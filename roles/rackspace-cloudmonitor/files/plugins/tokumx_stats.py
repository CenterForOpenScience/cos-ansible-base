#!/usr/bin/env python
"""
Rackspace Cloud Monitoring plugin to provide mongodb statistics.

Requirement:
pymongo - http://api.mongodb.org/python/current/

Copyright 2013 Steve Katen <steve.katen@rackspace.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from ConfigParser import SafeConfigParser
import sys

parser = SafeConfigParser()
parser.read('.env')
DATABASE_USER = parser.get('tokumx', 'DATABASE_USER')
DATABASE_PASS = parser.get('tokumx', 'DATABASE_PASS')
DATABASE_HOST = parser.get('tokumx', 'DATABASE_HOST')
DATABASE_PORT = parser.get('tokumx', 'DATABASE_PORT')
DATABASE_DB = parser.get('tokumx', 'DATABASE_DB')

try:
    from pymongo import MongoClient as Client
except ImportError:
    from pymongo import Connection as Client
from pymongo.errors import ConnectionFailure, AutoReconnect


def mongodb_stats(host, p, database, username, password):
    port = int(p)
    try:
        if username and password and database:
            c = Client("mongodb://"+username+":"+password+"@"+host+"/"+database, port)
        elif username and password:
            c = Client('mongodb://'+username+':'+password+'@'+host+'/', port)
        elif database:
            c = Client('mongodb://'+host+'/'+database, port)
        else:
            c = Client(host, port)
    except ConnectionFailure, AutoReconnect:
        return None
    else:
        return c.test.command("serverStatus")


def main():

    s = mongodb_stats(DATABASE_HOST,DATABASE_PORT,DATABASE_DB,DATABASE_USER,DATABASE_PASS)

    if not s:
        print "status err unable to generate statistics"
        sys.exit(0)

    print "status ok mongodb statistics generated"
    print "metric uptime float", s['uptime']
    print "metric conn_available int", s['connections']['available']
    print "metric conn_current int", s['connections']['current']
    print "metric conn_percent float", float(s['connections']['current']
                                             / s['connections']['available'])

    #print "metric mem_mapped int", s['mem']['mapped']
    #print "metric index_hits int", s['indexCounters']['hits']
    #print "metric index_misses int", s['indexCounters']['misses']
    #try:
    #    print "metric index_percent int", float(s['indexCounters']['hits']
    #                                        / s['indexCounters']['accesses'])
    #except ZeroDivisionError:
    #    print "metric index_percent int 0"

    #if (s['indexCounters']['btree']):
    #    print "metric index_hits int", s['indexCounters']['btree']['hits']
    #    print "metric index_misses int", s['indexCounters']['btree']['misses']
    #    print "metric index_percent int", float(s['indexCounters']['btree']['hits']
    #                                        / s['indexCounters']['btree']['accesses'])
    #else:
    #    print s['indexCounters']['btree']['hits']
    #    print "metric index_hits int", s['indexCounters']['hits']
    #    print "metric index_misses int", s['indexCounters']['misses']
    #    print "metric index_percent int", float(s['indexCounters']['hits']
    #                                        / s['indexCounters']['accesses'])

    if 'repl' in s:
        print "metric is_replicating string true"
        print "metric is_master string", s['repl']['ismaster']
        print "metric is_secondary string", s['repl']['secondary']
    else:
        print "metric is_replicating string false"

if __name__ == '__main__':
    main()
