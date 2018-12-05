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
Tempest test-case to test forwarding class objects using RBAC roles
"""

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF
LOG = logging.getLogger(__name__)


class ContrailForwardingClassTest(rbac_base.BaseContrailTest):

    """
    Test class to test Forwarding class objects using RBAC roles
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

    def _create_qos_global_configs(self, global_system_config):
        name = data_utils.rand_name('test-rbac-qos-global-config')
        parent_type = 'global-system-config'
        fq_name = [global_system_config, name]
        qos_global_config = self.qos_client.create_global_qos_configs(
            fq_name=fq_name,
            parent_type=parent_type)['global-qos-config']

        self.addCleanup(self._try_delete_resource,
                        self.qos_client.delete_global_qos_config,
                        qos_global_config['uuid'])
        return qos_global_config

    def _create_forwarding_class(self,
                                 global_system_config,
                                 global_qos_config):
        display_name = data_utils.rand_name('forwarding-class')
        parent_type = 'global-qos-config'
        fq_name = [global_system_config, global_qos_config, "1"]
        forwarding_class_id = data_utils.rand_int_id(1, 200)
        post_data = {
            'fq_name': fq_name,
            'parent_type': parent_type,
            'display_name': display_name,
            'forwarding_class_id': forwarding_class_id
        }
        new_fclass = self.forwarding_class_client.create_forwarding_classs(
            **post_data)['forwarding-class']
        self.addCleanup(self._try_delete_resource,
                        self.forwarding_class_client.delete_forwarding_class,
                        new_fclass['uuid'])
        return new_fclass

    @decorators.idempotent_id('88d84616-ce8d-46df-915f-90b560f88a4a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_forwarding_classs"])
    @idempotent_id('807a66fd-d4a4-472c-a13d-7ba590509e6e')
    def test_list_forwarding_classs(self):
        """
        test method for list forwarding classes objects
        """
        with self.rbac_utils.override_role(self):
            self.forwarding_class_client.list_forwarding_classs()

    @decorators.idempotent_id('73b015a3-e57b-4c48-9f05-8c2453f06092')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_forwarding_class"])
    @idempotent_id('8ef21f71-72a4-4de9-af93-6e759aa463c0')
    def test_show_forwarding_class(self):
        """
        test method for show forwarding classes objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        # Create a global qos config
        global_qos_config = \
            self._create_qos_global_configs(global_system_config)['name']
        new_fclass = self._create_forwarding_class(global_system_config,
                                                   global_qos_config)
        with self.rbac_utils.override_role(self):
            self.forwarding_class_client.show_forwarding_class(
                new_fclass['uuid'])

    @decorators.idempotent_id('8b1b3121-1f98-463c-8d39-7b750ef64254')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_forwarding_classs"])
    @idempotent_id('d098859c-ad36-4385-8fb0-c00934a99b6f')
    def test_create_forwarding_classs(self):
        """
        test method for create forwarding classes objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        # Create a global qos config
        global_qos_config = \
            self._create_qos_global_configs(global_system_config)['name']
        with self.rbac_utils.override_role(self):
            self._create_forwarding_class(global_system_config,
                                          global_qos_config)

    @decorators.idempotent_id('9c6d7400-d5dd-42b2-8e85-b056fd9f7596')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_forwarding_class"])
    @idempotent_id('589dc03d-a25d-48be-9d9c-d3f92ff2cfc6')
    def test_update_forwarding_class(self):
        """
        test method for update forwarding classes objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        # Create a global qos config
        global_qos_config = \
            self._create_qos_global_configs(global_system_config)['name']
        new_fclass = self._create_forwarding_class(global_system_config,
                                                   global_qos_config)
        update_name = data_utils.rand_name('updated_fclass')
        with self.rbac_utils.override_role(self):
            self.forwarding_class_client.update_forwarding_class(
                new_fclass['uuid'], display_name=update_name)

    @decorators.idempotent_id('c5349bc1-4d7a-44e4-8248-754a38865b19')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_forwarding_class"])
    @idempotent_id('a0348ffc-68c5-4d94-ba03-d08483503ced')
    def test_delete_forwarding_class(self):
        """
        test method for delete forwarding classes objects
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        # Create a global qos config
        global_qos_config = \
            self._create_qos_global_configs(global_system_config)['name']
        new_fclass = self._create_forwarding_class(global_system_config,
                                                   global_qos_config)
        with self.rbac_utils.override_role(self):
            self.forwarding_class_client.delete_forwarding_class(
                new_fclass['uuid'])
