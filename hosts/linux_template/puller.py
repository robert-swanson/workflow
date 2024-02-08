from workflow_py.base_objects.puller import BasePuller


class LinuxPuller(BasePuller):
    pass


def pull_to_local():
    LinuxPuller().pull_to_local()


if __name__ == '__main__':
    pull_to_local()
