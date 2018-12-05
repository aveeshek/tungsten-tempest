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
Tempest test-case to test project objects using RBAC roles
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


class ProjectContrailTest(rbac_base.BaseContrailTest):

    """
    Test class to test project objects using RBAC roles
    """

    def _create_project(self):
        fq_name = data_utils.rand_name('project')
        post_body = {
            'parent_type': 'domain',
            'fq_name': ['default-domain', fq_name]
        }
        resp_body = self.project_client.create_projects(
            **post_body)
        project_uuid = resp_body['project']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.project_client.delete_project,
                        project_uuid)
        return project_uuid

    def _update_project(self, project_uuid):
        put_body = {
            'display_name': data_utils.rand_name('project')
        }
        self.project_client.update_project(project_uuid, **put_body)

    @decorators.idempotent_id('b1afccc4-6947-444f-9dca-1422f22ad6a9')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_projects"])
    @idempotent_id('7db819fd-ceee-4a6b-9ad7-2e837c055bdd')
    def test_list_projects(self):
        """
        test method for list project objects
        """
        with self.rbac_utils.override_role(self):
            self.project_client.list_projects()

    @decorators.idempotent_id('f29f5705-9bd6-4d50-b8c4-f3450cac24d9')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_projects"])
    @idempotent_id('38b9b7a8-1568-417d-b0a3-e7adee88e4b9')
    def test_create_projects(self):
        """
        test method for create project objects
        """
        with self.rbac_utils.override_role(self):
            self._create_project()

    @decorators.idempotent_id('5f71a9be-4e4e-4eff-82ee-bd15b1fb0525')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_project"])
    @idempotent_id('c47e57c4-34b0-46c2-a678-83b1fe9afd25')
    def test_show_project(self):
        """
        test method for show project objects
        """
        project_uuid = self._create_project()
        with self.rbac_utils.override_role(self):
            self.project_client.show_project(project_uuid)

    @decorators.idempotent_id('89f5c981-67e3-4388-a724-6debd7b759e7')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_project"])
    @idempotent_id('3d4bd416-16cc-437c-9e95-f9ceda424f8b')
    def test_update_project(self):
        """
        test method for update project objects
        """
        project_uuid = self._create_project()
        with self.rbac_utils.override_role(self):
            self._update_project(project_uuid)

    @decorators.idempotent_id('8e0329c1-5316-4e94-a8e4-16ed329480b8')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_project"])
    @idempotent_id('787ebe8b-b88d-4488-b157-f70554bdd783')
    def test_delete_project(self):
        """
        test method for delete project objects
        """
        project_uuid = self._create_project()
        with self.rbac_utils.override_role(self):
            self.project_client.delete_project(project_uuid)
