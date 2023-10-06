#!/usr/bin/python3
"""This module defines the do_deploy function"""


def do_deploy(archive_path):
    """
    Deploys the web_static .tgz file to a server
    """
    from fabric.operations import put, run
    from fabric.api import env
    import os
    env.hosts = ['100.26.170.70', '100.26.255.3']
    env.user = 'ubuntu'
    if not os.path.exists(archive_path):
        return False
    try:
        tgz_name = os.path.split(archive_path)[-1]
        without_ext = tgz_name.split('.')[-1]
        put(archive_path, "/tmp/")
        run('mkdir -p /data/web_static/releases/')
        run('tar -zxvf /tmp/{} -C /data/web_static/releases/'.format(tgz_name))
        run('rm -rf /data/web_static/current')
        run('ln -s -f /data/web_static/releases/{}/ /data/web_static/current'
            .format(without_ext))
    except Exception as e:
        return None
    return True
