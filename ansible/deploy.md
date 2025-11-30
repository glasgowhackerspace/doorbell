# Automated deployment with Ansible

1. Ensure you have Ansible installed on your computer 'control node'. See: [ansible docs](https://docs.ansible.com/projects/ansible/latest/installation_guide/intro_installation.html)
2. Ensure you have root ssh access to your pi.
3. Update the [inventory](inventory) file with the IP address of your pi.
4. Run the setup playbook `ansible-playbook -i inventory main.yml`