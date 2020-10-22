import numpy as np
from sklearn.preprocessing import OneHotEncoder

from aiuna.content.data import Data
from aiuna.creation import nominal_idxs
from akangatu.distep import DIStep
from transf.mixin.config import asConfigLess


class Binarize(asConfigLess, DIStep):  # TODO: other fields
    def _process_(self, data: Data):
        newmatrices = {}

        # REMINDER: Binarize will do nothing to numeric datasets, but the uuid still needs to be predictable.
        # So, the provided Data object should be "processed" anyway.
        def func():
            data_nominal_idxs = nominal_idxs(data.Xt)
            encoder = OneHotEncoder()
            if len(data_nominal_idxs) > 0:
                nom = encoder.fit_transform(data.X[:, data_nominal_idxs]).toarray()
                num = np.delete(data.X, data_nominal_idxs, axis=1).astype(float)
                return np.column_stack((nom, num))

        newmatrices["X"] = func

        return data.update(self, **newmatrices)
