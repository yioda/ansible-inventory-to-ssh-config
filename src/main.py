from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from sshconf import read_ssh_config, empty_ssh_config_file
from os.path import expanduser
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from pkg_resources import get_distribution
from shutil import copyfile


def get_args():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    # parser.add_argument('-v', '--version', action='version',
    #                     version=get_distribution('ansible-inventory-to-ssh-config').version)
    parser.add_argument("inventory_file", help="ansible inventory file")
    parser.add_argument("-o", "--output", help="ssh config output path (default: ~/.ssh/newconfig)", default="~/.ssh/newconfig")
    parser.add_argument("-d", "--dry-run", help="show new configurations without updating file", action="store_true")
    parser.add_argument("--without-backup", help="show new configurations without updating file", action="store_true")

    return parser.parse_args()

def ansible_inventory_to_ssh_config(inventory_file, output, dry_run=False):
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[inventory_file])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    print("Inventory: {}".format(inventory_file))
    print("Target: {}".format(output))


    try:
        ssh_config = read_ssh_config(output)
        # copyfile(output, "")
    except FileNotFoundError:
        print("No such file, generate new file: {} ...".format(output))
        ssh_config = empty_ssh_config_file()

    for host in inventory.get_hosts('web'):
        host_var = variable_manager.get_vars(host=host)

        try:
            address = host_var['ansible_ssh_host']
        except:
            try:
                address = host_var['ansible_host']
            except:
                print('Failed to get [{}] ssh address... '.format(host))
                continue

        if ssh_config.host(host.get_name()):
            ssh_config.set(host.get_name(), HostName=address)
        else:
            ssh_config.add(host.get_name(), HostName=address)

    if dry_run:
        for h in ssh_config.hosts():
            print(h, ssh_config.host(h))
    else:
        try:
            ssh_config.save()
        except AttributeError:
            ssh_config.write(output)


def main():
    args = get_args()
    ansible_inventory_to_ssh_config(args.inventory_file, expanduser(args.output), args.dry_run)


if __name__ == '__main__':
    main()
