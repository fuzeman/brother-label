class ElementManager:
    def __init__(self, items):
        self._items = {}

        for item in items:
            self.register(item)
        
    def register(self, item):
        if item.identifier in self._items:
            raise KeyError('Element Already Registered')
        
        self._items[item.identifier] = item

    def deregister(self, item):
        if item not in self._items:
            return
        
        self._items.pop(item.identifier)

    def items(self):
        return self._items.items()
    
    def keys(self):
        return self._items.keys()

    def values(self):
        return self._items.values()
    
    def __getitem__(self, key):
        return self._items[key]
    
    def __contains__(self, key):
        return self._items.__contains__(key)

    def __iter__(self):
        return self._items.__iter__()
