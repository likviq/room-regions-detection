import asyncio

import cv2
import numpy as np

from src.constants.image_constants import ImageConstants


class ImageProcessingProvider:

    def __init__(self):
        self.line_detector = None

    async def resize_image(self, image, target_width, target_height):
        resized_image = await asyncio.to_thread(self._resize_image, image, target_width, target_height)
        return resized_image

    async def create_line_detector(self):
        if self.line_detector is None:
            self.line_detector = await asyncio.to_thread(cv2.createLineSegmentDetector, ImageConstants.LINE_DETECTOR_MODE)
        line_detector = self.line_detector
        return line_detector

    async def split_color_channels(self, image):
        channels = await asyncio.to_thread(cv2.split, image)
        return channels

    async def detect_lines(self, image, line_detector):
        detection = await asyncio.to_thread(line_detector.detect, image)
        lines = detection[0]
        return lines

    async def draw_segments(self, image, lines, line_detector):
        drawn_image = await asyncio.to_thread(line_detector.drawSegments, image, lines)
        return drawn_image

    async def create_flood_mask(self, image):
        image_height, image_width = image.shape[:2]
        flood_mask = np.zeros((image_height + 2, image_width + 2), np.uint8)
        return flood_mask

    async def copy_image(self, image):
        copied_image = await asyncio.to_thread(image.copy)
        return copied_image

    async def flood_fill(self, image, flood_mask, seed, fill_color, tolerance):
        await asyncio.to_thread(
            cv2.floodFill,
            image,
            flood_mask,
            seed,
            fill_color,
            loDiff=(tolerance, tolerance, tolerance),
            upDiff=(tolerance, tolerance, tolerance),
            flags=4 | cv2.FLOODFILL_FIXED_RANGE,
        )

    async def create_color_mask(self, image, fill_color):
        background_mask = np.all(image == fill_color, axis=-1)
        return background_mask

    async def create_region_visited_mask(self, image):
        image_height, image_width = image.shape[:2]
        visited = np.zeros((image_height, image_width), dtype=bool)
        return visited

    async def convert_to_int16(self, image):
        converted_image = image.astype(np.int16)
        return converted_image

    async def create_connected_components(self, free_mask):
        connected_components = await asyncio.to_thread(
            cv2.connectedComponentsWithStats,
            free_mask.astype(np.uint8),
            ImageConstants.EIGHT_CONNECTED_NEIGHBORS,
        )
        return connected_components

    async def create_random_generator(self):
        generator = np.random.RandomState(0)
        return generator

    async def create_random_color(self, generator):
        color = np.array([int(channel) for channel in generator.randint(60, 255, size=3)])
        return color

    async def draw_text_size(self, text):
        text_size = await asyncio.to_thread(cv2.getTextSize, text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)
        return text_size

    async def draw_rectangle(self, image, first_point, second_point):
        await asyncio.to_thread(cv2.rectangle, image, first_point, second_point, (0, 0, 0), -1)

    async def draw_text(self, image, text, position):
        await asyncio.to_thread(cv2.putText, image, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

    async def draw_line(self, image, first_point, second_point):
        await asyncio.to_thread(cv2.line, image, first_point, second_point, (0, 255, 0), 2)

    def _resize_image(self, image, target_width, target_height):
        resized_image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
        return resized_image
