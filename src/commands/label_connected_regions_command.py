from collections import deque

import cv2
import numpy as np

from src.constants.image_constants import ImageConstants
from src.entities.room_entity import RoomEntity
from src.entities.room_segment_entity import RoomSegmentEntity


class LabelConnectedRegionsCommand:
    def __init__(self, image_processing_provider):
        self.image_processing_provider = image_processing_provider

    async def execute(self, color_img, visited_a, visited_b, min_area, alpha):
        rooms = []
        room_identifier = 1
        height, width = color_img.shape[:2]

        labeled_image = color_img.copy()

        for start_y in range(height):
            for start_x in range(width):
                if visited_a[start_y, start_x]:
                    continue

                if visited_b[start_y, start_x]:
                    continue

                component_mask = await self._find_component(color_img, start_x, start_y, visited_a, visited_b)

                area = int(np.count_nonzero(component_mask))

                if area < min_area:
                    continue

                centroid = await self._calculate_centroid(component_mask)
                segments = await self._calculate_segments(component_mask)
                room = RoomEntity(room_identifier, area, centroid, segments)

                # --- Заливка регіону кольором ---
                fill_color = await self._create_random_color()
                mask_bool = component_mask.astype(bool)
                labeled_image[mask_bool] = (
                    labeled_image[mask_bool] * (1 - alpha) + np.array(fill_color) * alpha
                ).astype(np.uint8)

                rooms.append(room)
                room_identifier += 1

        labeled_image = await self._draw_room_identifiers(labeled_image, rooms)

        return labeled_image, rooms

    async def _draw_room_identifiers(self, labeled_image, rooms):
        for room in rooms:
            center_x = room.centroid["x"]
            center_y = room.centroid["y"]
            text = str(room.room_identifier)

            # Маркер центроїда — контрастна крапка (біла з чорною обводкою)
            cv2.circle(labeled_image, (center_x, center_y), 6, (0, 0, 0), -1)
            cv2.circle(labeled_image, (center_x, center_y), 4, (255, 255, 255), -1)

            # Текст з обводкою: спочатку товста чорна лінія (контур), потім білий текст поверх
            cv2.putText(
                labeled_image,
                text,
                (center_x + 8, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                4,          # товщина обводки
                cv2.LINE_AA
            )
            cv2.putText(
                labeled_image,
                text,
                (center_x + 8, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1,          # тонший, поверх обводки
                cv2.LINE_AA
            )

        return labeled_image

    async def _find_component(self, color_img, start_x, start_y, visited_a, visited_b):
        height, width = color_img.shape[:2]
        component_mask = np.zeros((height, width), dtype=np.uint8)
        queue = deque([(start_x, start_y)])
        neighbors = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

        visited_a[start_y, start_x] = True
        component_mask[start_y, start_x] = 1

        while queue:
            current_x, current_y = queue.popleft()

            for offset_x, offset_y in neighbors:
                next_x = current_x + offset_x
                next_y = current_y + offset_y

                if next_x < 0 or next_x >= width:
                    continue

                if next_y < 0 or next_y >= height:
                    continue

                if visited_a[next_y, next_x]:
                    continue

                if visited_b[next_y, next_x]:
                    continue

                visited_a[next_y, next_x] = True
                component_mask[next_y, next_x] = 1
                queue.append((next_x, next_y))

        return component_mask

    async def _calculate_centroid(self, component_mask):
        moments = cv2.moments(component_mask)

        centroid_x = 0
        centroid_y = 0

        if moments["m00"] != 0:
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])

        return {"x": centroid_x, "y": centroid_y}

    async def _calculate_segments(self, component_mask):
        contours, _ = cv2.findContours(
            component_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        segments = []

        for contour in contours:
            points = contour.reshape(-1, 2)

            if len(points) < 2:
                continue

            for index in range(len(points) - 1):
                start_point = (
                    int(points[index][0]),
                    int(points[index][1]),
                )
                end_point = (
                    int(points[index + 1][0]),
                    int(points[index + 1][1]),
                )

                segment = RoomSegmentEntity(start_point, end_point)
                segments.append(segment)

            first_point = (
                int(points[0][0]),
                int(points[0][1]),
            )
            last_point = (
                int(points[-1][0]),
                int(points[-1][1]),
            )

            segment = RoomSegmentEntity(last_point, first_point)
            segments.append(segment)

        return segments

    async def _create_labeled_image(self, color_img, rooms, alpha):
        labeled_image = color_img.copy()

        for room in rooms:
            color = await self._create_random_color()
            center_x = room.centroid["x"]
            center_y = room.centroid["y"]

            cv2.circle(labeled_image, (center_x, center_y), 5, color, -1)

            text = str(room.room_identifier)

            cv2.putText(
                labeled_image,
                text,
                (center_x, center_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

        return labeled_image

    async def _create_random_color(self):
        generator = np.random.default_rng()
        color = generator.integers(0, 255, size=3).tolist()

        return tuple(color)
