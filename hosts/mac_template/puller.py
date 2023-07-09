from py.base_objects.puller import BasePuller


class MacPuller(BasePuller):
    pass


def pull_to_local():
    MacPuller().pull_to_local()


if __name__ == '__main__':
    pull_to_local()
