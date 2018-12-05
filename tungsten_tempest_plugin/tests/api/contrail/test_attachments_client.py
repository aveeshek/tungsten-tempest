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
Tempest test-case to test attachment clients objects using RBAC roles
"""


from tungsten_tempest_plugin.tests.api.contrail import rbac_base

from patrole_tempest_plugin import rbac_rule_validation

from tempest import config
from tempest.lib import decorators
from tempest.lib.common.utils import data_utils
from tempest.lib.decorators import idempotent_id

CONF = config.CONF


class AttachmentsClientTest(rbac_base.BaseContrailTest):

    """
    Test class to test attachment client objects using RBAC roles
    """

    def _create_provider_attachments(self):
        provider_name = data_utils.rand_name('test-provider-attachment')
        fq_name = [provider_name]
        post_body = {'display_name': provider_name, 'fq_name': fq_name}
        new_provider = \
            self.attachments_client.create_provider_attachments(
                **post_body)['provider-attachment']
        self.addCleanup(self._try_delete_resource,
                        (self.attachments_client.
                         delete_provider_attachment),
                        new_provider['uuid'])
        return new_provider

    def _create_customer_attachments(self):
        customer_name = data_utils.rand_name('test-customer-attachment')
        customer_fq_name = [customer_name]
        new_customer = \
            self.attachments_client.create_customer_attachments(
                display_name=customer_name,
                fq_name=customer_fq_name)['customer-attachment']
        self.addCleanup(self._try_delete_resource,
                        (self.attachments_client.
                         delete_customer_attachment),
                        new_customer['uuid'])
        return new_customer

    @decorators.idempotent_id('67cdef12-9f9d-43ab-a9c1-332295e09036')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_provider_attachments"])
    @idempotent_id('961dbf54-ae4f-42e8-9d27-69fa7df39013')
    def test_list_provider_attachments(self):
        """
        test method for list provider attachment objects
        """
        with self.rbac_utils.override_role(self):
            self.attachments_client.list_provider_attachments()

    @decorators.idempotent_id('821222e5-eea5-4980-8495-30ba3c7bdcf8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_provider_attachments"])
    @idempotent_id('73ad032e-3e81-4dcc-be55-1987484207cd')
    def test_create_providerattach(self):
        """
        test method for create provider attachment objects
        """
        with self.rbac_utils.override_role(self):
            self._create_provider_attachments()

    @decorators.idempotent_id('e47d427d-c77a-49e5-9cb2-c0cc7b616d6a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_provider_attachment"])
    @idempotent_id('7b5278bc-dd79-495a-9f74-448c04f52bd2')
    def test_show_provider_attachment(self):
        """
        test method for delete provider attachment objects
        """
        new_provider = self._create_provider_attachments()
        with self.rbac_utils.override_role(self):
            self.attachments_client.show_provider_attachment(
                new_provider['uuid'])

    @decorators.idempotent_id('d2d4aad4-08f8-4781-aec9-ede9aea6312a')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_provider_attachment"])
    @idempotent_id('3516ff99-eddf-4932-afa4-433a43a0e5ac')
    def test_update_provider_attachment(self):
        """
        test method for update provider attachment objects
        """
        new_provider = self._create_provider_attachments()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.attachments_client.update_provider_attachment(
                new_provider['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('65b5f6ca-9eaa-451d-b20a-a0f7fbbd1622')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_provider_attachment"])
    @idempotent_id('234d5505-2abf-418b-b43b-ea6f5a724fd3')
    def test_delete_provider_attachment(self):
        """
        test method for delete provider attachment objects
        """
        new_provider = self._create_provider_attachments()
        with self.rbac_utils.override_role(self):
            self.attachments_client.delete_provider_attachment(
                new_provider['uuid'])

    @decorators.idempotent_id('26f459c0-942c-4152-b0eb-16cfec2ee764')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_customer_attachments"])
    @idempotent_id('3eca8fd8-ec3c-4a0e-8f62-b15d28796b7f')
    def test_list_customer_attachments(self):
        """
        test method for list customer attachment objects
        """
        with self.rbac_utils.override_role(self):
            self.attachments_client.list_customer_attachments()

    @decorators.idempotent_id('67faa58a-fc42-4ba8-b67e-39213f9a372f')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_customer_attachments"])
    @idempotent_id('53f93053-554c-4202-b763-0230d9a0553a')
    def test_create_customerattachments(self):
        """
        test method for create customer attachment objects
        """
        with self.rbac_utils.override_role(self):
            self._create_customer_attachments()

    @decorators.idempotent_id('b8badd01-5197-4b3e-93ed-b68c19eb890e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_customer_attachment"])
    @idempotent_id('c6671540-695c-4cba-bcee-4a5d1cddd412')
    def test_show_customer_attachment(self):
        """
        test method for show customer attachment objects
        """
        new_customer = self._create_customer_attachments()
        with self.rbac_utils.override_role(self):
            self.attachments_client.show_customer_attachment(
                new_customer['uuid'])

    @decorators.idempotent_id('6d6aeb09-9589-4ec4-811e-66cf1920bde5')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_customer_attachment"])
    @idempotent_id('50419cca-dd03-4d02-9c06-88446647fcba')
    def test_update_customer_attachment(self):
        """
        test method for update customer attachment objects
        """
        new_customer = self._create_customer_attachments()
        update_name = data_utils.rand_name('test')
        with self.rbac_utils.override_role(self):
            self.attachments_client.update_customer_attachment(
                new_customer['uuid'],
                display_name=update_name)

    @decorators.idempotent_id('5126eff2-e9e8-424f-b842-f923c704e069')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_customer_attachment"])
    @idempotent_id('5385c275-8e86-4739-9cb6-d1e0ed522807')
    def test_delete_customer_attachment(self):
        """
        test method for delete customer attachment objects
        """
        new_customer = self._create_customer_attachments()
        with self.rbac_utils.override_role(self):
            self.attachments_client.delete_customer_attachment(
                new_customer['uuid'])
