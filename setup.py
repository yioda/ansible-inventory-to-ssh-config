from setuptools import setup, find_packages
from subprocess import check_output

try:
    current_version = check_output(
        ['git', 'describe', '--tags']).rstrip().decode()
    print(current_version)
except Exception as e:
    current_version = 'g' + check_output(
        ['git', 'log', '-1', '--format=%h']).rstrip().decode()

setup(
    name="ansible-inventory-to-ssh-config",
    version=current_version,
    description="Generate ssh config file from Ansible inventory",
    author="Yioda",
    author_email='jyc180g@gmail.com',
    url="https://github.com/yioda/ansible-inventory-to-ssh-config",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ansible-inventory-to-ssh-config=src.main:main',
            'aitsc=src.main:main'
        ],
    },
    install_requires=[
        'ansible>=2.10.7',
        'sshconf==0.2.2'
    ],
    python_requires=">=3"
)
