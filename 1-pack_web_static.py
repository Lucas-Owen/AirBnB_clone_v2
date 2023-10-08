#!/usr/bin/python3
"""This module defines the do_pack function"""


def do_pack():
    """
    Generates a .tgz of web_static folder
    Name is web_static_<year><month><day><hour><minute><second>.tgz
    """
    from datetime import datetime
    from fabric.operations import local
    import os
    time = datetime.now()
    tgz = "versions/web_static_{:4d}{:02d}{:02d}{:02d}{:02d}{:02d}.tgz".format(
        time.year,
        time.month,
        time.day,
        time.hour,
        time.minute,
        time.second,
    )
    print("Packing web_static to {}".format(tgz))
    if not os.path.isdir('versions'):
        local('mkdir -p versions')
    try:
        local('tar -czvf {} web_static'.format(tgz))
    except Exception as e:
        return None
    print("web_static packed: {} -> {}Bytes".format(tgz,
                                                    os.path.getsize(tgz)))
    return tgz
