from py.path_object.host.host import Host
from py.var_store import VAR_STORE


def get_host_list() -> list[Host]:
    return [Host(host_dir) for host_dir in VAR_STORE.get_hosts_dir().iterdir() if host_dir.is_dir()]
