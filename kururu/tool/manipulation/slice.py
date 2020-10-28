#  Copyright (c) 2020. Davi Pereira dos Santos
#      This file is part of the kururu project.
#      Please respect the license. Removing authorship by any means
#      (by code make up or closing the sources) or ignoring property rights
#      is a crime and is unethical regarding the effort and time spent here.
#      Relevant employers or funding agencies will be notified accordingly.
#
#      kururu is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      kururu is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
from akangatu.distep import DIStep


class Slice(DIStep):
    """Select rows(or columns) inside a given interval, including limits."""

    def __init__(self, first=0, last=5, fields="X,Y"):
        # REMINDER: super call with locals lead to infinite loop
        super().__init__(first=first, last=last, fields=fields)
        self.first, self.last = first, last
        self.fields = fields.split(",")

    def _process_(self, data):
        first = self.first
        last = self.last
        if first < 0:
            if last >= 0:
                print("First cannot be negative while last is non negative:", first, last)
            first -= 1
            last -= 1

        if first == last:
            newfields = {k: data.field(k, context=self)[first].reshape(1, -1) for k in self.fields}
        else:
            newfields = {k: data.field(k, context=self)[first:last + 1] for k in self.fields}
        return data.update(self, **newfields)
