# containernerds.discord
Ansible Collection to allow communication to Discord from Ansible.

# Usage
```yml
---
- hosts: localhost
  tasks:
    - name: Send Discord Message
      containernerds.discord.webhook_message:
        msg: "Intergration Test"
        webhook: "Discord Webhook https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks"
```
