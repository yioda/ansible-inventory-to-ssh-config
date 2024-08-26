from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import datetime
from os.path import expanduser
from shutil import copyfile

from importlib.metadata import distribution
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from sshconf import empty_ssh_config_file, read_ssh_config_file


def get_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                        version=distribution('ansible-inventory-to-ssh-config').version)
    parser.add_argument("inventory_file", help="ansible inventory file")
    parser.add_argument("-o", "--output",
                        help="ssh config output path (default: ~/.ssh/config.ansible)",
                        default="~/.ssh/config.ansible")
    parser.add_argument("-d", "--dry-run",
                        help="show new configurations without updating file",
                        action="store_true")
    parser.add_argument("-b", "--with-backup",
                        help="update with backup",
                        action="store_true",
                        default=False)
    parser.add_argument("-O", "--override",
                        help="override whole config, would remove undefiend hosts in playbook",
                        action="store_true", default=False)

    return parser.parse_args()


def update_ssh_config(ssh_config_file, inventories, variables, group='all'):
    for host in inventories.get_hosts(group):
        # Get ssh connection info from playbook inventory
        host_vars = variables.get_vars(host=host)
        hostname = host_vars.get("ansible_ssh_host", host_vars.get("ansible_host", '127.0.0.1'))
        port = host_vars.get("ansible_ssh_port", host_vars.get("ansible_port", 22))
        user = host_vars.get("ansible_ssh_user", host_vars.get("ansible_user", None))
        identityfile = host_vars.get("ansible_ssh_private_key_file")

        # Update to ssh config
        ssh_vars = ssh_config_file.host(host.get_name())
        ssh_vars.update({'Hostname': hostname})
        if port != 22:
            ssh_vars.update({'Port': port})
        if user:
            ssh_vars.update({'User': user})
        if identityfile:
            ssh_vars.update({'IdentityFile': identityfile})

        try:
            ssh_config_file.set(host.get_name(), **ssh_vars)
        except ValueError:
            ssh_config_file.add(host.get_name(), **ssh_vars)


def backup(target_file):
    copyfile(target_file, f'{target_file}.{datetime.now().strftime("%Y%m%d_%H%M%S")}')


def ansible_inventory_to_ssh_config(
        inventory_file, output, dry_run=False, with_backup=False, override=False):
    print(f'Inventory: {inventory_file}')
    print(f'Target: {output}')

    loader = DataLoader()
    inventories = InventoryManager(loader=loader, sources=[inventory_file])
    variables = VariableManager(loader=loader, inventory=inventories)

    try:
        ssh_config_file = read_ssh_config_file(output)
    except FileNotFoundError:
        ssh_config_file = empty_ssh_config_file()

    if override:
        ssh_config_file = empty_ssh_config_file()

    update_ssh_config(ssh_config_file, inventories, variables)

    if dry_run:
        print(ssh_config_file.config())
        return

    if with_backup:
        backup(output)
    ssh_config_file.write(output)


def main():
    args = get_args()
    ansible_inventory_to_ssh_config(
        args.inventory_file, expanduser(args.output), args.dry_run, args.with_backup, args.override)
