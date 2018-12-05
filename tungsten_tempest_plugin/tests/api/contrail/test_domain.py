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
Tempest test-case to test domain objects using RBAC roles
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


class DomainContrailTest(rbac_base.BaseContrailTest):

    """
    Test class to test domain objects using RBAC roles
    """

    def _create_domains(self):
        fq_name = data_utils.rand_name('domain')
        post_body = {
            'fq_name': [fq_name]
        }
        resp_body = self.domain_client.create_domains(
            **post_body)
        domain_uuid = resp_body['domain']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.domain_client.delete_domain,
                        domain_uuid)
        return domain_uuid

    def _update_domain(self, domain_uuid):
        put_body = {
            'display_name': data_utils.rand_name('domain')
        }
        self.domain_client.update_domain(domain_uuid, **put_body)

    @decorators.idempotent_id('d9db33f3-b326-47d9-972e-9f6ca33d94cb')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_domains"])
    @idempotent_id('fa02e27b-f661-4186-a522-69e8fcb6abf9')
    def test_list_domains(self):
        """
        test method for list domain objects
        """
        with self.rbac_utils.override_role(self):
            self.domain_client.list_domains()

    @decorators.idempotent_id('32a12708-7209-4d8a-8096-96867acff917')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_domains"])
    @idempotent_id('3f18be91-c37b-4e17-bf5e-b704d993f738')
    def test_create_domains(self):
        """
        test method for create domain objects
        """
        with self.rbac_utils.override_role(self):
            self._create_domains()

    @decorators.idempotent_id('8eb9d91b-21b0-443c-af70-88dda1c21c03')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_domain"])
    @idempotent_id('e79f8581-ba9f-420a-aa26-f1cb51cf4bbf')
    def test_show_domain(self):
        """
        test method for show domain objects
        """
        domain_uuid = self._create_domains()
        with self.rbac_utils.override_role(self):
            self.domain_client.show_domain(domain_uuid)

    @decorators.idempotent_id('7f0f1fac-2685-4405-9c83-6dee210dfab0')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_domain"])
    @idempotent_id('fdf72539-20b5-4bdb-b22b-70c86fbb52a4')
    def test_update_domain(self):
        """
        test method for update domain objects
        """
        domain_uuid = self._create_domains()
        with self.rbac_utils.override_role(self):
            self._update_domain(domain_uuid)

    @decorators.idempotent_id('2439c2fa-5102-4e63-9c4d-834743643fd6')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_domain"])
    @idempotent_id('abaad2b0-6bde-40b8-b257-20ca805c1dca')
    def test_delete_domain(self):
        """
        test method for delete domain objects
        """
        domain_uuid = self._create_domains()
        with self.rbac_utils.override_role(self):
            self.domain_client.delete_domain(domain_uuid)
