from __future__ import annotations
from typing import Hashable
import heapq
import time


OUTPUT_TYPE = int

banned: list[int] = [2, 4, 6, 8]
costs: dict[str, int] = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

homes_1: dict[str, list[int]] = {
    "A": [11, 15],
    "B": [12, 16],
    "C": [13, 17],
    "D": [14, 18]
}
homes_2: dict[str, list[int]] = {
    "A": [11, 15, 19, 23],
    "B": [12, 16, 20, 24],
    "C": [13, 17, 21, 25],
    "D": [14, 18, 22, 26]
}
homes: dict[str, list[int]] = {}

directions_1: list[list[list[int]]] = [
    [[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 11], [0, 1, 2, 3, 4, 12], [0, 1, 2, 3, 4, 5, 6, 13], [0, 1, 2, 3, 4, 5, 6, 7, 8, 14]], [[1], [], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 11], [1, 2, 3, 4, 12], [1, 2, 3, 4, 5, 6, 13], [1, 2, 3, 4, 5, 6, 7, 8, 14]], [[2, 1], [2], [], [2], [2, 3], [2, 3, 4], [2, 3, 4, 5], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8, 9], [2], [2, 3, 4], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7, 8], [2, 11], [2, 3, 4, 12], [2, 3, 4, 5, 6, 13], [2, 3, 4, 5, 6, 7, 8, 14]], [[3, 2, 1], [3, 2], [3], [], [3], [3, 4], [3, 4, 5], [3, 4, 5, 6], [3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8, 9], [3, 2], [3, 4], [3, 4, 5, 6], [3, 4, 5, 6, 7, 8], [3, 2, 11], [3, 4, 12], [3, 4, 5, 6, 13], [3, 4, 5, 6, 7, 8, 14]], [[4, 3, 2, 1], [4, 3, 2], [4, 3], [4], [], [4], [4, 5], [4, 5, 6], [4, 5, 6, 7], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9], [4, 3, 2], [4], [4, 5, 6], [4, 5, 6, 7, 8], [4, 3, 2, 11], [4, 12], [4, 5, 6, 13], [4, 5, 6, 7, 8, 14]], [[5, 4, 3, 2, 1], [5, 4, 3, 2], [5, 4, 3], [5, 4], [5], [], [5], [5, 6], [5, 6, 7], [5, 6, 7, 8], [5, 6, 7, 8, 9], [5, 4, 3, 2], [5, 4], [5, 6], [5, 6, 7, 8], [5, 4, 3, 2, 11], [5, 4, 12], [5, 6, 13], [5, 6, 7, 8, 14]], [[6, 5, 4, 3, 2, 1], [6, 5, 4, 3, 2], [6, 5, 4, 3], [6, 5, 4], [6, 5], [6], [], [6], [6, 7], [6, 7, 8], [6, 7, 8, 9], [6, 5, 4, 3, 2], [6, 5, 4], [6], [6, 7, 8], [6, 5, 4, 3, 2, 11], [6, 5, 4, 12], [6, 13], [6, 7, 8, 14]], [[7, 6, 5, 4, 3, 2, 1], [7, 6, 5, 4, 3, 2], [7, 6, 5, 4, 3], [7, 6, 5, 4], [7, 6, 5], [7, 6], [7], [], [7], [7, 8], [7, 8, 9], [7, 6, 5, 4, 3, 2], [7, 6, 5, 4], [7, 6], [7, 8], [7, 6, 5, 4, 3, 2, 11], [7, 6, 5, 4, 12], [7, 6, 13], [7, 8, 14]], [[8, 7, 6, 5, 4, 3, 2, 1], [8, 7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4, 3], [8, 7, 6, 5, 4], [8, 7, 6, 5], [8, 7, 6], [8, 7], [8], [], [8], [8, 9], [8, 7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4], [8, 7, 6], [8], [8, 7, 6, 5, 4, 3, 2, 11], [8, 7, 6, 5, 4, 12], [8, 7, 6, 13], [8, 14]], [[9, 8, 7, 6, 5, 4, 3, 2, 1], [9, 8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4, 3], [9, 8, 7, 6, 5, 4], [9, 8, 7, 6, 5], [9, 8, 7, 6], [9, 8, 7], [9, 8], [9], [], [9], [9, 8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4], [9, 8, 7, 6], [9, 8], [9, 8, 7, 6, 5, 4, 3, 2, 11], [9, 8, 7, 6, 5, 4, 12], [9, 8, 7, 6, 13], [9, 8, 14]], [[10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [10, 9, 8, 7, 6, 5, 4, 3, 2], [10, 9, 8, 7, 6, 5, 4, 3], [10, 9, 8, 7, 6, 5, 4], [10, 9, 8, 7, 6, 5], [10, 9, 8, 7, 6], [10, 9, 8, 7], [10, 9, 8], [10, 9], [10], [], [10, 9, 8, 7, 6, 5, 4, 3, 2], [10, 9, 8, 7, 6, 5, 4], [10, 9, 8, 7, 6], [10, 9, 8], [10, 9, 8, 7, 6, 5, 4, 3, 2, 11], [10, 9, 8, 7, 6, 5, 4, 12], [10, 9, 8, 7, 6, 13], [10, 9, 8, 14]], [[11, 2, 1], [11, 2], [11], [11, 2], [11, 2, 3], [11, 2, 3, 4], [11, 2, 3, 4, 5], [11, 2, 3, 4, 5, 6], [11, 2, 3, 4, 5, 6, 7], [11, 2, 3, 4, 5, 6, 7, 8], [11, 2, 3, 4, 5, 6, 7, 8, 9], [], [11, 2, 3, 4], [11, 2, 3, 4, 5, 6], [11, 2, 3, 4, 5, 6, 7, 8], [11], [11, 2, 3, 4, 12], [11, 2, 3, 4, 5, 6, 13], [11, 2, 3, 4, 5, 6, 7, 8, 14]], [[12, 4, 3, 2, 1], [12, 4, 3, 2], [12, 4, 3], [12, 4], [12], [12, 4], [12, 4, 5], [12, 4, 5, 6], [12, 4, 5, 6, 7], [12, 4, 5, 6, 7, 8], [12, 4, 5, 6, 7, 8, 9], [12, 4, 3, 2], [], [12, 4, 5, 6], [12, 4, 5, 6, 7, 8], [12, 4, 3, 2, 11], [12], [12, 4, 5, 6, 13], [12, 4, 5, 6, 7, 8, 14]], [[13, 6, 5, 4, 3, 2, 1], [13, 6, 5, 4, 3, 2], [13, 6, 5, 4, 3], [13, 6, 5, 4], [13, 6, 5], [13, 6], [13], [13, 6], [13, 6, 7], [13, 6, 7, 8], [13, 6, 7, 8, 9], [13, 6, 5, 4, 3, 2], [13, 6, 5, 4], [], [13, 6, 7, 8], [13, 6, 5, 4, 3, 2, 11], [13, 6, 5, 4, 12], [13], [13, 6, 7, 8, 14]], [[14, 8, 7, 6, 5, 4, 3, 2, 1], [14, 8, 7, 6, 5, 4, 3, 2], [14, 8, 7, 6, 5, 4, 3], [14, 8, 7, 6, 5, 4], [14, 8, 7, 6, 5], [14, 8, 7, 6], [14, 8, 7], [14, 8], [14], [14, 8], [14, 8, 9], [14, 8, 7, 6, 5, 4, 3, 2], [14, 8, 7, 6, 5, 4], [14, 8, 7, 6], [], [14, 8, 7, 6, 5, 4, 3, 2, 11], [14, 8, 7, 6, 5, 4, 12], [14, 8, 7, 6, 13], [14]], [[15, 11, 2, 1], [15, 11, 2], [15, 11], [15, 11, 2], [15, 11, 2, 3], [15, 11, 2, 3, 4], [15, 11, 2, 3, 4, 5], [15, 11, 2, 3, 4, 5, 6], [15, 11, 2, 3, 4, 5, 6, 7], [15, 11, 2, 3, 4, 5, 6, 7, 8], [15, 11, 2, 3, 4, 5, 6, 7, 8, 9], [15], [15, 11, 2, 3, 4], [15, 11, 2, 3, 4, 5, 6], [15, 11, 2, 3, 4, 5, 6, 7, 8], [], [15, 11, 2, 3, 4, 12], [15, 11, 2, 3, 4, 5, 6, 13], [15, 11, 2, 3, 4, 5, 6, 7, 8, 14]], [[16, 12, 4, 3, 2, 1], [16, 12, 4, 3, 2], [16, 12, 4, 3], [16, 12, 4], [16, 12], [16, 12, 4], [16, 12, 4, 5], [16, 12, 4, 5, 6], [16, 12, 4, 5, 6, 7], [16, 12, 4, 5, 6, 7, 8], [16, 12, 4, 5, 6, 7, 8, 9], [16, 12, 4, 3, 2], [16], [16, 12, 4, 5, 6], [16, 12, 4, 5, 6, 7, 8], [16, 12, 4, 3, 2, 11], [], [16, 12, 4, 5, 6, 13], [16, 12, 4, 5, 6, 7, 8, 14]], [[17, 13, 6, 5, 4, 3, 2, 1], [17, 13, 6, 5, 4, 3, 2], [17, 13, 6, 5, 4, 3], [17, 13, 6, 5, 4], [17, 13, 6, 5], [17, 13, 6], [17, 13], [17, 13, 6], [17, 13, 6, 7], [17, 13, 6, 7, 8], [17, 13, 6, 7, 8, 9], [17, 13, 6, 5, 4, 3, 2], [17, 13, 6, 5, 4], [17], [17, 13, 6, 7, 8], [17, 13, 6, 5, 4, 3, 2, 11], [17, 13, 6, 5, 4, 12], [], [17, 13, 6, 7, 8, 14]], [[18, 14, 8, 7, 6, 5, 4, 3, 2, 1], [18, 14, 8, 7, 6, 5, 4, 3, 2], [18, 14, 8, 7, 6, 5, 4, 3], [18, 14, 8, 7, 6, 5, 4], [18, 14, 8, 7, 6, 5], [18, 14, 8, 7, 6], [18, 14, 8, 7], [18, 14, 8], [18, 14], [18, 14, 8], [18, 14, 8, 9], [18, 14, 8, 7, 6, 5, 4, 3, 2], [18, 14, 8, 7, 6, 5, 4], [18, 14, 8, 7, 6], [18], [18, 14, 8, 7, 6, 5, 4, 3, 2, 11], [18, 14, 8, 7, 6, 5, 4, 12], [18, 14, 8, 7, 6, 13], []]]
