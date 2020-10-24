import traceback

from aiuna.content.data import Data
from akangatu.container import Container1
from akangatu.distep import DIStep
from tatu.amnesia import Amnesia
from tatu.storage import Storage
from tatu.pickle_ import Pickle
from tatu.sql.sqlite import SQLite


class LCache(DIStep):
    storages = {}

    def __init__(self, storage="sqlite", seed=0):  # TODO: what todo with seed here?
        super().__init__(seed=seed, storage=storage)
        if storage == "pickle":
            storage = Pickle()
        elif storage == "sqlite":
            storage = SQLite()
        elif storage == "amnesia":
            storage = Amnesia()
        elif not isinstance(storage, Storage):
            print("Unknown storage:", self.storage)
            exit()
        if storage.id not in self.storages:
            self.storages[storage.id] = storage
        self.storage = self.storages[storage.id]

    def _process_(self, data: Data):
        # TODO ver no papel como fazer mini Caches p/ stream (se é versdade)
        print("bef fetch")
        fetched = self.storage.lazyfetch(data, lock=True)
        print("aft fetch")
        if fetched:
            return fetched
        print("bef store")
        ret = self.storage.lazystore(data)
        print("aft store")
        return ret

    # TODO dar unlock() no data.getitem se exception

    def _uuid_(self):
        return self.step.uuid
