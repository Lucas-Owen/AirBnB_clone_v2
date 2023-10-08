#!/usr/bin/python3
"""This module defines the do_clean function"""

from fabric.operations import put, run, local
from fabric.api import env, runs_once
import os
env.hosts = ['100.26.170.70', '100.26.255.3']
env.user = 'ubuntu'


def do_clean(number=0):
    """Cleans outdated archives"""
    try:
        number = int(number)
        if number == 0:
            number = 1
        archives = ['./versions/'+file for file in os.listdir('./versions')]
        archives.sort(key=lambda x: os.path.getctime(x), reverse=True)
        archives = archives[number:]
        if archives:
            local('rm -rf {}'.format(' '.join(archives)))
        archives = run(
            'ls -td --time=ctime /data/web_static/releases/web_static*'
            ).split()
        archives = archives[number:]
        if archives:
            run('rm -rf {}'.format(' '.join(archives)))
    except Exception as e:
        print('An exception occured')
