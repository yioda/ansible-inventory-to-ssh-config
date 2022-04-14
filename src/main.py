from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from sshconf import read_ssh_config, empty_ssh_config_file
from os.path import expanduser
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from pkg_resources import get_distribution
from shutil import copyfile
from datetime import datetime


def get_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                        version=get_distribution('ansible-inventory-to-ssh-config').version)
    parser.add_argument("inventory_file", help="ansible inventory file")
    parser.add_argument("-o", "--output", help="ssh config output path (default: ~/.ssh/config)", default="~/.ssh/config")
    parser.add_argument("-d", "--dry-run", help="show new configurations without updating file", action="store_true")
    parser.add_argument("--without-backup", help="update without backup", action="store_true", default=False)

    return parser.parse_args()

def update_ssh_config(ssh_config, inventories, variables, group='all'):
    def _get_key(vars, keynames):
        value = vars.get(keynames[0], vars.get(keynames[1], None))
        if not value:
            raise KeyError(f"Provided dictionary does not contain values for given keys: {keynames}")
        return value

    for host in inventories.get_hosts(group):
        host_var = variables.get_vars(host=host)
        host_name = host.get_name()
        ssh_config_options = {}

        try:
            ssh_config_options["HostName"] = _get_key(host_var, ("ansible_host","ansible_ssh_host"))
        except KeyError:
            print('Failed to get [{}] ssh address... '.format(host))
            continue

        try:
            ssh_config_options["Port"] = _get_key(host_var, ("ansible_port","ansible_ssh_port"))
        except KeyError:
            # Field is not mandatory, no need to do error handling
            pass

        try:
            ssh_config_options["User"] = _get_key(host_var, ("ansible_user","ansible_ssh_user"))
        except KeyError:
            # Field is not mandatory, no need to do error handling
            pass


        try:
            ssh_config.set(host_name, **ssh_config_options)
        except ValueError:
            ssh_config.add(host_name, **ssh_config_options)




def backup(target_file):
    copyfile(target_file, "{}.{}".format(target_file, datetime.now().strftime("%Y%m%d_%H%M%S")))


def print_ssh_config(ssh_config):
    for h in ssh_config.hosts():
        print(h, ssh_config.host(h))


def ansible_inventory_to_ssh_config(inventory_file, output, dry_run=False, with_backup=True):
    print("Inventory: {}".format(inventory_file))
    print("Target: {}".format(output))

    loader = DataLoader()
    inventories = InventoryManager(loader=loader, sources=[inventory_file])
    variables = VariableManager(loader=loader, inventory=inventories)

    try:
        ssh_config = read_ssh_config(output)
        update_ssh_config(ssh_config, inventories, variables)

        if with_backup:
            backup(output)

        if dry_run:
            print_ssh_config(ssh_config)
        else:
            ssh_config.save()
    except FileNotFoundError:
        ssh_config = empty_ssh_config_file()
        update_ssh_config(ssh_config, inventories, variables)

        if dry_run:
            print_ssh_config(ssh_config)
        else:
            print("No such file, generate a new file: {} ...".format(output))
            ssh_config.write(output)


def main():
    args = get_args()
    ansible_inventory_to_ssh_config(args.inventory_file, expanduser(args.output), args.dry_run, not args.without_backup)

