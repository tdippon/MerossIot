import logging

from meross_iot.model.enums import Namespace, OnlineStatus

_LOGGER = logging.getLogger(__name__)


class SystemAllMixin(object):
    _execute_command: callable
    _abilities_spec: dict
    handle_update: callable

    def __init__(self, device_uuid: str,
                 manager,
                 **kwargs):
        super().__init__(device_uuid=device_uuid, manager=manager, **kwargs)

    async def async_update(self, *args, **kwargs) -> None:
        # Call the super implementation
        await super().async_update(*args, **kwargs)

        result = await self._execute_command(method="GET", namespace=Namespace.SYSTEM_ALL, payload={})

        # Once we have the response, update all the mixin which are interested
        self.handle_update(namespace=Namespace.SYSTEM_ALL, data=result)


class SystemOnlineMixin(object):
    _abilities_spec: dict
    _online: OnlineStatus
    handle_update: callable

    def __init__(self, device_uuid: str,
                 manager,
                 **kwargs):
        super().__init__(device_uuid=device_uuid, manager=manager, **kwargs)

    def handle_update(self, namespace: Namespace, data: dict) -> bool:
        _LOGGER.debug(f"Handling {self.__class__.__name__} mixin data update.")
        locally_handled = False
        if namespace == Namespace.SYSTEM_ALL:
            online_data = data.get('all').get('system').get('online')
            status = OnlineStatus(online_data.get("status"))
            self._online = status
            locally_handled = True

        super_handled = super().handle_update(namespace=namespace, data=data)
        return super_handled or locally_handled

    def handle_push_notification(self, namespace: Namespace, data: dict) -> bool:
        locally_handled = False

        if namespace == Namespace.SYSTEM_ONLINE:
            _LOGGER.debug(f"OnlineMixin handling push notification for namespace {namespace}")
            payload = data.get('online')
            if payload is None:
                _LOGGER.error(f"OnlineMixin could not find 'online' attribute in push notification data: "
                              f"{data}")
                locally_handled = False
            else:
                online_data = payload.get("online")
                status = OnlineStatus(online_data.get("status"))
                self._online = status
                locally_handled = True

        # Always call the parent handler when done with local specific logic. This gives the opportunity to all
        # ancestors to catch all events.
        parent_handled = super().handle_push_notification(namespace=namespace, data=data)
        return locally_handled or parent_handled