directions_2: list[list[list[int]]] = [[[], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 7], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 11], [0, 1, 2, 3, 4, 12], [0, 1, 2, 3, 4, 5, 6, 13], [0, 1, 2, 3, 4, 5, 6, 7, 8, 14], [0, 1, 2, 11, 15], [0, 1, 2, 3, 4, 12, 16], [0, 1, 2, 3, 4, 5, 6, 13, 17], [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 18], [0, 1, 2, 11, 15, 19], [0, 1, 2, 3, 4, 12, 16, 20], [0, 1, 2, 3, 4, 5, 6, 13, 17, 21], [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[1], [], [1], [1, 2], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5, 6, 7, 8], [1, 2, 11], [1, 2, 3, 4, 12], [1, 2, 3, 4, 5, 6, 13], [1, 2, 3, 4, 5, 6, 7, 8, 14], [1, 2, 11, 15], [1, 2, 3, 4, 12, 16], [1, 2, 3, 4, 5, 6, 13, 17], [1, 2, 3, 4, 5, 6, 7, 8, 14, 18], [1, 2, 11, 15, 19], [1, 2, 3, 4, 12, 16, 20], [1, 2, 3, 4, 5, 6, 13, 17, 21], [1, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[2, 1], [2], [], [2], [2, 3], [2, 3, 4], [2, 3, 4, 5], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7, 8], [2, 3, 4, 5, 6, 7, 8, 9], [2], [2, 3, 4], [2, 3, 4, 5, 6], [2, 3, 4, 5, 6, 7, 8], [2, 11], [2, 3, 4, 12], [2, 3, 4, 5, 6, 13], [2, 3, 4, 5, 6, 7, 8, 14], [2, 11, 15], [2, 3, 4, 12, 16], [2, 3, 4, 5, 6, 13, 17], [2, 3, 4, 5, 6, 7, 8, 14, 18], [2, 11, 15, 19], [2, 3, 4, 12, 16, 20], [2, 3, 4, 5, 6, 13, 17, 21], [2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[3, 2, 1], [3, 2], [3], [], [3], [3, 4], [3, 4, 5], [3, 4, 5, 6], [3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [3, 4, 5, 6, 7, 8, 9], [3, 2], [3, 4], [3, 4, 5, 6], [3, 4, 5, 6, 7, 8], [3, 2, 11], [3, 4, 12], [3, 4, 5, 6, 13], [3, 4, 5, 6, 7, 8, 14], [3, 2, 11, 15], [3, 4, 12, 16], [3, 4, 5, 6, 13, 17], [3, 4, 5, 6, 7, 8, 14, 18], [3, 2, 11, 15, 19], [3, 4, 12, 16, 20], [3, 4, 5, 6, 13, 17, 21], [3, 4, 5, 6, 7, 8, 14, 18, 22]], [[4, 3, 2, 1], [4, 3, 2], [4, 3], [4], [], [4], [4, 5], [4, 5, 6], [4, 5, 6, 7], [4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9], [4, 3, 2], [4], [4, 5, 6], [4, 5, 6, 7, 8], [4, 3, 2, 11], [4, 12], [4, 5, 6, 13], [4, 5, 6, 7, 8, 14], [4, 3, 2, 11, 15], [4, 12, 16], [4, 5, 6, 13, 17], [4, 5, 6, 7, 8, 14, 18], [4, 3, 2, 11, 15, 19], [4, 12, 16, 20], [4, 5, 6, 13, 17, 21], [4, 5, 6, 7, 8, 14, 18, 22]], [[5, 4, 3, 2, 1], [5, 4, 3, 2], [5, 4, 3], [5, 4], [5], [], [5], [5, 6], [5, 6, 7], [5, 6, 7, 8], [5, 6, 7, 8, 9], [5, 4, 3, 2], [5, 4], [5, 6], [5, 6, 7, 8], [5, 4, 3, 2, 11], [5, 4, 12], [5, 6, 13], [5, 6, 7, 8, 14], [5, 4, 3, 2, 11, 15], [5, 4, 12, 16], [5, 6, 13, 17], [5, 6, 7, 8, 14, 18], [5, 4, 3, 2, 11, 15, 19], [5, 4, 12, 16, 20], [5, 6, 13, 17, 21], [5, 6, 7, 8, 14, 18, 22]], [[6, 5, 4, 3, 2, 1], [6, 5, 4, 3, 2], [6, 5, 4, 3], [6, 5, 4], [6, 5], [6], [], [6], [6, 7], [6, 7, 8], [6, 7, 8, 9], [6, 5, 4, 3, 2], [6, 5, 4], [6], [6, 7, 8], [6, 5, 4, 3, 2, 11], [6, 5, 4, 12], [6, 13], [6, 7, 8, 14], [6, 5, 4, 3, 2, 11, 15], [6, 5, 4, 12, 16], [6, 13, 17], [6, 7, 8, 14, 18], [6, 5, 4, 3, 2, 11, 15, 19], [6, 5, 4, 12, 16, 20], [6, 13, 17, 21], [6, 7, 8, 14, 18, 22]], [[7, 6, 5, 4, 3, 2, 1], [7, 6, 5, 4, 3, 2], [7, 6, 5, 4, 3], [7, 6, 5, 4], [7, 6, 5], [7, 6], [7], [], [7], [7, 8], [7, 8, 9], [7, 6, 5, 4, 3, 2], [7, 6, 5, 4], [7, 6], [7, 8], [7, 6, 5, 4, 3, 2, 11], [7, 6, 5, 4, 12], [7, 6, 13], [7, 8, 14], [7, 6, 5, 4, 3, 2, 11, 15], [7, 6, 5, 4, 12, 16], [7, 6, 13, 17], [7, 8, 14, 18], [7, 6, 5, 4, 3, 2, 11, 15, 19], [7, 6, 5, 4, 12, 16, 20], [7, 6, 13, 17, 21], [7, 8, 14, 18, 22]], [[8, 7, 6, 5, 4, 3, 2, 1], [8, 7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4, 3], [8, 7, 6, 5, 4], [8, 7, 6, 5], [8, 7, 6], [8, 7], [8], [], [8], [8, 9], [8, 7, 6, 5, 4, 3, 2], [8, 7, 6, 5, 4], [8, 7, 6], [8], [8, 7, 6, 5, 4, 3, 2, 11], [8, 7, 6, 5, 4, 12], [8, 7, 6, 13], [8, 14], [8, 7, 6, 5, 4, 3, 2, 11, 15], [8, 7, 6, 5, 4, 12, 16], [8, 7, 6, 13, 17], [8, 14, 18], [8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [8, 7, 6, 5, 4, 12, 16, 20], [8, 7, 6, 13, 17, 21], [8, 14, 18, 22]], [[9, 8, 7, 6, 5, 4, 3, 2, 1], [9, 8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4, 3], [9, 8, 7, 6, 5, 4], [9, 8, 7, 6, 5], [9, 8, 7, 6], [9, 8, 7], [9, 8], [9], [], [9], [9, 8, 7, 6, 5, 4, 3, 2], [9, 8, 7, 6, 5, 4], [9, 8, 7, 6], [9, 8], [9, 8, 7, 6, 5, 4, 3, 2, 11], [9, 8, 7, 6, 5, 4, 12], [9, 8, 7, 6, 13], [9, 8, 14], [9, 8, 7, 6, 5, 4, 3, 2, 11, 15], [9, 8, 7, 6, 5, 4, 12, 16], [9, 8, 7, 6, 13, 17], [9, 8, 14, 18], [9, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [9, 8, 7, 6, 5, 4, 12, 16, 20], [9, 8, 7, 6, 13, 17, 21], [9, 8, 14, 18, 22]], [[10, 9, 8, 7, 6, 5, 4, 3, 2, 1], [10, 9, 8, 7, 6, 5, 4, 3, 2], [10, 9, 8, 7, 6, 5, 4, 3], [10, 9, 8, 7, 6, 5, 4], [10, 9, 8, 7, 6, 5], [10, 9, 8, 7, 6], [10, 9, 8, 7], [10, 9, 8], [10, 9], [10], [], [10, 9, 8, 7, 6, 5, 4, 3, 2], [10, 9, 8, 7, 6, 5, 4], [10, 9, 8, 7, 6], [10, 9, 8], [10, 9, 8, 7, 6, 5, 4, 3, 2, 11], [10, 9, 8, 7, 6, 5, 4, 12], [10, 9, 8, 7, 6, 13], [10, 9, 8, 14], [10, 9, 8, 7, 6, 5, 4, 3, 2, 11, 15], [10, 9, 8, 7, 6, 5, 4, 12, 16], [10, 9, 8, 7, 6, 13, 17], [10, 9, 8, 14, 18], [10, 9, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [10, 9, 8, 7, 6, 5, 4, 12, 16, 20], [10, 9, 8, 7, 6, 13, 17, 21], [10, 9, 8, 14, 18, 22]], [[11, 2, 1], [11, 2], [11], [11, 2], [11, 2, 3], [11, 2, 3, 4], [11, 2, 3, 4, 5], [11, 2, 3, 4, 5, 6], [11, 2, 3, 4, 5, 6, 7], [11, 2, 3, 4, 5, 6, 7, 8], [11, 2, 3, 4, 5, 6, 7, 8, 9], [], [11, 2, 3, 4], [11, 2, 3, 4, 5, 6], [11, 2, 3, 4, 5, 6, 7, 8], [11], [11, 2, 3, 4, 12], [11, 2, 3, 4, 5, 6, 13], [11, 2, 3, 4, 5, 6, 7, 8, 14], [11, 15], [11, 2, 3, 4, 12, 16], [11, 2, 3, 4, 5, 6, 13, 17], [11, 2, 3, 4, 5, 6, 7, 8, 14, 18], [11, 15, 19], [11, 2, 3, 4, 12, 16, 20], [11, 2, 3, 4, 5, 6, 13, 17, 21], [11, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[12, 4, 3, 2, 1], [12, 4, 3, 2], [12, 4, 3], [12, 4], [12], [12, 4], [12, 4, 5], [12, 4, 5, 6], [12, 4, 5, 6, 7], [12, 4, 5, 6, 7, 8], [12, 4, 5, 6, 7, 8, 9], [12, 4, 3, 2], [], [12, 4, 5, 6], [12, 4, 5, 6, 7, 8], [12, 4, 3, 2, 11], [12], [12, 4, 5, 6, 13], [12, 4, 5, 6, 7, 8, 14], [12, 4, 3, 2, 11, 15], [12, 16], [12, 4, 5, 6, 13, 17], [12, 4, 5, 6, 7, 8, 14, 18], [12, 4, 3, 2, 11, 15, 19], [12, 16, 20], [12, 4, 5, 6, 13, 17, 21], [12, 4, 5, 6, 7, 8, 14, 18, 22]], [[13, 6, 5, 4, 3, 2, 1], [13, 6, 5, 4, 3, 2], [13, 6, 5, 4, 3], [13, 6, 5, 4], [13, 6, 5], [13, 6], [13], [13, 6], [13, 6, 7], [13, 6, 7, 8], [13, 6, 7, 8, 9], [13, 6, 5, 4, 3, 2], [13, 6, 5, 4], [], [13, 6, 7, 8], [13, 6, 5, 4, 3, 2, 11], [13, 6, 5, 4, 12], [13], [13, 6, 7, 8, 14], [13, 6, 5, 4, 3, 2, 11, 15], [13, 6, 5, 4, 12, 16], [13, 17], [13, 6, 7, 8, 14, 18], [13, 6, 5, 4, 3, 2, 11, 15, 19], [13, 6, 5, 4, 12, 16, 20], [13, 17, 21], [13, 6, 7, 8, 14, 18, 22]], [[14, 8, 7, 6, 5, 4, 3, 2, 1], [14, 8, 7, 6, 5, 4, 3, 2], [14, 8, 7, 6, 5, 4, 3], [14, 8, 7, 6, 5, 4], [14, 8, 7, 6, 5], [14, 8, 7, 6], [14, 8, 7], [14, 8], [14], [14, 8], [14, 8, 9], [14, 8, 7, 6, 5, 4, 3, 2], [14, 8, 7, 6, 5, 4], [14, 8, 7, 6], [], [14, 8, 7, 6, 5, 4, 3, 2, 11], [14, 8, 7, 6, 5, 4, 12], [14, 8, 7, 6, 13], [14], [14, 8, 7, 6, 5, 4, 3, 2, 11, 15], [14, 8, 7, 6, 5, 4, 12, 16], [14, 8, 7, 6, 13, 17], [14, 18], [14, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [14, 8, 7, 6, 5, 4, 12, 16, 20], [14, 8, 7, 6, 13, 17, 21], [14, 18, 22]], [[15, 11, 2, 1], [15, 11, 2], [15, 11], [15, 11, 2], [15, 11, 2, 3], [15, 11, 2, 3, 4], [15, 11, 2, 3, 4, 5], [15, 11, 2, 3, 4, 5, 6], [15, 11, 2, 3, 4, 5, 6, 7], [15, 11, 2, 3, 4, 5, 6, 7, 8], [15, 11, 2, 3, 4, 5, 6, 7, 8, 9], [15], [15, 11, 2, 3, 4], [15, 11, 2, 3, 4, 5, 6], [15, 11, 2, 3, 4, 5, 6, 7, 8], [], [15, 11, 2, 3, 4, 12], [15, 11, 2, 3, 4, 5, 6, 13], [15, 11, 2, 3, 4, 5, 6, 7, 8, 14], [15], [15, 11, 2, 3, 4, 12, 16], [15, 11, 2, 3, 4, 5, 6, 13, 17], [
    15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18], [15, 19], [15, 11, 2, 3, 4, 12, 16, 20], [15, 11, 2, 3, 4, 5, 6, 13, 17, 21], [15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[16, 12, 4, 3, 2, 1], [16, 12, 4, 3, 2], [16, 12, 4, 3], [16, 12, 4], [16, 12], [16, 12, 4], [16, 12, 4, 5], [16, 12, 4, 5, 6], [16, 12, 4, 5, 6, 7], [16, 12, 4, 5, 6, 7, 8], [16, 12, 4, 5, 6, 7, 8, 9], [16, 12, 4, 3, 2], [16], [16, 12, 4, 5, 6], [16, 12, 4, 5, 6, 7, 8], [16, 12, 4, 3, 2, 11], [], [16, 12, 4, 5, 6, 13], [16, 12, 4, 5, 6, 7, 8, 14], [16, 12, 4, 3, 2, 11, 15], [16], [16, 12, 4, 5, 6, 13, 17], [16, 12, 4, 5, 6, 7, 8, 14, 18], [16, 12, 4, 3, 2, 11, 15, 19], [16, 20], [16, 12, 4, 5, 6, 13, 17, 21], [16, 12, 4, 5, 6, 7, 8, 14, 18, 22]], [[17, 13, 6, 5, 4, 3, 2, 1], [17, 13, 6, 5, 4, 3, 2], [17, 13, 6, 5, 4, 3], [17, 13, 6, 5, 4], [17, 13, 6, 5], [17, 13, 6], [17, 13], [17, 13, 6], [17, 13, 6, 7], [17, 13, 6, 7, 8], [17, 13, 6, 7, 8, 9], [17, 13, 6, 5, 4, 3, 2], [17, 13, 6, 5, 4], [17], [17, 13, 6, 7, 8], [17, 13, 6, 5, 4, 3, 2, 11], [17, 13, 6, 5, 4, 12], [], [17, 13, 6, 7, 8, 14], [17, 13, 6, 5, 4, 3, 2, 11, 15], [17, 13, 6, 5, 4, 12, 16], [17], [17, 13, 6, 7, 8, 14, 18], [17, 13, 6, 5, 4, 3, 2, 11, 15, 19], [17, 13, 6, 5, 4, 12, 16, 20], [17, 21], [17, 13, 6, 7, 8, 14, 18, 22]], [[18, 14, 8, 7, 6, 5, 4, 3, 2, 1], [18, 14, 8, 7, 6, 5, 4, 3, 2], [18, 14, 8, 7, 6, 5, 4, 3], [18, 14, 8, 7, 6, 5, 4], [18, 14, 8, 7, 6, 5], [18, 14, 8, 7, 6], [18, 14, 8, 7], [18, 14, 8], [18, 14], [18, 14, 8], [18, 14, 8, 9], [18, 14, 8, 7, 6, 5, 4, 3, 2], [18, 14, 8, 7, 6, 5, 4], [18, 14, 8, 7, 6], [18], [18, 14, 8, 7, 6, 5, 4, 3, 2, 11], [18, 14, 8, 7, 6, 5, 4, 12], [18, 14, 8, 7, 6, 13], [], [18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15], [18, 14, 8, 7, 6, 5, 4, 12, 16], [18, 14, 8, 7, 6, 13, 17], [18], [18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [18, 14, 8, 7, 6, 5, 4, 12, 16, 20], [18, 14, 8, 7, 6, 13, 17, 21], [18, 22]], [[19, 15, 11, 2, 1], [19, 15, 11, 2], [19, 15, 11], [19, 15, 11, 2], [19, 15, 11, 2, 3], [19, 15, 11, 2, 3, 4], [19, 15, 11, 2, 3, 4, 5], [19, 15, 11, 2, 3, 4, 5, 6], [19, 15, 11, 2, 3, 4, 5, 6, 7], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 9], [19, 15], [19, 15, 11, 2, 3, 4], [19, 15, 11, 2, 3, 4, 5, 6], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8], [19], [19, 15, 11, 2, 3, 4, 12], [19, 15, 11, 2, 3, 4, 5, 6, 13], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14], [], [19, 15, 11, 2, 3, 4, 12, 16], [19, 15, 11, 2, 3, 4, 5, 6, 13, 17], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18], [19], [19, 15, 11, 2, 3, 4, 12, 16, 20], [19, 15, 11, 2, 3, 4, 5, 6, 13, 17, 21], [19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[20, 16, 12, 4, 3, 2, 1], [20, 16, 12, 4, 3, 2], [20, 16, 12, 4, 3], [20, 16, 12, 4], [20, 16, 12], [20, 16, 12, 4], [20, 16, 12, 4, 5], [20, 16, 12, 4, 5, 6], [20, 16, 12, 4, 5, 6, 7], [20, 16, 12, 4, 5, 6, 7, 8], [20, 16, 12, 4, 5, 6, 7, 8, 9], [20, 16, 12, 4, 3, 2], [20, 16], [20, 16, 12, 4, 5, 6], [20, 16, 12, 4, 5, 6, 7, 8], [20, 16, 12, 4, 3, 2, 11], [20], [20, 16, 12, 4, 5, 6, 13], [20, 16, 12, 4, 5, 6, 7, 8, 14], [20, 16, 12, 4, 3, 2, 11, 15], [], [20, 16, 12, 4, 5, 6, 13, 17], [20, 16, 12, 4, 5, 6, 7, 8, 14, 18], [20, 16, 12, 4, 3, 2, 11, 15, 19], [20], [20, 16, 12, 4, 5, 6, 13, 17, 21], [20, 16, 12, 4, 5, 6, 7, 8, 14, 18, 22]], [[21, 17, 13, 6, 5, 4, 3, 2, 1], [21, 17, 13, 6, 5, 4, 3, 2], [21, 17, 13, 6, 5, 4, 3], [21, 17, 13, 6, 5, 4], [21, 17, 13, 6, 5], [21, 17, 13, 6], [21, 17, 13], [21, 17, 13, 6], [21, 17, 13, 6, 7], [21, 17, 13, 6, 7, 8], [21, 17, 13, 6, 7, 8, 9], [21, 17, 13, 6, 5, 4, 3, 2], [21, 17, 13, 6, 5, 4], [21, 17], [21, 17, 13, 6, 7, 8], [21, 17, 13, 6, 5, 4, 3, 2, 11], [21, 17, 13, 6, 5, 4, 12], [21], [21, 17, 13, 6, 7, 8, 14], [21, 17, 13, 6, 5, 4, 3, 2, 11, 15], [21, 17, 13, 6, 5, 4, 12, 16], [], [21, 17, 13, 6, 7, 8, 14, 18], [21, 17, 13, 6, 5, 4, 3, 2, 11, 15, 19], [21, 17, 13, 6, 5, 4, 12, 16, 20], [21], [21, 17, 13, 6, 7, 8, 14, 18, 22]], [[22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 1], [22, 18, 14, 8, 7, 6, 5, 4, 3, 2], [22, 18, 14, 8, 7, 6, 5, 4, 3], [22, 18, 14, 8, 7, 6, 5, 4], [22, 18, 14, 8, 7, 6, 5], [22, 18, 14, 8, 7, 6], [22, 18, 14, 8, 7], [22, 18, 14, 8], [22, 18, 14], [22, 18, 14, 8], [22, 18, 14, 8, 9], [22, 18, 14, 8, 7, 6, 5, 4, 3, 2], [22, 18, 14, 8, 7, 6, 5, 4], [22, 18, 14, 8, 7, 6], [22, 18], [22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11], [22, 18, 14, 8, 7, 6, 5, 4, 12], [22, 18, 14, 8, 7, 6, 13], [22], [22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15], [22, 18, 14, 8, 7, 6, 5, 4, 12, 16], [22, 18, 14, 8, 7, 6, 13, 17], [], [22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [22, 18, 14, 8, 7, 6, 5, 4, 12, 16, 20], [22, 18, 14, 8, 7, 6, 13, 17, 21], [22]], [[23, 19, 15, 11, 2, 1], [23, 19, 15, 11, 2], [23, 19, 15, 11], [23, 19, 15, 11, 2], [23, 19, 15, 11, 2, 3], [23, 19, 15, 11, 2, 3, 4], [23, 19, 15, 11, 2, 3, 4, 5], [23, 19, 15, 11, 2, 3, 4, 5, 6], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 9], [23, 19, 15], [23, 19, 15, 11, 2, 3, 4], [23, 19, 15, 11, 2, 3, 4, 5, 6], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8], [23, 19], [23, 19, 15, 11, 2, 3, 4, 12], [23, 19, 15, 11, 2, 3, 4, 5, 6, 13], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14], [23], [23, 19, 15, 11, 2, 3, 4, 12, 16], [23, 19, 15, 11, 2, 3, 4, 5, 6, 13, 17], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18], [], [23, 19, 15, 11, 2, 3, 4, 12, 16, 20], [23, 19, 15, 11, 2, 3, 4, 5, 6, 13, 17, 21], [23, 19, 15, 11, 2, 3, 4, 5, 6, 7, 8, 14, 18, 22]], [[24, 20, 16, 12, 4, 3, 2, 1], [24, 20, 16, 12, 4, 3, 2], [24, 20, 16, 12, 4, 3], [24, 20, 16, 12, 4], [24, 20, 16, 12], [24, 20, 16, 12, 4], [24, 20, 16, 12, 4, 5], [24, 20, 16, 12, 4, 5, 6], [24, 20, 16, 12, 4, 5, 6, 7], [24, 20, 16, 12, 4, 5, 6, 7, 8], [24, 20, 16, 12, 4, 5, 6, 7, 8, 9], [24, 20, 16, 12, 4, 3, 2], [24, 20, 16], [24, 20, 16, 12, 4, 5, 6], [24, 20, 16, 12, 4, 5, 6, 7, 8], [24, 20, 16, 12, 4, 3, 2, 11], [24, 20], [24, 20, 16, 12, 4, 5, 6, 13], [24, 20, 16, 12, 4, 5, 6, 7, 8, 14], [24, 20, 16, 12, 4, 3, 2, 11, 15], [24], [24, 20, 16, 12, 4, 5, 6, 13, 17], [24, 20, 16, 12, 4, 5, 6, 7, 8, 14, 18], [24, 20, 16, 12, 4, 3, 2, 11, 15, 19], [], [24, 20, 16, 12, 4, 5, 6, 13, 17, 21], [24, 20, 16, 12, 4, 5, 6, 7, 8, 14, 18, 22]], [[25, 21, 17, 13, 6, 5, 4, 3, 2, 1], [25, 21, 17, 13, 6, 5, 4, 3, 2], [25, 21, 17, 13, 6, 5, 4, 3], [25, 21, 17, 13, 6, 5, 4], [25, 21, 17, 13, 6, 5], [25, 21, 17, 13, 6], [25, 21, 17, 13], [25, 21, 17, 13, 6], [25, 21, 17, 13, 6, 7], [25, 21, 17, 13, 6, 7, 8], [25, 21, 17, 13, 6, 7, 8, 9], [25, 21, 17, 13, 6, 5, 4, 3, 2], [25, 21, 17, 13, 6, 5, 4], [25, 21, 17], [25, 21, 17, 13, 6, 7, 8], [25, 21, 17, 13, 6, 5, 4, 3, 2, 11], [25, 21, 17, 13, 6, 5, 4, 12], [25, 21], [25, 21, 17, 13, 6, 7, 8, 14], [25, 21, 17, 13, 6, 5, 4, 3, 2, 11, 15], [25, 21, 17, 13, 6, 5, 4, 12, 16], [25], [25, 21, 17, 13, 6, 7, 8, 14, 18], [25, 21, 17, 13, 6, 5, 4, 3, 2, 11, 15, 19], [25, 21, 17, 13, 6, 5, 4, 12, 16, 20], [], [25, 21, 17, 13, 6, 7, 8, 14, 18, 22]], [[26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 1], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3], [26, 22, 18, 14, 8, 7, 6, 5, 4], [26, 22, 18, 14, 8, 7, 6, 5], [26, 22, 18, 14, 8, 7, 6], [26, 22, 18, 14, 8, 7], [26, 22, 18, 14, 8], [26, 22, 18, 14], [26, 22, 18, 14, 8], [26, 22, 18, 14, 8, 9], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2], [26, 22, 18, 14, 8, 7, 6, 5, 4], [26, 22, 18, 14, 8, 7, 6], [26, 22, 18], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11], [26, 22, 18, 14, 8, 7, 6, 5, 4, 12], [26, 22, 18, 14, 8, 7, 6, 13], [26, 22], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15], [26, 22, 18, 14, 8, 7, 6, 5, 4, 12, 16], [26, 22, 18, 14, 8, 7, 6, 13, 17], [26], [26, 22, 18, 14, 8, 7, 6, 5, 4, 3, 2, 11, 15, 19], [26, 22, 18, 14, 8, 7, 6, 5, 4, 12, 16, 20], [26, 22, 18, 14, 8, 7, 6, 13, 17, 21], []]]
