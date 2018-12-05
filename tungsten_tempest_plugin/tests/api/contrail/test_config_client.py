# Copyright 2016 AT&T Corp
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Tempest test-case to test config objects using RBAC roles
"""

import random

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ConfigNodeTest(rbac_base.BaseContrailTest):

    """
    Test class to test config node objects using RBAC roles
    """

    @staticmethod
    def _random_ip_generator():
        random_ip = ".".join(map(str, (random.randint(0, 255)
                                       for _ in range(4))))
        return random_ip

    def _create_config_node(self):
        config_node_ip_address = self._random_ip_generator()
        display_name = data_utils.rand_name('config_node')
        fq_name = [display_name]
        config_node = self.config_client.create_config_nodes(
            config_node_ip_address=config_node_ip_address,
            display_name=display_name, fq_name=fq_name)
        config_node_id = config_node['config-node']['uuid']
        if config_node_id:
            self.addCleanup(self._try_delete_resource,
                            self.config_client.delete_config_node,
                            config_node_id)
        return config_node

    @decorators.idempotent_id('fc18b48d-33f0-4262-b9e6-25be8ed0a1c8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_config_nodes"])
    @idempotent_id('b560e060-e4f0-45b0-93e2-55f0cb201e06')
    def test_list_config_nodes(self):
        """
        test method for list config node objects
        """
        with self.rbac_utils.override_role(self):
            self.config_client.list_config_nodes()

    @decorators.idempotent_id('b1cf9b76-2014-4e1c-a4de-3279935f1804')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_config_nodes"])
    @idempotent_id('a8d20d0d-dc5a-4cae-87c5-7f6914c3701e')
    def test_create_config_nodes(self):
        """
        test method for create config node objects
        """
        with self.rbac_utils.override_role(self):
            self._create_config_node()

    @decorators.idempotent_id('5cb27969-7cd3-4797-8379-f92e83c589b7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_config_node"])
    @idempotent_id('16573a85-57ab-418c-bb23-5dd936e7be90')
    def test_delete_config_node(self):
        """
        test method for delete config node objects
        """
        config_node = self._create_config_node()
        config_node_uuid = config_node['config-node']['uuid']
        with self.rbac_utils.override_role(self):
            self.config_client.delete_config_node(
                config_node_uuid)

    @decorators.idempotent_id('1b21427f-4869-44a3-b617-0a272ca1268b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_config_node"])
    @idempotent_id('a5b17108-4fa3-4d09-b861-e2857aab8f80')
    def test_show_config_node(self):
        """
        test method for show config node objects
        """
        config_node = self._create_config_node()
        config_node_uuid = config_node['config-node']['uuid']
        with self.rbac_utils.override_role(self):
            self.config_client.show_config_node(config_node_uuid)

    @decorators.idempotent_id('e3fce15b-4a56-4bff-b4c9-484e375cf9b0')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_config_node"])
    @idempotent_id('8f70d2c0-594b-4a94-ab15-88bd8a2e62e5')
    def test_update_config_node(self):
        """
        test method for update config node objects
        """
        config_node = self._create_config_node()
        config_node_uuid = config_node['config-node']['uuid']
        updated_name = data_utils.rand_name('new_config_node')
        with self.rbac_utils.override_role(self):
            self.config_client.update_config_node(
                config_node_uuid, display_name=updated_name)


class ConfigRootTest(rbac_base.BaseContrailTest):

    """
    Test class to test config root objects using RBAC roles
    """

    def _create_config_root(self):
        display_name = data_utils.rand_name('config_root')
        fq_name = [display_name]
        config_root = self.config_client.create_config_roots(
            display_name=display_name, fq_name=fq_name)
        config_root_uuid = config_root['config-root']['uuid']
        if config_root_uuid:
            self.addCleanup(self._try_delete_resource,
                            self.config_client.delete_config_root,
                            config_root_uuid)
        return config_root

    @decorators.idempotent_id('f4f12780-0f1e-4609-ac9a-f8f165f4c6ce')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_config_roots"])
    @idempotent_id('291b28ea-d0d8-47cd-ac76-1f980047cb76')
    def test_create_config_roots(self):
        """
        test method for create config root service objects
        """
        with self.rbac_utils.override_role(self):
            self._create_config_root()

    @decorators.idempotent_id('969dc640-7ae4-4ee2-adb0-d1be8a12591a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_config_root"])
    @idempotent_id('bd04c0fb-3deb-4904-ad2c-1a10933c30dd')
    def test_delete_config_root(self):
        """
        test method for delete config root service objects
        """
        config_root = self._create_config_root()
        config_root_uuid = config_root['config-root']['uuid']
        with self.rbac_utils.override_role(self):
            self.config_client.delete_config_root(
                config_root_uuid)

    @decorators.idempotent_id('457d314c-5a79-428f-bea9-c280cfa56d4a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_config_root"])
    @idempotent_id('fba2c419-9a83-4d88-9a26-84770544bb3f')
    def test_show_config_root(self):
        """
        test method for show config root service objects
        """
        config_root = self._create_config_root()
        config_root_uuid = config_root['config-root']['uuid']
        with self.rbac_utils.override_role(self):
            self.config_client.show_config_root(config_root_uuid)

    @decorators.idempotent_id('6b362490-4475-4530-bdde-e46364b99838')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_config_root"])
    @idempotent_id('bfcc074f-5e1c-4b45-8a2a-857239f8acb0')
    def test_update_config_root(self):
        """
        test method for update config root service objects
        """
        config_root = self._create_config_root()
        config_root_uuid = config_root['config-root']['uuid']
        updated_name = data_utils.rand_name('new_config_root')
        with self.rbac_utils.override_role(self):
            self.config_client.update_config_root(
                config_root_uuid, display_name=updated_name)

    @decorators.idempotent_id('4234d8dd-5bbf-4d3d-8e2f-0c2a1a3f0e03')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_config_roots"])
    @idempotent_id('316e7425-8fb0-41b4-9080-a76697abbafa')
    def test_list_config_roots(self):
        """
        test method for list config root service objects
        """
        with self.rbac_utils.override_role(self):
            self.config_client.list_config_roots()


class GlobalSystemConfigTest(rbac_base.BaseContrailTest):

    """
    Test class to test config node objects using RBAC roles
    """

    def _create_global_system_config(self):
        config_name = data_utils.rand_name('test-config')
        parent_type = 'config-root'
        config_fq_name = [config_name]
        new_config = \
            self.config_client.create_global_system_configs(
                parent_type=parent_type,
                display_name=config_name,
                fq_name=config_fq_name)['global-system-config']
        self.addCleanup(self._try_delete_resource,
                        (self.config_client.
                         delete_global_system_config),
                        new_config['uuid'])
        return new_config

    @decorators.idempotent_id('774a814a-973e-44b6-8653-ceff86c90a45')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_global_system_configs"])
    @idempotent_id('d1d189a7-14c1-49c5-b180-cd42ed2ca123')
    def test_list_global_system_configs(self):
        """
        test method for list global system config service objects
        """
        with self.rbac_utils.override_role(self):
            self.config_client.list_global_system_configs()

    @decorators.idempotent_id('177b82c4-7884-4a27-a134-4b45fb3cf237')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_global_system_configs"])
    @idempotent_id('e0ba6a20-3e28-47ac-bf95-9a848fcee49a')
    def test_create_global_sys_configs(self):
        """
        test method for create global system config service objects
        """
        with self.rbac_utils.override_role(self):
            self._create_global_system_config()

    @decorators.idempotent_id('ff9637ca-e4e8-4381-a62e-b799716ec845')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_global_system_config"])
    @idempotent_id('4b9f9131-cb34-4b7d-9d06-c6aca85cce3a')
    def test_show_global_system_config(self):
        """
        test method for show global system config service objects
        """
        new_config = self._create_global_system_config()
        with self.rbac_utils.override_role(self):
            self.config_client.show_global_system_config(
                new_config['uuid'])

    @decorators.idempotent_id('cec2ca37-ff71-4311-a8aa-6459b46dba7c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_global_system_config"])
    @idempotent_id('4f90dc83-da59-45a4-8ab6-b387bd6c2df4')
    def test_update_global_sys_config(self):
        """
        test method for update global system config service objects
        """
        new_config = self._create_global_system_config()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.config_client.update_global_system_config(
                new_config['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('3019ef0e-601c-4c7b-b709-a634a6ad0702')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_global_system_config"])
    @idempotent_id('fce1653c-e657-4a1e-8ced-7e02d297d6c9')
    def test_delete_global_sys_config(self):
        """
        test method for delete global system config service objects
        """
        new_config = self._create_global_system_config()
        with self.rbac_utils.override_role(self):
            self.config_client.delete_global_system_config(
                new_config['uuid'])
