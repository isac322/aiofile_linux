# coding: UTF-8

import select

from linux_aio_bind import IOCBCMD, IOCBPriorityClass
from typing import Any

from .base import AIOCmd


class NonRWCmd(AIOCmd):
    """
    .. versionadded:: 0.1.0
    """

    def __init__(self,
                 file: Any,
                 cmd: IOCBCMD,
                 buf: int,
                 priority_class: IOCBPriorityClass,
                 priority_value: int,
                 res_fd: int) -> None:
        super().__init__(file, cmd, 0, priority_class, priority_value, buf, 0, 0, res_fd)


class PollCmd(NonRWCmd):
    """
    .. warning::
        Works only on Linux 4.19 or later.
        Otherwise, submission of this command will raise OSError (with error code 22 EINVAL)

    .. versionadded:: 0.1.0
    """
    __slots__ = ('_event_masks',)

    _event_masks: int

    def __init__(self,
                 file: Any,
                 event_masks: int = None,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        if event_masks is None:
            self._event_masks = select.EPOLLIN | select.EPOLLOUT | select.EPOLLPRI
        else:
            self._event_masks = event_masks

        super().__init__(file, IOCBCMD.POLL, self._event_masks, priority_class, priority_value, res_fd)

    @property
    def event_masks(self) -> int:
        return self._event_masks

    @event_masks.setter
    def event_masks(self, new_masks) -> None:
        self._event_masks = new_masks


class FsyncCmd(NonRWCmd):
    """
    .. warning::
        Works only on Linux 4.18 or later.
        Otherwise, submission of this command will raise OSError (with error code 22 EINVAL)

    .. versionadded:: 0.1.0
    """

    def __init__(self,
                 file: Any,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.FSYNC, 0, priority_class, priority_value, res_fd)


class FDsyncCmd(NonRWCmd):
    """
    .. warning::
        Works only on Linux 4.18 or later.
        Otherwise, submission of this command will raise OSError (with error code 22 EINVAL)

    .. versionadded:: 0.1.0
    """

    def __init__(self,
                 file: Any,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.FDSYNC, 0, priority_class, priority_value, res_fd)
