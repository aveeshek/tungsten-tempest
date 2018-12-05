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
Tempest test-case to test service group objects using RBAC roles
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


class ContrailSecurityGroupTest(rbac_base.BaseContrailTest):

    """
    Test class to test security group objects using RBAC roles
    """

    def _delete_security_group(self, sec_grp_id):
        return self.security_group_client.delete_security_group(sec_grp_id)

    def _create_security_groups(self):
        name = data_utils.rand_name('securitygroup')
        domain_name = 'default-domain'
        fq_name = ['default-domain', self.tenant_name, name]
        parent_type = 'project'
        sec_grp = self.security_group_client.create_security_groups(
            domain_name=domain_name,
            fq_name=fq_name,
            display_name=name,
            parent_type=parent_type)['security-group']
        self.addCleanup(self._try_delete_resource,
                        self._delete_security_group,
                        sec_grp['uuid'])
        return sec_grp

    @decorators.idempotent_id('d0dd9b3c-c303-443a-a07e-072242b2952d')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_security_groups"])
    @idempotent_id('a13cc1d5-f562-4b68-b732-980deb3cddf4')
    def test_list_security_groups(self):
        """
        test method for list security group objects
        """
        self._create_security_groups()
        with self.rbac_utils.override_role(self):
            self.security_group_client.list_security_groups()

    @decorators.idempotent_id('d7bc3044-83dd-4d8b-9010-028a95b45385')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_security_group"])
    @idempotent_id('c7ca1781-08ae-4fa2-bd6d-1f369950c4c4')
    def test_show_security_group(self):
        """
        test method for show security group objects
        """
        grp = self._create_security_groups()
        grp_id = grp['uuid']
        with self.rbac_utils.override_role(self):
            self.security_group_client.show_security_group(grp_id)

    @decorators.idempotent_id('19da2264-a5c0-46b5-92d8-5a1c6ab88d14')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_security_group"])
    @idempotent_id('e682d7b4-deb8-4b5c-9c9b-1e1ada827b40')
    def test_delete_security_group(self):
        """
        test method for delete security group objects
        """
        grp = self._create_security_groups()
        grp_id = grp['uuid']
        with self.rbac_utils.override_role(self):
            self._delete_security_group(grp_id)

    @decorators.idempotent_id('8f461d8b-298a-4f89-be5c-272aec14fb95')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_security_groups"])
    @idempotent_id('63a2ff14-7869-40a2-962a-d65752de5651')
    def test_create_security_groups(self):
        """
        test method for create security group objects
        """
        with self.rbac_utils.override_role(self):
            self._create_security_groups()

    @decorators.idempotent_id('056b5529-41e0-4d77-9c67-6ffc6e6bc2cb')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_security_group"])
    @idempotent_id('cf9aafe2-fffb-4028-8fd7-4d6634e144e7')
    def test_update_security_group(self):
        """
        test method for update security group objects
        """
        grp = self._create_security_groups()
        grp_id = grp['uuid']
        display_name = data_utils.rand_name('securitygroupnew')
        with self.rbac_utils.override_role(self):
            self.security_group_client.update_security_group(
                sec_group_id=grp_id,
                display_name=display_name)