directions: list[list[list[int]]] = []

amphipods_1: list[str] = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
amphipods_2: list[str] = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D1", "D2", "D3", "D4"]
amphipods: list[str] = []

class State:
    def __init__(self, locations: dict[str, int]) -> None:
        self.locations: dict[str, int] = locations
        self.moved: dict[str, int] = {
            "A1": 0,
            "A2": 0,
            "A3": 0,
            "A4": 0,
            "B1": 0,
            "B2": 0,
            "B3": 0,
            "B4": 0,
            "C1": 0,
            "C2": 0,
            "C3": 0,
            "C4": 0,
            "D1": 0,
            "D2": 0,
            "D3": 0,
            "D4": 0
        }

    def __str__(self) -> str:
        return str(self.locations)

    def __hash__(self) -> int:
        return hash(str(self.locations))

    def __lt__(self, other: State) -> bool:
        return hash(self) < hash(other)

    def __eq__(self, other) -> bool:
        if isinstance(other, State):
            return self.locations == other.locations
        else:
            return False

    def finished(self) -> bool:
        for key, value in self.locations.items():
            if value not in homes[key[0]]:
                return False
        return True

    def can_reach(self, amphipod: str, goal: int) -> bool:
        for process in directions[self.locations[amphipod]][goal][1:]:
            if process in self.locations.values():
                return False
        return goal not in self.locations.values()

    def residents(self, amphipod: str) -> str:
        home: list[int] = homes[amphipod[0]]
        ret: str = ""
        for key, value in self.locations.items():
            if value in home:
                ret += key[0]
        return ret.upper()

    def generate_edges(self) -> list[tuple[State, int]]:
        ret: list[tuple[State, int]] = []
        for amphipod in amphipods:
            if self.moved[amphipod] > 2:
                continue

            current_location: int = self.locations[amphipod]
            residents: str = self.residents(amphipod)

            if residents.replace(amphipod[0], "") == "":
                try:
                    objective = homes[amphipod[0]][-1 - len(residents)]
                    if self.can_reach(amphipod, objective):
                        new: State = self.copy()
                        new.locations[amphipod] = objective
                        new.moved[amphipod] = 2
                        ret.append(
                            (new, costs[amphipod[0]] * len(directions[current_location][objective])))
                except IndexError as _:
                    pass

            if self.moved[amphipod] == 0:
                for objective in range(11):
                    if not self.can_reach(amphipod, objective):
                        continue

                    if objective in banned:
                        continue

                    new = self.copy()
                    new.locations[amphipod] = objective
                    new.moved[amphipod] = 1
                    ret.append(
                        (new, costs[amphipod[0]] * len(directions[current_location][objective])))

        return ret

    def copy(self) -> State:
        ret: State = State(self.locations.copy())
        ret.moved = self.moved.copy()
        return ret


