import pkg_resources


def get_path(os_path):
    return pkg_resources.resource_filename('app', os_path)
