from setuptools import setup

setup(name='crhomeautomation',
      version='0.1',
      description='A Raspberry Pi home automation project to control Nexa remote switch.',
      url='https://github.com/crundberg/home-automation',
      author='Christoffer Rundberg',
      author_email='christoffer@crwebb.se',
      license='MIT',
      packages=['crhomeautomation'],
      install_requires=[
          'mysql-server',
          'python-mysqldb',
          'python-dev',
          'libboost-python-dev',
          'python-pip',
          'apache2',
          'php5',
          'libapache2-mod-php5',
          'php5-curl',
          'flask',
      ],
      zip_safe=False)
