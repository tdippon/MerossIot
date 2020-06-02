import logging
from datetime import datetime
from typing import Union, List

from meross_iot.model.enums import OnlineStatus
from meross_iot.model.shared import BaseDictPayload

_LOGGER = logging.getLogger(__name__)


class HttpDeviceInfo(BaseDictPayload):
    def __init__(self,
                 uuid: str,
                 online_status: Union[int, OnlineStatus],
                 dev_name: str,
                 dev_icon_id: str,
                 bind_time: Union[int, datetime],
                 device_type: str,
                 sub_type: str,
                 channels: List[dict],
                 region: str,
                 fmware_version: str,
                 hdware_version: str,
                 user_dev_icon: str,
                 icon_type: int,
                 skill_number: str,
                 domain: str,
                 reserved_domain: str,
                 *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.uuid = uuid
        if isinstance(online_status, int):
            self.online_status = OnlineStatus(online_status)
        elif isinstance(online_status, OnlineStatus):
            self.online_status = online_status
        else:
            _LOGGER.warning(f"Provided online_status is not int neither OnlineStatus. It will be ignored.")
            self.online_status = None

        self.dev_name = dev_name
        self.dev_icon_id = dev_icon_id
        if isinstance(bind_time, int):
            self.bind_time = datetime.utcfromtimestamp(bind_time)
        elif isinstance(bind_time, datetime):
            self.bind_time = bind_time
        else:
            _LOGGER.warning(f"Provided bind_time is not int neither datetime. It will be ignored.")
            self.bind_time = None

        self.device_type = device_type
        self.sub_type = sub_type
        self.channels = channels
        self.region = region
        self.fmware_version = fmware_version
        self.hdware_version = hdware_version
        self.user_dev_icon = user_dev_icon
        self.icon_type = icon_type
        self.skill_number = skill_number
        self.domain = domain
        self.reserved_domain = reserved_domain

