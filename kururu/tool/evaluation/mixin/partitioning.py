#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the kururu project.
#  Please respect the license - more about this in the section (*) below.
#
#  kururu is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kururu is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with kururu.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.

from sklearn.model_selection import StratifiedKFold, LeaveOneOut, StratifiedShuffleSplit

from akangatu.transf.config import globalcache


class withPartitioning:
    def __init__(self, mode, config):
        if mode == "cv":
            del config["test_size"]
            self.algorithm = StratifiedKFold(shuffle=True, n_splits=config["splits"], random_state=config["seed"])
        elif mode == "loo":
            del config["tests"]
            del config["test_size"]
            del config["seed"]
            self.algorithm = LeaveOneOut()
        elif mode == "holdout":
            self.algorithm = StratifiedShuffleSplit(n_splits=config["splits"], test_size=config["test_size"], random_state=config["seed"])
        else:
            raise Exception("Wrong mode: ", mode)
        self._config = config
        self.splits = config["splits"]
        self.fields = config["fields"].split(",")

    # @globalcache
    def partitionings(self, data):
        X, y = data.Xy  # TODO: add other scenarios beyond classification?
        return list(self.algorithm.split(X=X, y=y))

    def _config_(self):
        return self._config
