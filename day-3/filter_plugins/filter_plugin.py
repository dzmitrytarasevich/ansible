from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors

def get_mongo_src(arg, os_family, os_version, mongo_version):
    systems = {'RedHat':'rhel', 'Debian':'debian', 'CentOS': 'centos', 'Suse': 'suse', 'Ubuntu': 'ubuntu'}
    if os_family not in systems:
        print(os_family)
        return "Your OS doesn't exist in OS list!"
    for links in arg:
        if systems[os_family] in links and os_version in links and mongo_version in links:
            return links
    return "There is no link for your OS in mongodb.yml file!"

class FilterModule(object):
    def filters(self):
        return {
            'get_mongo_src': get_mongo_src
        }
