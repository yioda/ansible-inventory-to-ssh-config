# Ansible inventory file to ssh config
This is a python tool for updating ssh config from ansible inventory file.


## Install

``` bash
$ pip3 install --user ansible-inventory-to-ssh-config
```

From github:

``` bash
$ pip3 install --user git+https://github.com/yioda/ansible-inventory-to-ssh-config
```

Local install

``` bash
$ git clone https://github.com/yioda/ansible-inventory-to-ssh-config.git
$ pip3 install .
```

## Usage

``` bash
$ aitsc -h # or ansible-inventory-to-ssh-config -h
usage: aitsc [-h] [-v] [-o OUTPUT] [-d] [-b] [-O] inventory_file

positional arguments:
  inventory_file        ansible inventory file

options:
  -h, --help            show this help message and exit
  -v, --version         show program version number and exit
  -o OUTPUT, --output OUTPUT
                        ssh config output path (default: ~/.ssh/config.ansible)
  -d, --dry-run         show new configurations without updating file
  -b, --with-backup     update with backup
  -O, --override        override whole config, this would remove those hosts undefined in playbook


# Update ~/.ssh/config.ansible from specified inventory file
$ aitsc $INVENTORY_FILE

# Update with backup
$ aitsc $INVENTORY_FILE --with-backup

# Output as a new file
$ aitsc $INVENTORY_FILE -o new_ssh_config

# Show content without output
$ aitsc $INVENTORY_FILE -d

# Override while config
$ aitsc $INVENTORY_FILE -O
```

## Example

``` bash
# Input (Inventory File)
$ cat hosts

[group_1]
node1 ansible_ssh_host=192.168.0.5
node2 ansible_ssh_host=192.168.0.6

[group_2]
node3 ansible_host=192.168.0.7
node4 ansible_host=192.168.0.8

# Commnad
$ aitsc hosts -o newconfig
Inventory: hosts
Target: newconfig

# Output (SSH Config Format)
$ cat new_ssh_config

Host node1
  HostName 192.168.0.5


Host node2
  HostName 192.168.0.6


Host node3
  HostName 192.168.0.7


Host node4
  HostName 192.168.0.8
```
