#!/usr/bin/env python3
"""
This module contains the MRU Caching
"""


from collections import OrderedDict


BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    """
        A class MRUCache that inherits
    from BaseCaching and implements the caching system
    """
    def __init__(self):
        super().__init__()
        self.mru_order = OrderedDict()

    def put(self, key, item):
        """
            Assign to the dictionary
            self.cache_data the item value for the key key
        """
        if not key or not item:
            return

        self.cache_data[key] = item
        self.mru_order[key] = item

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            item_discarded = next(iter(self.mru_order))
            del self.cache_data[item_discarded]
            print("DISCARD:", item_discarded)

        if len(self.mru_order) > BaseCaching.MAX_ITEMS:
            self.mru_order.popitem(last=False)

        self.mru_order.move_to_end(key, False)

    def get(self, key):
        """
            Rreturn the value in
            self.cache_data linked to key.
        """
        if key in self.cache_data:
            self.mru_order.move_to_end(key, False)
            return self.cache_data[key]
        return None
