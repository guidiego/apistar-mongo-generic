import importlib
from .base import MongoEnginericsAdapter


class HugWSGIAdapter(MongoEnginericsAdapter):
    def __init__(self, *args, **kwargs):
        self.hug = importlib.import_module('hug')
        self._api = self.hug.api.API(__name__)

        super(HugWSGIAdapter, self).__init__(*args, **kwargs)

    def attach(self, ctrl):
        prefix = '/{}'.format(ctrl.name)

        @self.hug.get('%s/' % prefix)
        def find(**kwargs):
            return ctrl.find(kwargs)

        @self.hug.put('%s/{item_id}' % prefix)
        def update(body, item_id):
            return ctrl.update(item_id, body)

        @self.hug.post('%s/' % prefix)
        def create(body):
            return ctrl.create(body)

        @self.hug.get('%s/{item_id}' % prefix)
        def find_one(item_id):
            return ctrl.find_one(item_id)

        @self.hug.delete('%s/{item_id}' % prefix)
        def delete(item_id):
            return ctrl.delete(item_id)

    def get_app(self):
        for controller in self._controllers:
            self.attach(controller())

        return self._api.http
