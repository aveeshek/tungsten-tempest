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
Tempest test-case to test Alias IP and IP pools objects using RBAC roles
"""

from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class AliasIPsTest(rbac_base.BaseContrailTest):
    """
    Test class to test Alias IP and IP pools objects using RBAC roles
    """

    @classmethod
    def resource_setup(cls):
        super(AliasIPsTest, cls).resource_setup()
        # Create project
        project_name = data_utils.rand_name('test-project')
        project_fq_name = ['default-domain', project_name]
        cls.project = cls.project_client.create_projects(
            parent_type='domain',
            fq_name=project_fq_name)['project']

        # Create network ipam
        ipam_name = data_utils.rand_name('test-ipam')
        ipam_fq_name = ['default-domain', cls.project['name'], ipam_name]
        subnet_info = [{'subnet': {'ip_prefix': '2.2.3.0',
                                   'ip_prefix_len': 24}}]
        cls.ipam = cls.network_ipams_client.create_network_ipams(
            parent_type='project',
            fq_name=ipam_fq_name)['network-ipam']

        # Create network
        net_name = data_utils.rand_name('test-net')
        net_fq_name = ['default-domain', cls.project['name'], net_name]
        net_ipam_refs = [
            {
                'to': cls.ipam['fq_name'],
                'href': cls.ipam['href'],
                'uuid': cls.ipam['uuid'],
                'attr': {
                    'ipam_subnets': subnet_info
                }
            }
        ]
        cls.network = cls.vn_client.create_virtual_networks(
            parent_type='project',
            fq_name=net_fq_name,
            network_ipam_refs=net_ipam_refs)['virtual-network']

    @classmethod
    def resource_cleanup(cls):
        cls._try_delete_resource(cls.vn_client.delete_virtual_network,
                                 cls.network['uuid'])
        cls._try_delete_resource(cls.network_ipams_client.delete_network_ipam,
                                 cls.ipam['uuid'])
        cls._try_delete_resource(cls.project_client.delete_project,
                                 cls.project['uuid'])
        super(AliasIPsTest, cls).resource_cleanup()

    def _create_alias_ip_pools(self):
        alias_ip_pool_name = data_utils.rand_name('test-alias-ip-pool')
        alias_ip_pool_fq_name = ['default-domain', self.project['name'],
                                 self.network['name'], alias_ip_pool_name]
        new_alias_ip_pool = self.alias_ip_client.create_alias_ip_pools(
            fq_name=alias_ip_pool_fq_name,
            parent_type='virtual-network')['alias-ip-pool']

        self.addCleanup(self._try_delete_resource,
                        self.alias_ip_client.delete_alias_ip_pool,
                        new_alias_ip_pool['uuid'])
        return new_alias_ip_pool

    def _create_alias_ips(self, alias_ip_pool, address):
        alias_ip_name = data_utils.rand_name('test-alias-ip')
        alias_ip_fq_name = alias_ip_pool['fq_name']
        alias_ip_fq_name.append(alias_ip_name)
        alias_ip_project_ref = [
            {
                'to': self.project['fq_name'],
                'href': self.project['href'],
                'uuid': self.project['uuid'],
            }
        ]
        new_alias_ip = self.alias_ip_client.create_alias_ips(
            fq_name=alias_ip_fq_name,
            parent_type='alias-ip-pool',
            project_refs=alias_ip_project_ref,
            alias_ip_address=address)['alias-ip']
        self.addCleanup(self._try_delete_resource,
                        self.alias_ip_client.delete_alias_ip,
                        new_alias_ip['uuid'])
        return new_alias_ip

    @decorators.idempotent_id('ad82cd15-1d18-4ee9-9f4e-8653b27ff68d')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_alias_ips"])
    @idempotent_id('899d6824-0755-41ef-adef-03eb1858bcb0')
    def test_list_alias_ips(self):
        """
        test method for list alias IP
        """
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.list_alias_ips()

    @decorators.idempotent_id('aae9af3b-ebb8-426e-afde-59a655352dfa')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_alias_ips"])
    @idempotent_id('bc9aae29-22a8-4eed-a31f-c0ded300e3a3')
    def test_create_alias_ips(self):
        """
        test method for create alias IP
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        with self.rbac_utils.override_role(self):
            self._create_alias_ips(new_alias_ip_pool, '2.2.3.1')

    @decorators.idempotent_id('0d7785ab-63d6-4695-b2e1-d43706f166ed')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_alias_ip"])
    @idempotent_id('d20318b1-c204-44e7-a44c-66f6a1fbe7a0')
    def test_show_alias_ip(self):
        """
        test method for show alias IP
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        new_alias_ip = self._create_alias_ips(new_alias_ip_pool, '2.2.3.2')
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.show_alias_ip(
                new_alias_ip['uuid'])

    @decorators.idempotent_id('12577013-4194-439b-b598-f83aedbc4f0f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_alias_ip"])
    @idempotent_id('c237b18f-d899-4b80-8e9b-068244a24612')
    def test_update_alias_ip(self):
        """
        test method for update alias IP
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        new_alias_ip = self._create_alias_ips(new_alias_ip_pool, '2.2.3.3')
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.update_alias_ip(
                new_alias_ip['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('31ed2a1b-48e1-44d0-bf21-304d7fb4a0ac')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_alias_ip"])
    @idempotent_id('456c641c-9066-4125-8dec-d1529ad8f1ba')
    def test_delete_alias_ip(self):
        """
        test method for delete alias IP
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        new_alias_ip = self._create_alias_ips(new_alias_ip_pool, '2.2.3.4')
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.delete_alias_ip(
                new_alias_ip['uuid'])

    @decorators.idempotent_id('a46c088a-9b3b-4a88-9df6-d0cc41d32bf4')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_alias_ip_pools"])
    @idempotent_id('ffe85f35-589a-4b90-a1d3-6aed92a85954')
    def test_list_alias_ip_pools(self):
        """
        est method for list alias IP pools
        """
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.list_alias_ip_pools()

    @decorators.idempotent_id('5ac92620-24af-4948-bc9f-5c43f0e65e9d')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_alias_ip_pools"])
    @idempotent_id('83abd2c0-d46a-4337-87d0-31cdb86e4226')
    def test_create_alias_ip_pools(self):
        """
        test method for create alias IP pool
        """
        with self.rbac_utils.override_role(self):
            self._create_alias_ip_pools()

    @decorators.idempotent_id('1e8f4d95-bf80-4383-bce7-e9460214264a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_alias_ip_pool"])
    @idempotent_id('a1cbe111-ccba-4fa4-ba59-7d1ee08a15db')
    def test_show_alias_ip_pool(self):
        """
        test method for show alias IP pool
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.show_alias_ip_pool(
                new_alias_ip_pool['uuid'])

    @decorators.idempotent_id('ece84364-c139-42f1-b2ab-8adad9fe11a4')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_alias_ip_pool"])
    @idempotent_id('7f3448d7-22f1-4808-b3eb-15eeb3f079aa')
    def test_update_alias_ip_pool(self):
        """
        test method for update alias IP pool
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.update_alias_ip_pool(
                new_alias_ip_pool['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('aabbbff0-e8f8-4dc9-9e77-5c3cc390cc14')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_alias_ip_pool"])
    @idempotent_id('f59ea4fb-d10f-40c8-a8fa-dcd948ca89c8')
    def test_delete_alias_ip_pool(self):
        """
        test method for delete alias IP pool
        """
        new_alias_ip_pool = self._create_alias_ip_pools()
        with self.rbac_utils.override_role(self):
            self.alias_ip_client.delete_alias_ip_pool(
                new_alias_ip_pool['uuid'])
