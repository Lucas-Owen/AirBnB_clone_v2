#!/usr/bin/python3
"""This module defines the do_deploy function"""


from fabric.operations import put, run
from fabric.api import env
import os

env.hosts = ['100.26.170.70', '100.26.255.3']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Deploys the web_static .tgz file to a server
    """
    if not os.path.exists(archive_path):
        print(archive_path)
        return False
    try:
        tgz_name = os.path.split(archive_path)[-1]
        without_ext = tgz_name.split('.')[-1]
        extract_path = '/data/web_static/releases/{}'.format(without_ext)
        upload_path = '/tmp/{}'.format(tgz_name)
        put(archive_path, "/tmp/")
        run('mkdir -p {}'.format(extract_path))
        run('tar -xzf {} -C {}'.format(upload_path, extract_path))
        run('rm -rf {}'.format(upload_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(extract_path))
        print("New version deployed!")
    except Exception as e:
        return None
    return True
