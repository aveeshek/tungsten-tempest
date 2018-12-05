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
Tempest test-case to test discovery service assignment objects using RBAC roles
"""

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class DiscoveryServiceAssignmentTest(rbac_base.BaseContrailTest):

    """
    Test class to test discovery service assignment objects using RBAC roles
    """

    def _create_discovery_service_assignments(self):
        dsa_name = [data_utils.rand_name('test-dsa')]
        new_dsa = self.dsa_client.create_ds_assignments(
            fq_name=dsa_name)['discovery-service-assignment']

        self.addCleanup(self._try_delete_resource,
                        self.dsa_client.delete_ds_assignment,
                        new_dsa['uuid'])
        return new_dsa

    @decorators.idempotent_id('2a97b185-3c1a-4fe8-b073-9f8f9018c540')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_discovery_service_assignments"])
    @idempotent_id('9ac1e4ca-8983-403f-b644-7758935f2f36')
    def test_list_discovery_service(self):
        """
        test method for list discovery service assignment objects
        """
        with self.rbac_utils.override_role(self):
            self.dsa_client.list_ds_assignments()

    @decorators.idempotent_id('f6c90c82-6731-4580-af3b-aaeb6f8cc2b7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_discovery_service_assignments"])
    @idempotent_id('40ad1208-a039-4809-8516-41b4dfcbd00c')
    def test_create_discovery_service(self):
        """
        test method for create discovery service assignment objects
        """
        with self.rbac_utils.override_role(self):
            self._create_discovery_service_assignments()

    @decorators.idempotent_id('0612ad3e-40a6-41bd-a2be-64e5f4d134a7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_discovery_service_assignment"])
    @idempotent_id('63660fe9-22b8-456c-a757-a7da1abfbce8')
    def test_show_discovery_service(self):
        """
        test method for show discovery service assignment objects
        """
        new_dsa = self._create_discovery_service_assignments()
        with self.rbac_utils.override_role(self):
            self.dsa_client.show_ds_assignment(new_dsa['uuid'])

    @decorators.idempotent_id('3b9193ad-fe66-4b16-8398-539da153aa72')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_discovery_service_assignment"])
    @idempotent_id('71ce1404-965b-4670-abb7-5b6fea3b24b7')
    def test_update_discovery_service(self):
        """
        test method for update discovery service assignment objects
        """
        new_dsa = self._create_discovery_service_assignments()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.dsa_client.update_ds_assignment(
                new_dsa['uuid'],
                fq_name=new_dsa['fq_name'],
                display_name=update_name)

    @decorators.idempotent_id('ecd4b3f7-21bf-4222-bb29-6c8202ba953f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_discovery_service_assignment"])
    @idempotent_id('e7ff845d-2140-4eb0-9720-26370459723b')
    def test_delete_discovery_service(self):
        """
        test method for delete discovery service assignment objects
        """
        new_dsa = self._create_discovery_service_assignments()
        with self.rbac_utils.override_role(self):
            self.dsa_client.delete_ds_assignment(
                new_dsa['uuid'])
