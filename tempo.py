from typing import List, Tuple
from bisect import bisect_left, bisect_right, insort
from collections import defaultdict



def getPlusSignCount(N: int, L: List[int], D: str) -> int:
    horizontal = defaultdict(list)  # y: list of (x_start, x_end)
    vertical = defaultdict(list)  # x: list of (y_start, y_end)

    x, y = 0, 0
    for i in range(N):
        dir = D[i]
        length = L[i]
        if dir == 'U':
            new_y = y + length
            vertical[x].append((y, new_y))
            y = new_y
        elif dir == 'D':
            new_y = y - length
            vertical[x].append((new_y, y))
            y = new_y
        elif dir == 'L':
            new_x = x - length
            horizontal[y].append((new_x, x))
            x = new_x
        elif dir == 'R':
            new_x = x + length
            horizontal[y].append((x, new_x))
            x = new_x

    # Function to merge intervals
    def merge(intervals):
        if not intervals:
            return []
        intervals.sort()
        merged = []
        current_start, current_end = intervals[0]
        for start, end in intervals:
            if start <= current_end:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        merged.append((current_start, current_end))
        return merged

    # Merge intervals for horizontal and vertical lines
    for y_coord in horizontal:
        horizontal[y_coord] = merge(horizontal[y_coord])
    for x_coord in vertical:
        vertical[x_coord] = merge(vertical[x_coord])

    unique_ys = set()
    for y_coord in horizontal:
        unique_ys.add(y_coord)
    for x_coord in vertical:
        for y_start, y_end in vertical[x_coord]:
            unique_ys.add(y_start)
            unique_ys.add(y_end)
    sorted_ys = sorted(unique_ys)
    y_to_idx = {y: idx for idx, y in enumerate(sorted_ys)}

    events = []
    for x_coord in vertical:
        for y_start, y_end in vertical[x_coord]:
            events.append((y_start, 'add', x_coord))
            events.append((y_end, 'remove', x_coord))

    events.sort(key=lambda event: (event[0], 0 if event[1] == 'add' else 1))

    active_x = []
    active_x_set = set()
    event_idx = 0
    plus_signs = 0

    sorted_horizontal = sorted(horizontal.items(), key=lambda item: y_to_idx[item[0]])

    def is_y_in_segment(y, segments):
        left = 0
        right = len(segments)
        while left < right:
            mid = (left + right) // 2
            if segments[mid][0] < y < segments[mid][1]:
                return True
            elif y < segments[mid][0]:
                right = mid
            else:
                left = mid + 1
        return False

    for y, segments in sorted_horizontal:
        while event_idx < len(events) and events[event_idx][0] <= y:
            if events[event_idx][1] == 'add':
                insort(active_x, events[event_idx][2])
                active_x_set.add(events[event_idx][2])
            else:
                idx = bisect_left(active_x, events[event_idx][2])
                if idx < len(active_x) and active_x[idx] == events[event_idx][2]:
                    active_x.pop(idx)
                    active_x_set.discard(events[event_idx][2])
            event_idx += 1

        for x_start, x_end in segments:
            left = bisect_right(active_x, x_start)
            right = bisect_left(active_x, x_end)
            candidates = active_x[left:right]
            for x in candidates:
                if x > x_start and x < x_end:
                    if is_y_in_segment(y, vertical[x]):
                        plus_signs += 1

    return plus_signs


