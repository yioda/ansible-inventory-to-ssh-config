# ansible-inventory-to-ssh-config
This is a python tool for updating ssh config from ansible inventory file.

## Requirments

``` bash
$ pip3 install --user ansible sshconf
```

## Install

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
$ aitsc -h
usage: aitsc [-h] [-o OUTPUT] [-d] [--with-backup] inventory_file

positional arguments:
  inventory_file        ansible inventory file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        ssh config output path (default: ~/.ssh/config)
  -d, --dry-run         show new configurations without updating file
  --without-backup      update without backup

# Update ~/.ssh/config from specified inventory file
$ aitsc $INVENTORY_FILE

# Update without backup
$ aitsc $INVENTORY_FILE --without-backup

# Output as a new file
$ aitsc $INVENTORY_FILE -o new_ssh_config

# Show content without output
$ aitsc $INVENTORY_FILE -d
```