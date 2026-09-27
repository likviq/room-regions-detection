from collections import deque

import numpy as np

from src.constants.image_constants import ImageConstants


class FindColorRegionCommand:

    def __init__(self, image_processing_provider):
        self.image_processing_provider = image_processing_provider

    async def execute(self, color_image, start_point, threshold):
        image_height, image_width = color_image.shape[:2]
        visited = await self.image_processing_provider.create_region_visited_mask(color_image)
        start_x, start_y = self._normalize_start_point(start_point)

        if not self._is_start_point_inside_image(start_x, start_y, image_width, image_height):
            return visited

        queue = deque([(start_x, start_y)])
        visited[start_y, start_x] = True
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        image_int = await self.image_processing_provider.convert_to_int16(color_image)

        while queue:
            current_x, current_y = queue.popleft()
            current_pixel = image_int[current_y, current_x]

            for direction_x, direction_y in neighbors:
                neighbor_x = current_x + direction_x
                neighbor_y = current_y + direction_y

                if self._is_neighbor_outside_or_visited(neighbor_x, neighbor_y, image_width, image_height, visited):
                    continue

                neighbor_pixel = image_int[neighbor_y, neighbor_x]
                pixel_difference = np.abs(neighbor_pixel - current_pixel)

                if np.all(pixel_difference <= threshold):
                    visited[neighbor_y, neighbor_x] = True
                    queue.append((neighbor_x, neighbor_y))

        return visited

    def _normalize_start_point(self, start_point):
        start_x = int(round(start_point[0]))
        start_y = int(round(start_point[1]))
        return start_x, start_y

    def _is_start_point_inside_image(self, start_x, start_y, image_width, image_height):
        is_inside = 0 <= start_x < image_width and 0 <= start_y < image_height
        return is_inside

    def _is_neighbor_outside_or_visited(self, neighbor_x, neighbor_y, image_width, image_height, visited):
        is_outside = neighbor_x < 0 or neighbor_x >= image_width or neighbor_y < 0 or neighbor_y >= image_height

        if is_outside:
            return True

        is_visited = visited[neighbor_y, neighbor_x]
        return is_visited
