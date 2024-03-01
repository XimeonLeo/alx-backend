#!/usr/bin/env python3
""" Hypermedia pagination
"""
import csv
import math
from typing import Tuple, List, Dict, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    index_range

    Args:
        page (int): page index
        page_size (int): _description_

    Returns:
        Tuple: containing start-index and end-index
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a db of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """ A method of cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        get_page

        Args:
            page (int, optional): page. Defaults to 1.
            page_size (int, optional): page_size. Defaults to 10.

        Returns:
            List[List]: list of items
        """
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0
        csv_size = len(self.dataset())
        start, end = index_range(page, page_size)
        end = min(end, csv_size)
        if start >= csv_size:
            return []
        return self.dataset()[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """returns all necessary key value pairs for pagination

        Args:
            page (int, optional): page index. Defaults to 1.
            page_size (int, optional): number of items in page. Defaults to 10.

        Returns:
            dict: dictionary of all necessary
            key value pairs of pagination attributes
        """
        total_pages = math.ceil(len(self.dataset()) / page_size)
        return {
            "page_size": page_size,
            "page": page,
            "data": self.get_page(page, page_size),
            "next_page": page + 1 if page + 1 <= total_pages else None,
            "prev_page": page - 1 if page > 1 else None,
            "total_pages": total_pages
        }
