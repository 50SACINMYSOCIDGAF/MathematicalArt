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

        # Handle each direction, updating position and storing line segments
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

    # Merge overlapping line segments to simplify processing
    def merge(intervals):
        """
        Merge overlapping intervals to reduce computational complexity.

        Example:
        [(1,3), (2,4), (5,7)] -> [(1,4), (5,7)]
        """
        if not intervals:
            return []

        intervals.sort()

        merged = []
        current_start, current_end = intervals[0]

        # Iterate through intervals, merging overlapping segments
        for start, end in intervals:
            if start <= current_end:
                # Overlapping or adjacent interval, extend current segment
                current_end = max(current_end, end)
            else:
                # Non-overlapping interval, add previous segment and start new one
                merged.append((current_start, current_end))
                current_start, current_end = start, end

        # Add the last segment
        merged.append((current_start, current_end))
        return merged

    # Merge overlapping segments for both horizontal and vertical lines
    for y_coord in horizontal:
        horizontal[y_coord] = merge(horizontal[y_coord])
    for x_coord in vertical:
        vertical[x_coord] = merge(vertical[x_coord])

    # Collect unique y-coordinates from both horizontal and vertical lines
    unique_ys = set()
    for y_coord in horizontal:
        unique_ys.add(y_coord)
    for x_coord in vertical:
        for y_start, y_end in vertical[x_coord]:
            unique_ys.add(y_start)
            unique_ys.add(y_end)

    # Create a mapping of y-coordinates to indices for efficient processing
    sorted_ys = sorted(unique_ys)
    y_to_idx = {y: idx for idx, y in enumerate(sorted_ys)}

    events = []
    for x_coord in vertical:
        for y_start, y_end in vertical[x_coord]:
            # 'add' event when line starts, 'remove' event when line ends
            events.append((y_start, 'add', x_coord))
            events.append((y_end, 'remove', x_coord))

    # Sort events by y-coordinate, with 'add' events processed before 'remove' events
    events.sort(key=lambda event: (event[0], 0 if event[1] == 'add' else 1))

    active_x = []
    active_x_set = set()
    event_idx = 0
    plus_signs = 0

    sorted_horizontal = sorted(horizontal.items(), key=lambda item: y_to_idx[item[0]])

    # Binary search to check if a y-coordinate is within a vertical line segment
    def is_y_in_segment(y, segments):
        left, right = 0, len(segments)
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
        # Process vertical line segment events up to current y-coordinate
        while event_idx < len(events) and events[event_idx][0] <= y:
            if events[event_idx][1] == 'add':
                # Add x-coordinate to active set when vertical line starts
                insort(active_x, events[event_idx][2])
                active_x_set.add(events[event_idx][2])
            else:
                # Remove x-coordinate from active set when vertical line ends
                idx = bisect_left(active_x, events[event_idx][2])
                if idx < len(active_x) and active_x[idx] == events[event_idx][2]:
                    active_x.pop(idx)
                    active_x_set.discard(events[event_idx][2])
            event_idx += 1

        for x_start, x_end in segments:
            # Find candidate x-coordinates between horizontal segment bounds
            left = bisect_right(active_x, x_start)
            right = bisect_left(active_x, x_end)
            candidates = active_x[left:right]

            # Check each candidate for a plus sign
            for x in candidates:
                if x > x_start and x < x_end:
                    # Verify vertical line exists at this x-coordinate
                    if is_y_in_segment(y, vertical[x]):
                        plus_signs += 1

    return plus_signs