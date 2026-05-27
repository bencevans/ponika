from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Any, TypeAlias

from ponika.endpoints import CRUDEndpoint
from ponika.endpoints.auto_reboot.ping_wget import PingWgetCreatePayload
from ponika.endpoints.auto_reboot.scheduler import SchedulerCreatePayload
from ponika.endpoints.dhcp.static_leases_ipv4 import (
    StaticLeaseIpv4CreatePayload,
)
from ponika.endpoints.dhcp.static_leases_ipv6 import (
    StaticLeaseIpv6CreatePayload,
)
from ponika.endpoints.ip_routes.ipv4 import Ipv4RouteCreatePayload
from ponika.endpoints.ip_routes.ipv6 import Ipv6RouteCreatePayload
from ponika.endpoints.recipients.email_users import EmailUserCreatePayload
from ponika.endpoints.recipients.phone_groups import PhoneGroupCreatePayload
from ponika.endpoints.sms_utilities.rules import SmsRuleCreatePayload
from ponika.endpoints.wireguard.config import WireguardConfigCreatePayload
from ponika.endpoints.wireguard.peers import WireguardPeerCreateItemPayload
from ponika.endpoints.wireless.interfaces import WirelessInterfaceCreatePayload
from ponika.endpoints.zerotier.config import ZerotierConfigCreatePayload
from ponika.endpoints.zerotier.networks import (
    ZerotierNetworkConfigCreatePayload,
)
from ponika.models import BaseModel, BasePayload

if TYPE_CHECKING:
    from ponika import PonikaClient


ConfigValue: TypeAlias = BasePayload | BaseModel | Mapping[str, Any]
ConfigSection: TypeAlias = Sequence[ConfigValue]
ConfigDefinition: TypeAlias = Mapping[str, Mapping[str, ConfigSection]]


class RecipientsConfig(BaseModel):
    phone_groups: list[PhoneGroupCreatePayload] | None = None
    email_users: list[EmailUserCreatePayload] | None = None


class AutoRebootConfig(BaseModel):
    scheduler: list[SchedulerCreatePayload] | None = None
    ping_wget: list[PingWgetCreatePayload] | None = None


class DhcpConfig(BaseModel):
    static_leases_ipv4: list[StaticLeaseIpv4CreatePayload] | None = None
    static_leases_ipv6: list[StaticLeaseIpv6CreatePayload] | None = None


class IpRoutesConfig(BaseModel):
    routes_ipv4: list[Ipv4RouteCreatePayload] | None = None
    routes_ipv6: list[Ipv6RouteCreatePayload] | None = None


class SmsUtilitiesConfig(BaseModel):
    rules: list[SmsRuleCreatePayload] | None = None


class WireguardPeersConfig(BaseModel):
    interface_id: str | int
    items: list[WireguardPeerCreateItemPayload]


class WireguardConfig(BaseModel):
    config: list[WireguardConfigCreatePayload] | None = None
    peers: list[WireguardPeersConfig] | None = None


class WirelessConfig(BaseModel):
    interfaces: list[WirelessInterfaceCreatePayload] | None = None


class ZerotierNetworksConfig(BaseModel):
    config_id: str | int
    items: list[ZerotierNetworkConfigCreatePayload]


class ZerotierConfig(BaseModel):
    config: list[ZerotierConfigCreatePayload] | None = None
    networks: list[ZerotierNetworksConfig] | None = None


class PonikaConfig(BaseModel):
    auto_reboot: AutoRebootConfig | None = None
    dhcp: DhcpConfig | None = None
    ip_routes: IpRoutesConfig | None = None
    recipients: RecipientsConfig | None = None
    sms_utilities: SmsUtilitiesConfig | None = None
    # We do not provide users module within ConfigState method
    # UserManagement should always be a manually task
    # users: list[UserDefinition] | None = None
    wireguard: WireguardConfig | None = None
    wireless: WirelessConfig | None = None
    zerotier: ZerotierConfig | None = None


