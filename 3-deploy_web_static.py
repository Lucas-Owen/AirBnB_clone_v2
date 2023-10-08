#!/usr/bin/python3
"""This module defines the deploy function"""

from fabric.operations import put, run, local
from fabric.api import env, runs_once
from datetime import datetime
import os
env.hosts = ['100.26.170.70', '100.26.255.3']
env.user = 'ubuntu'


@runs_once
def do_pack():
    """
    Generates a .tgz of web_static folder
    Name is web_static_<year><month><day><hour><minute><second>.tgz
    """

    time = datetime.now()
    name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        time.year,
        time.month,
        time.day,
        time.hour,
        time.minute,
        time.second,
    )
    print("Packing web_static to {}".format(name))
    if not os.path.isdir('versions'):
        local('mkdir -p versions')
    try:
        local('tar -czvf {} web_static'.format(name))
    except Exception as e:
        return None
    print("web_static packed: {} -> {}Bytes".format(name,
                                                    os.path.getsize(name)))
    return name


def do_deploy(archive_path):
    """
    Deploys the web_static .tgz file to a server
    """
    if not os.path.exists(archive_path):
        print(archive_path)
        return False
    try:
        tgz_name = os.path.split(archive_path)[-1]
        without_ext = tgz_name.split('.')[-2]
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


def deploy():
    """
    Deploys the web_static .tgz file to a server
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
