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
Tempest test-case to test QoS config objects using RBAC roles
"""

from oslo_log import log as logging

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

LOG = logging.getLogger(__name__)
CONF = config.CONF


class QosConfigContrailTest(rbac_base.BaseContrailTest):

    """
    Test class to test QoS config objects using RBAC roles
    """

    def _delete_qos_config(self, qos_config_id):
        self.qos_client.delete_qos_config(qos_config_id)

    def _create_qos_configs(self):
        name = data_utils.rand_name('test-rbac-qos-config')
        parent_type = 'project'
        fq_name = ['default-domain', self.tenant_name, name]
        qos_config = self.qos_client.create_qos_configs(
            fq_name=fq_name,
            parent_type=parent_type)['qos-config']
        self.addCleanup(self._try_delete_resource,
                        self._delete_qos_config,
                        qos_config['uuid'])
        return qos_config

    @decorators.idempotent_id('53533827-08f1-4dbf-83c1-9e74b44d7103')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_qos_configs"])
    @idempotent_id('6bc44b34-14d4-4e0e-b45d-fe3df047879f')
    def test_list_qos_configs(self):
        """
        test method for list QoS config objects
        """
        self._create_qos_configs()
        with self.rbac_utils.override_role(self):
            self.qos_client.list_qos_configs()

    @decorators.idempotent_id('6ea49847-17eb-4cd7-8bb0-0eb9210593fe')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_qos_configs"])
    @idempotent_id('031b4a27-22cd-4d93-938d-ba6d0f3163ba')
    def test_create_qos_configs(self):
        """
        test method for create QoS config objects
        """
        with self.rbac_utils.override_role(self):
            self._create_qos_configs()

    @decorators.idempotent_id('2d2ebdbc-ccf4-44e9-8257-0dc2cb35632a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_qos_config"])
    @idempotent_id('a9d82b49-3492-4667-b252-ef30b0ee6eb3')
    def test_show_qos_config(self):
        """
        test method for show QoS config objects
        """
        qos_config = self._create_qos_configs()
        with self.rbac_utils.override_role(self):
            self.qos_client.show_qos_config(qos_config['uuid'])

    @decorators.idempotent_id('c1638a68-a758-4284-a763-a3b81bc1f6a8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_qos_config"])
    @idempotent_id('d324a5e6-cc86-4444-91a2-74592283a7ec')
    def test_delete_qos_config(self):
        """
        test method for delete QoS config objects
        """
        qos_config = self._create_qos_configs()
        with self.rbac_utils.override_role(self):
            self.qos_client.delete_qos_config(qos_config['uuid'])

    @decorators.idempotent_id('53649c15-c159-4763-9b55-1dfa2029a8d2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_qos_config"])
    @idempotent_id('7f1901a5-0cf0-40bd-98a5-f8a930b11cfe')
    def test_update_qos_config(self):
        """
        test method for update QoS config objects
        """
        qos_config = self._create_qos_configs()
        display_name = data_utils.rand_name('qos_config')
        with self.rbac_utils.override_role(self):
            self.qos_client.update_qos_config(
                qos_config_id=qos_config['uuid'],
                display_name=display_name)
