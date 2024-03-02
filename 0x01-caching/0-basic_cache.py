#!/usr/bin/env python3
""" This module contains a class BasicCache
    that inherits from BaseCaching
"""


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache class that inherits from BaseCaching
    """

    def put(self, key, item):
        """Assign to the dictionary self.cache_data
            the item value for the key `key`.
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """
        Return the value in self.cache_data linked to key.
        """
        return self.cache_data.get(key, None)
