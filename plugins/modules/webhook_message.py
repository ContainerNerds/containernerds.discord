#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2021, Anthony Loukinas <anthony@containernerds.com>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = """
module: webhook_message
short_description: Send Discord notifications using Webhooks
description:
    - The C(discord) module sends notifications to U(http://discordapp.com) via the Incoming WebHook integration
author: "Anthony Loukinas (@anthonyloukinas)"
options:
  webhook:
    type: str
    required: true
    description:
      - Discord webook url. This authenticates you to the discord service.
        Make sure to use keep this private.
  msg:
    type: str
    required: true
    description:
      - Message to send. Note that the module does not handle escaping characters.
        Plain-text angle brackets and ampersands should be converted to HTML entities (e.g. & to &amp;) before sending.
  username:
    type: str
    description:
      - This is the sender of the message.
    default: "Ansible"
  avatar_url:
    type: str
    description:
      - Url for the message sender's icon (default C(https://www.ansible.com/favicon.ico))
    default: https://www.ansible.com/favicon.ico
"""

EXAMPLES = """
- name: Send notification message via Slack
  containernerds.discord.webhook_message:
    token: thetoken/generatedby/slack
    msg: '{{ inventory_hostname }} completed'
  delegate_to: localhost
"""
import traceback

try:
    import re
    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils.urls import fetch_url
except ImportError:
    HAS_ANOTHER_LIBRARY = False
    ANOTHER_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_ANOTHER_LIBRARY = True


def build_payload_for_discord(module, msg, username, avatar_url):
    payload = {}

    if msg is not None:
        payload['content'] = msg
    if username is not None:
        payload['username'] = username
    if avatar_url is not None:
        payload['avatar_url'] = avatar_url

    return payload


def do_notify_discord(module, webhook, payload):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = module.jsonify(payload)

    response, info = fetch_url(module=module, url=webhook, headers=headers, method='POST', data=data)

    if info['status'] != 204:
        module.fail_json(msg=" failed to send message", status=info['status'])

    return(['webhook', 'ok'])


def main():
    module = AnsibleModule(
        argument_spec=dict(
            webhook=dict(type='str', required=True, no_log=True),
            msg=dict(type='str', required=True),
            username=dict(type='str', required=False, default="Ansible"),
            avatar_url=dict(type='str', required=False, default="https://www.ansible.com/favicon.ico")
        ),
        supports_check_mode=True,
    )

    if not HAS_ANOTHER_LIBRARY:
        module.fail_json(msg="missing lib", exception=ANOTHER_LIBRARY_IMPORT_ERROR)

    webhook = module.params['webhook']
    msg = module.params['msg']
    username = module.params['username']
    avatar_url = module.params['avatar_url']

    changed = True

    payload = build_payload_for_discord(module, msg, username, avatar_url)
    discord_response = do_notify_discord(module, webhook, payload)

    module.exit_json(msg="OK", changed=changed)


if __name__ == '__main__':
    main()
