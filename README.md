[![PyPI version](https://img.shields.io/pypi/v/ansible-core.svg)](https://pypi.org/project/ansible-core)
[![Pylint check](https://github.com/yioda/ansible-inventory-to-ssh-config/actions/workflows/pylint.yml/badge.svg)](https://github.com/yioda/ansible-inventory-to-ssh-config/actions/workflows/pylint.yml)
[![PyPI pulish](https://github.com/yioda/ansible-inventory-to-ssh-config/actions/workflows/publish-to-pypi.yml/badge.svg)](https://github.com/yioda/ansible-inventory-to-ssh-config/actions/workflows/publish-to-pypi.yml)

# Ansible inventory file to ssh config
This is a Python tool for updating the SSH config from the Ansible inventory file.

## Dependencies

- [ansible>=2.10.7](https://pypi.org/project/ansible/2.10.5/)
- [sshconf==0.2.5](https://pypi.org/project/sshconf/0.2.5/)

## Install

> [!WARNING]
> This project would install Ansible with the specified version metioned above, be careful that might conflict with the version you are using currently.
> You might need a separated env for this tool, for example:
> ``` console
> $ mkdir foo;cd foo
> foo$ pyenv virtualenv 3.11.4 bar;pyenv local bar
> (bar)foo$
> ```

``` bash
$ pip install ansible-inventory-to-ssh-config
```

From Github:

``` bash
$ pip install git+https://github.com/yioda/ansible-inventory-to-ssh-config
```

Local install

``` bash
$ git clone https://github.com/yioda/ansible-inventory-to-ssh-config.git
$ pip install .
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
node3 ansible_host=192.168.0.7 ansible_ssh_private_key_file=~/.ssh/id_rsa_for_ansible
node4 ansible_host=192.168.0.8 ansible_port=10422 ansible_user=foo

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
  IdentityFile ~/.ssh/id_rsa_for_ansible


Host node4
  HostName 192.168.0.8
  Port 10422
  User foo
```
