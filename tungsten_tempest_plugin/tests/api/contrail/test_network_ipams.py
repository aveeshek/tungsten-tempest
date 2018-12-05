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
Tempest test-case to test network ipam objects using RBAC roles
"""

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class NetworkIpamsTest(rbac_base.BaseContrailTest):

    """
    Test class to test network ipam objects using RBAC roles
    """

    def _create_network_ipams(self):
        ipam_name = data_utils.rand_name('test-ipam')
        ipam_fq_name = ['default-domain', self.tenant_name, ipam_name]
        new_ipam = self.network_ipams_client.create_network_ipams(
            parent_type='project',
            fq_name=ipam_fq_name)['network-ipam']
        self.addCleanup(self._try_delete_resource,
                        self.network_ipams_client.delete_network_ipam,
                        new_ipam['uuid'])
        return new_ipam

    @decorators.idempotent_id('53a9505e-6201-48c3-b457-762d360977fd')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_network_ipams"])
    @idempotent_id('9ee2c4d8-3209-4ef8-86e1-0ecea2d4c5f2')
    def test_list_network_ipams(self):
        """
        test method for list n/w ipam objects
        """
        with self.rbac_utils.override_role(self):
            self.network_ipams_client.list_network_ipams()

    @decorators.idempotent_id('05790aae-b95e-4e19-9c40-daee94ce869c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_network_ipams"])
    @idempotent_id('ef2415ea-0810-413a-85a0-4508c9d7af91')
    def test_create_network_ipams(self):
        """
        test method for create n/w ipam objects
        """
        with self.rbac_utils.override_role(self):
            self._create_network_ipams()

    @decorators.idempotent_id('b91ad50e-98c1-4103-9532-54128cacd0a3')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_network_ipam"])
    @idempotent_id('527b19e5-068a-44e3-b175-b504eafeec6e')
    def test_show_network_ipam(self):
        """
        test method for show n/w ipam objects
        """
        new_ipam = self._create_network_ipams()
        with self.rbac_utils.override_role(self):
            self.network_ipams_client.show_network_ipam(new_ipam['uuid'])

    @decorators.idempotent_id('7c062754-212c-4585-ab4a-81539130e4fb')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_network_ipam"])
    @idempotent_id('118c1620-efb6-4cc6-8eb5-71bf8631d365')
    def test_delete_network_ipam(self):
        """
        test method for delete n/w ipam objects
        """
        new_ipam = self._create_network_ipams()
        with self.rbac_utils.override_role(self):
            self.network_ipams_client.delete_network_ipam(new_ipam['uuid'])

    @decorators.idempotent_id('fd9264de-6c91-4a4e-8f91-12798ebd4fe7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_network_ipam"])
    @idempotent_id('44cbe2d9-583d-4215-964a-1c321f5e8d92')
    def test_update_network_ipam(self):
        """
        test method for update n/w ipam objects
        """
        new_ipam = self._create_network_ipams()
        with self.rbac_utils.override_role(self):
            self.network_ipams_client.update_network_ipam(
                new_ipam['uuid'],
                display_name=data_utils.rand_name('test-ipam'))
