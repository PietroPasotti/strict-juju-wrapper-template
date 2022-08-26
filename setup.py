# Copyright 2021 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# TODO: Template: fill this in.
setup(
    name="jujuwrapper",
    version="0.1",
    packages=find_packages(),
    long_description=read('README.md'),
    requires=["juju==3.0.1",
              "typer==0.4.1"],
    entry_points={
        'console_scripts': [
            'jujuwrapper = jujuwrapper.main:main'
        ]
    }
)
