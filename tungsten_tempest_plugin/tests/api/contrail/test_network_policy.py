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
Tempest test-case to test network policy objects using RBAC roles
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


class NetworkPolicyTest(rbac_base.BaseContrailTest):

    """
    Test class to test network policy objects using RBAC roles
    """

    def _create_policy(self):
        fq_name = data_utils.rand_name('network-policy')
        post_body = {
            'parent_type': 'project',
            'fq_name': ["default-domain", self.tenant_name, fq_name]
        }
        resp_body = self.network_policy_client.create_network_policys(
            **post_body)
        network_policy_uuid = resp_body['network-policy']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.network_policy_client.delete_network_policy,
                        network_policy_uuid)
        return network_policy_uuid

    def _update_policy(self, network_policy_uuid):
        put_body = {
            'display_name': data_utils.rand_name('network-policy')
        }
        self.network_policy_client.update_network_policy(network_policy_uuid,
                                                         **put_body)

    @decorators.idempotent_id('8f7cac43-758f-4e7f-99dc-c71d6b38c75a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_network_policys"])
    @idempotent_id('fa2a28f3-a8bb-4908-95b9-1e11cf58b16f')
    def test_list_policys(self):
        """
        test method for list n/w policy objects
        """
        with self.rbac_utils.override_role(self):
            self.network_policy_client.list_network_policys()

    @decorators.idempotent_id('7981c0be-ca0b-4d1f-9f92-c33aaa1d93c7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_network_policys"])
    @idempotent_id('a30be228-afba-40c9-8678-ae020db68d79')
    def test_create_network_policys(self):
        """
        test method for create n/w policy objects
        """
        with self.rbac_utils.override_role(self):
            self._create_policy()

    @decorators.idempotent_id('5f028687-0599-409f-a785-97b6d131f48b')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_network_policy"])
    @idempotent_id('6cefe92e-8936-49a6-bce0-12da3396e7ab')
    def test_show_network_policy(self):
        """
        test method for show n/w policy objects
        """
        policy_uuid = self._create_policy()
        with self.rbac_utils.override_role(self):
            self.network_policy_client.show_network_policy(policy_uuid)

    @decorators.idempotent_id('9a58b489-7600-4369-9b11-696ae46d8457')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_network_policy"])
    @idempotent_id('1d470505-3ad4-4870-87d7-3f0b0f9fc635')
    def test_update_network_policy(self):
        """
        test method for update n/w policy objects
        """
        policy_uuid = self._create_policy()
        with self.rbac_utils.override_role(self):
            self._update_policy(policy_uuid)

    @decorators.idempotent_id('acabbe91-6823-446f-9590-508655a57316')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_network_policy"])
    @idempotent_id('aae9018f-e7a2-4a75-a68e-afd6c380640e')
    def test_delete_network_policy(self):
        """
        test method for delete n/w policy objects
        """
        policy_uuid = self._create_policy()
        with self.rbac_utils.override_role(self):
            self.network_policy_client.delete_network_policy(policy_uuid)
