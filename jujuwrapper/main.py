#!/bin/python3
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

import juju.model
import juju.application
import juju.unit
from asyncio import run as aiorun
import typer
from subprocess import Popen, PIPE


def juju_status():
    """Demo: direct juju cli call: equivalent to `juju status`"""
    proc = Popen('juju status'.split(), stdout=PIPE)
    print(proc.stdout.read().decode('utf-8'))


def juju_get_units_containing(
        name: str = typer.Option('', help='string to use for filtering')
):
    """Demo: python-libjuju wrapper function"""

    aiorun(_juju_get_units_containing(name=name))


async def _juju_get_units_containing(name: str):
    # if we're snapped, HOME is not going to be where we think it is.
    # hacky solution: pass JUJU_DATA as envvar. One would probably have to
    # pass a jujudata.FileJujuData instance.
    user = os.environ['USER']
    jdata = f"/home/{user}/.local/share/juju"
    os.environ['JUJU_DATA'] = jdata
    print(f'using JUJU_DATA: {jdata}')

    model = juju.model.Model()
    await model.connect()
    units = []

    app: juju.application.Application
    for app_name, app in model.applications.items():
        unit: juju.unit.Unit
        for unit in app.units:
            if name in unit.name:
                units.append(unit.name)

    if not units:
        print(f'no units found containing {name}')
    else:
        print(units)


def main():
    app = typer.Typer(name="jujuwrapper",
                      help="Demo python wrapper for juju client.")
    app.command(name="status")(juju_status)
    app.command(name="filter")(juju_get_units_containing)

    app()


if __name__ == '__main__':
    main()
