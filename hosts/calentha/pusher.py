from workflow_py.base_objects.pusher import BasePusher


class LinuxPusher(BasePusher):
    pass


def push_to_saved():
    LinuxPusher().push_to_saved()


if __name__ == '__main__':
    LinuxPusher().push_to_saved()