class ConfigAction(str, Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    UNCHANGED = 'unchanged'


@dataclass(frozen=True)
class ConfigChange:
    section: str
    action: ConfigAction
    match_field: str
    match_value: Any
    existing: dict[str, Any] | None = None
    desired: dict[str, Any] | None = None


@dataclass(frozen=True)
class ConfigApplyResult:
    changes: list[ConfigChange] = field(default_factory=list)

    @property
    def created(self) -> list[ConfigChange]:
        return self._filter(ConfigAction.CREATE)

    @property
    def updated(self) -> list[ConfigChange]:
        return self._filter(ConfigAction.UPDATE)

    @property
    def deleted(self) -> list[ConfigChange]:
        return self._filter(ConfigAction.DELETE)

    @property
    def unchanged(self) -> list[ConfigChange]:
        return self._filter(ConfigAction.UNCHANGED)

    def _filter(self, action: ConfigAction) -> list[ConfigChange]:
        return [change for change in self.changes if change.action == action]


class ConfigApplier:
    """Apply declarative configuration sections to a Ponika device.

    The applier reconciles only sections present in the given config. For each
    managed section it creates missing items, updates changed items and deletes
    existing items that are not present in the desired configuration.
    """

    def __init__(self, client: 'PonikaClient') -> None:
        self._client = client

    def apply(
        self,
        config: PonikaConfig | ConfigDefinition,
        dry_run: bool = False,
        delete_unmanaged: bool = True,
    ) -> ConfigApplyResult:
        changes: list[ConfigChange] = []

        for group_name, group_config in self._config_to_mapping(
            config
        ).items():
            group = getattr(self._client, group_name, None)
            if group is None:
                raise ValueError(f'Unknown config group: {group_name}')

            if self._is_reconcile_endpoint(group):
                changes.extend(
                    self.apply_endpoint(
                        endpoint=group,
                        desired_items=group_config,
                        section=group_name,
                        dry_run=dry_run,
                        delete_unmanaged=delete_unmanaged,
                    )
                )
                continue

            for section_name, desired_items in group_config.items():
                endpoint = getattr(group, section_name, None)
                if endpoint is None:
                    raise ValueError(
                        f'Unknown config section: {group_name}.{section_name}'
                    )
                if self._is_reconcile_endpoint(endpoint):
                    changes.extend(
                        self.apply_endpoint(
                            endpoint=endpoint,
                            desired_items=desired_items,
                            section=f'{group_name}.{section_name}',
                            dry_run=dry_run,
                            delete_unmanaged=delete_unmanaged,
                        )
                    )
                    continue

                if self._is_dynamic_config_section(endpoint, desired_items):
                    for dynamic_config in desired_items:
                        dynamic_endpoint = endpoint.config(
                            **self._dynamic_path_params(dynamic_config)
                        )
                        changes.extend(
                            self.apply_endpoint(
                                endpoint=dynamic_endpoint,
                                desired_items=dynamic_config['items'],
                                section=f'{group_name}.{section_name}',
                                dry_run=dry_run,
                                delete_unmanaged=delete_unmanaged,
                            )
                        )
                    continue

                if not self._is_reconcile_endpoint(endpoint):
                    raise ValueError(
                        f'Config section {group_name}.{section_name} does not '
                        'support CRUD reconciliation.'
                    )

        return ConfigApplyResult(changes=changes)

    def _config_to_mapping(
        self, config: PonikaConfig | ConfigDefinition
    ) -> ConfigDefinition:
        if isinstance(config, PonikaConfig):
            return config.model_dump(exclude_none=True)
        return config

    def _is_reconcile_endpoint(self, endpoint: Any) -> bool:
        return isinstance(endpoint, CRUDEndpoint) or all(
            hasattr(endpoint, method)
            for method in ('get_config', 'create', 'update', 'delete')
        )

    def _is_dynamic_config_section(
        self, endpoint: Any, desired_items: Any
    ) -> bool:
        return (
            hasattr(endpoint, 'config')
            and isinstance(desired_items, list)
            and all(
                isinstance(item, Mapping) and 'items' in item
                for item in desired_items
            )
        )

    def _dynamic_path_params(
        self, dynamic_config: Mapping[str, Any]
    ) -> dict[str, Any]:
        return {
            key: value
            for key, value in dynamic_config.items()
            if key != 'items'
        }

    def print_changes(self, changes: ConfigApplyResult):
        print('Planned changes:')
        for change in changes.changes:
            print(
                f'- {change.action.value}: '
                f'{change.section} {change.match_field}={change.match_value}'
            )
            print(f'  Existing: {change.existing}')
            print(f'  Desired:  {change.desired}')

    def apply_endpoint(
        self,
        endpoint: CRUDEndpoint,
        desired_items: ConfigSection,
        section: str,
        dry_run: bool = False,
        delete_unmanaged: bool = True,
    ) -> list[ConfigChange]:
        existing_items = endpoint.get_config()
        desired_data = [self._to_data(item) for item in desired_items]
        existing_data = [self._to_data(item) for item in existing_items]

        match_fields = getattr(endpoint, 'config_match_fields', ('id',))
        desired_by_key = self._index_desired(
            desired_data, match_fields, section
        )
        existing_by_key = self._index_existing(existing_data, match_fields)
        matched_existing_ids: set[Any] = set()
        deleted_existing_ids: set[Any] = set()

        changes: list[ConfigChange] = []
        for key, desired_item in desired_by_key.items():
            match_field, match_value = key
            existing_item = existing_by_key.get(key)

            if existing_item is None:
                if not dry_run:
                    endpoint.create(endpoint.create_model(**desired_item))
                changes.append(
                    ConfigChange(
                        section=section,
                        action=ConfigAction.CREATE,
                        match_field=match_field,
                        match_value=match_value,
                        desired=desired_item,
                    )
                )
                continue

            item_id = existing_item.get(endpoint.config_id_field)
            if item_id is not None:
                matched_existing_ids.add(item_id)

            if self._is_changed(existing_item, desired_item):
                if item_id is None:
                    raise ValueError(
                        f'Existing item in {section} has no '
                        f'{endpoint.config_id_field!r} field.'
                    )
                update_data = {
                    endpoint.config_id_field: item_id,
                    **desired_item,
                }
                if not dry_run:
                    endpoint.update(endpoint.update_model(**update_data))
                changes.append(
                    ConfigChange(
                        section=section,
                        action=ConfigAction.UPDATE,
                        match_field=match_field,
                        match_value=match_value,
                        existing=existing_item,
                        desired=update_data,
                    )
                )
            else:
                changes.append(
                    ConfigChange(
                        section=section,
                        action=ConfigAction.UNCHANGED,
                        match_field=match_field,
                        match_value=match_value,
                        existing=existing_item,
                        desired=desired_item,
                    )
                )

        if not delete_unmanaged:
            return changes

        for key, existing_item in existing_by_key.items():
            item_id = existing_item.get(endpoint.config_id_field)
            if item_id is None:
                raise ValueError(
                    f'Existing item in {section} has no '
                    f'{endpoint.config_id_field!r} field.'
                )
            if (
                item_id in matched_existing_ids
                or item_id in deleted_existing_ids
            ):
                continue

            if not dry_run:
                endpoint.delete(item_id)
            deleted_existing_ids.add(item_id)
            changes.append(
                ConfigChange(
                    section=section,
                    action=ConfigAction.DELETE,
                    match_field=key[0],
                    match_value=key[1],
                    existing=existing_item,
                )
            )

        return changes

    def _index_desired(
        self,
        items: list[dict[str, Any]],
        match_fields: tuple[str, ...],
        section: str,
    ) -> dict[tuple[str, Any], dict[str, Any]]:
        result: dict[tuple[str, Any], dict[str, Any]] = {}
        for item in items:
            key = self._key_for_item(item, match_fields)
            if key is None:
                raise ValueError(
                    f'Desired item in {section} needs one of these match '
                    f'fields: {", ".join(match_fields)}'
                )
            if key in result:
                raise ValueError(
                    f'Duplicate desired item in {section}: {key[0]}={key[1]!r}'
                )
            result[key] = item
        return result

    def _index_existing(
        self,
        items: list[dict[str, Any]],
        match_fields: tuple[str, ...],
    ) -> dict[tuple[str, Any], dict[str, Any]]:
        result: dict[tuple[str, Any], dict[str, Any]] = {}
        for item in items:
            for key in self._keys_for_item(item, match_fields):
                result.setdefault(key, item)
        return result

    def _keys_for_item(
        self, item: Mapping[str, Any], match_fields: tuple[str, ...]
    ) -> list[tuple[str, Any]]:
        return [
            (field_name, self._normalise(value))
            for field_name in match_fields
            if (value := item.get(field_name)) is not None
        ]

    def _key_for_item(
        self, item: Mapping[str, Any], match_fields: tuple[str, ...]
    ) -> tuple[str, Any] | None:
        for field_name in match_fields:
            value = item.get(field_name)
            if value is not None:
                return field_name, self._normalise(value)
        return None

    def _is_changed(
        self, existing: Mapping[str, Any], desired: Mapping[str, Any]
    ) -> bool:
        return any(
            self._normalise(existing.get(field_name)) != self._normalise(value)
            for field_name, value in desired.items()
        )

    def _to_data(self, item: ConfigValue) -> dict[str, Any]:
        if isinstance(item, BasePayload):
            return item.asdict()
        if isinstance(item, BaseModel):
            return item.model_dump(exclude_unset=True, exclude_none=True)
        return dict(item)

    def _normalise(self, value: Any) -> Any:
        if isinstance(value, bool):
            return value
        if value in ('0', '1'):
            return value == '1'
        if isinstance(value, list):
            return [self._normalise(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self._normalise(item) for item in value)
        if isinstance(value, dict):
            return {key: self._normalise(item) for key, item in value.items()}
        return value
