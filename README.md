# Meta Careers: Plus Sign Painting on a Cartesian Plane Challenge (L4)

## Problem Description

This algorithmic challenge involves creating a mathematical painting on a 2D Cartesian plane with specific rules for stroke placement and plus sign detection.

### Key Constraints

- Starting point: (0, 0)
- Strokes are axis-aligned (horizontal or vertical)
- Brush is not lifted between strokes
- Challenge is to count unique plus sign positions

### Plus Sign Definition

A plus sign occurs at a point if paint segments exist in all four cardinal directions:
- Up
- Down
- Left
- Right

## Solution Approach

The current implementation employs sophisticated techniques:
- Uses `defaultdict` for tracking horizontal and vertical lines
- Interval merging to handle overlapping line segments
- Binary search for efficient plus sign detection
- Time complexity: Approximately O(N log N)

### Current Performance

- Passes 32/33 test cases
- Optimisation opportunities remain for the final test case

## Potential Improvements

- Refine interval merging logic
- Enhance coordinate tracking precision
- Implement more robust plus sign validation mechanism

## Complexity Considerations

- Spatial tracking of line segments
- Efficient event-based processing
- Minimising computational overhead while maintaining accuracy

## Note

Solution represents an intricate geometric computation challenge, requiring meticulous algorithmic design.
