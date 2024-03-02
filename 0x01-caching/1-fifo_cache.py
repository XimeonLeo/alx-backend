#!/usr/bin/env python3
""" This module contains the FIFO caching system
"""

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    """
        A class FIFOCache caching system that iniherits from BaseCaching
    """

    def __init__(self):
        """
            Initialize the super class
        """
        super().__init__()
        self.key_indexes = []

    def put(self, key, item):
        """
            assign to the dictionary self.cache_data
            the item value for the key key.
        """
        if key and item:
            if key in self.cache_data:
                self.cache_data[key] = item
                return

            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                item_discarded = self.key_indexes.pop(0)
                del self.cache_data[item_discarded]
                print("DISCARD:", item_discarded)

            self.cache_data[key] = item
            self.key_indexes.append(key)

    def get(self, key):
        """
            return the value in self.cache_data linked to key.
        """
        if key in self.cache_data:
            return self.cache_data[key]
        return None
