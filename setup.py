from setuptools import setup, find_packages

setup(
    name="ansible-inventory-to-ssh-config",
    version="0.0.1",
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
        'ansible',
        'sshconf'
    ],
    python_requires=">=3"
)