def parse_inp(inp: list[str], part: int = 1) -> State:
    combined_inp: str = "".join(inp)
    for letter in "ABCD":
        combined_inp = combined_inp.replace(letter, letter.lower(), 1)
    combined_inp = "".join([char for char in combined_inp if char.isalpha()])

    if part == 2:
        combined_inp = combined_inp[:4] + "........" + combined_inp[4:]
        locations: dict[str, int] = {letter: combined_inp.index(letter) + 11 for letter in combined_inp if letter != "."}
        return State({
            "A1": locations["a"],
            "A2": locations["A"],
            "A3": 18,
            "A4": 21,
            "B1": locations["b"],
            "B2": locations["B"],
            "B3": 17,
            "B4": 20,
            "C1": locations["c"],
            "C2": locations["C"],
            "C3": 16,
            "C4": 22,
            "D1": locations["d"],
            "D2": locations["D"],
            "D3": 15,
            "D4": 19
        })
    
    locations = {letter: combined_inp.index(letter) + 11 for letter in combined_inp if letter != "."}
    return State({
        "A1": locations["a"],
        "A2": locations["A"],
        "B1": locations["b"],
        "B2": locations["B"],
        "C1": locations["c"],
        "C2": locations["C"],
        "D1": locations["d"],
        "D2": locations["D"],
    })


