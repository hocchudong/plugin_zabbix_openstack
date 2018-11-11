#!/usr/bin/python3.5

from setuptools import setup

requirements = [
    "aiohttp",
    "requests",
    "py-zabbix",
    "configparser",
]

setup(
    name='openstack_monitoring',
    version='1.0',
    description="OpenStack Monitoring with Zabbix",
    long_description="test",
    author="Minh Nguyen",
    author_email='nguyenvanminhkma@gmail.com',
    url='https://minhkma.github.io',
    packages=[
        'openstack_monitoring',
    ],
    package_dir={'openstack_monitoring':
                 'openstack_monitoring'},
    entry_points={
        'console_scripts': [
            'openstack_monitoring=openstack_monitoring.main:main'
        ]
    },
    data_files=[
        ('/etc/openstack_monitoring/', ['etc/config.cfg']),
    ],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='openstack_monitoring',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)