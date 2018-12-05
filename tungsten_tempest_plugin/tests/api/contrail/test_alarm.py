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
Tempest test-case to test Alarms object using RBAC roles
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


class AlarmContrailTest(rbac_base.BaseContrailTest):

    """
    Test class to test Alarm objects using RBAC roles
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

    def _create_alarm(self, global_system_config):
        post_body = {
            'fq_name': [global_system_config,
                        data_utils.rand_name('alarm')],
            'alarm_severity': 1,
            'parent_type': 'global-system-config',
            'uve_keys': {
                'uve_key': ['analytics_node']
            },
            'alarm_rules': {
                'or_list': [{
                    'and_list': [{
                        'operation': '!=',
                        'operand1': 'NodeStatus.process_info.process_state',
                        'operand2': {
                            'json_value': '"PROCESS_STATE_RUNNING"'
                        }
                    }]
                }]
            }
        }
        resp_body = self.alarm_client.create_alarms(
            **post_body)
        alarm_uuid = resp_body['alarm']['uuid']
        self.addCleanup(self._try_delete_resource,
                        self.alarm_client.delete_alarm,
                        alarm_uuid)
        return alarm_uuid

    def _update_alarm(self, alarm_uuid):
        put_body = {
            'alarm_severity': 2
        }
        self.alarm_client.update_alarm(alarm_uuid, **put_body)

    @decorators.idempotent_id('fdfc89f9-e919-4a81-966e-0aadaff4ce1c')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["list_alarms"])
    @idempotent_id('dc7d19dd-dd5e-4ec8-bf0c-c6d9d83a60a8')
    def test_list_alarms(self):
        """
        test method for list alarms
        """
        with self.rbac_utils.override_role(self):
            self.alarm_client.list_alarms()

    @decorators.idempotent_id('0e844c89-c7a3-4667-b996-e176d5ea460e')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["create_alarms"])
    @idempotent_id('7fe55d0c-e54a-4bb7-95a6-9c53f9e9c4bf')
    def test_create_alarms(self):
        """
        test method for create alarms
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        with self.rbac_utils.override_role(self):
            self._create_alarm(global_system_config)

    @decorators.idempotent_id('e787e656-44ad-4aa6-8644-4ab9a2f40b83')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["show_alarm"])
    @idempotent_id('ab0ccbe4-7bfe-4176-890a-d438ee04290d')
    def test_show_alarm(self):
        """
        test method for show alarms
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        alarm_uuid = self._create_alarm(global_system_config)
        with self.rbac_utils.override_role(self):
            self.alarm_client.show_alarm(alarm_uuid)

    @decorators.idempotent_id('c3160759-4a68-4272-90e7-a69aa0e711f6')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["update_alarm"])
    @idempotent_id('ab331cca-ee53-4106-9b30-7319bfb1bea7')
    def test_update_alarm(self):
        """
        test method for update alarms
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        alarm_uuid = self._create_alarm(global_system_config)
        with self.rbac_utils.override_role(self):
            self._update_alarm(alarm_uuid)

    @decorators.idempotent_id('11f2d137-4ad3-4c99-b0f9-9bde637722a2')
    @rbac_rule_validation.action(service="Contrail",
                                 rules=["delete_alarm"])
    @idempotent_id('84fadb14-77c0-4f21-b5b2-1da7a2fd27e6')
    def test_delete_alarm(self):
        """
        test method for delete alarms
        """
        # Create global system config
        global_system_config = self._create_global_system_config()['name']
        alarm_uuid = self._create_alarm(global_system_config)
        with self.rbac_utils.override_role(self):
            self.alarm_client.delete_alarm(alarm_uuid)