def main_part_1(inp: list[str]) -> OUTPUT_TYPE:
    global directions, homes, amphipods
    directions = directions_1
    homes = homes_1
    amphipods = amphipods_1

    t: float = time.time()
    state: State = parse_inp(inp, 1)
    best_found: dict[State, int] = {state: 0}
    states: list[tuple[int, State]] = []
    heapq.heappush(states, (0, state))
    low_score: int = 0
    prev_states: int = 0
    while states:
        score: int
        current_state: State

        score, current_state = heapq.heappop(states)
        if score != low_score:
            print(
                f"Checked upto score: {low_score}, {len(states)}(+{len(states) - prev_states}) states left, {time.time() - t}s used")
            low_score = score
            prev_states = len(states)

        print(f"Checking state: {current_state}")

        if current_state.finished():
            return score

        for path, cost in current_state.generate_edges():
            cost += score

            if path in best_found.keys() and best_found[path] <= cost:
                continue

            best_found[path] = cost
            heapq.heappush(states, (cost, path))
            print(f"Appended state: {path} / cost: {cost}")

    return 0


def main_part_2(inp: list[str]) -> OUTPUT_TYPE:
    global directions, homes, amphipods
    directions = directions_2
    homes = homes_2
    amphipods = amphipods_2

    t: float = time.time()
    state: State = parse_inp(inp, 2)
    best_found: dict[State, int] = {state: 0}
    states: list[tuple[int, State]] = []
    heapq.heappush(states, (0, state))
    low_score: int = 0
    prev_states: int = 0
    while states:
        score: int
        current_state: State

        score, current_state = heapq.heappop(states)
        if score != low_score:
            print(
                f"Checked upto score: {low_score}, {len(states)}(+{len(states) - prev_states}) states left, {time.time() - t}s used")
            low_score = score
            prev_states = len(states)

        print(f"Checking state: {current_state}")

        if current_state.finished():
            return score

        for path, cost in current_state.generate_edges():
            cost += score

            if path in best_found.keys() and best_found[path] <= cost:
                continue

            best_found[path] = cost
            heapq.heappush(states, (cost, path))
            print(f"Appended state: {path} / cost: {cost}")
    
    return 0


def main() -> None:
    test_input: str = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
    test_input_parsed: list[str] = test_input.split("\n")
    test_output_part_1_expected: OUTPUT_TYPE = 12521
    test_output_part_2_expected: OUTPUT_TYPE = 44169

    file_location: str = "Day 23/input.txt"
    input_file: list[str] = open(file_location, "r").readlines()

    test_output_part_1: OUTPUT_TYPE = main_part_1(test_input_parsed)
    test_output_part_2: OUTPUT_TYPE = main_part_2(test_input_parsed)

    if test_output_part_1_expected == test_output_part_1:
        print(f"Part 1: {main_part_1(input_file)}")
    else:
        print(f"Part 1 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_1_expected}")
        print(f"Got: {test_output_part_1}")
        print()

    if test_output_part_2_expected == test_output_part_2:
        print(f"Part 2: {main_part_2(input_file)}")
    else:
        print(f"Part 2 testing error: ")
        print(f"Test input: {test_input}")
        print(f"Expected output: {test_output_part_2_expected}")
        print(f"Got: {test_output_part_2}")


if __name__ == "__main__":
    main()