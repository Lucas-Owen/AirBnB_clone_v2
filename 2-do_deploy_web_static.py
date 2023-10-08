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
        tgz_name = os.path.split(archive_path)[-2]
        without_ext = tgz_name.split('.')[-1]
        extract_dir = '/data/web_static/releases/'
        extract_path = '{}{}'.format(extract_dir, without_ext)
        upload_path = '/tmp/{}'.format(tgz_name)
        put(archive_path, "/tmp/")
        run('mkdir -p {}'.format(extract_dir))
        run('tar -xzf {} -C {}'.format(upload_path, extract_dir))
        run('mv {}/web_static {}'.format(extract_dir, extract_path))
        run('rm -rf {}'.format(upload_path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(extract_path))
        print("New version deployed!")
    except Exception as e:
        return None
    return True
