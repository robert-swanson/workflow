from py.base_objects.pusher import BasePusher


class MacPusher(BasePusher):
    pass


def push_to_saved():
    MacPusher().push_to_saved()


if __name__ == '__main__':
    push_to_saved()
