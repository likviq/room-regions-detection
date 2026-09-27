import numpy as np

from src.constants.image_constants import ImageConstants


class RemoveBackgroundCommand:

    def __init__(self, image_processing_provider):
        self.image_processing_provider = image_processing_provider

    async def execute(self, image, tolerance):
        image_height, image_width = image.shape[:2]
        flood_mask = await self.image_processing_provider.create_flood_mask(image)
        processed_image = await self.image_processing_provider.copy_image(image)
        fill_color = (0, 0, 0)
        seed_points = [(0, 0), (image_width - 1, 0), (0, image_height - 1), (image_width - 1, image_height - 1)]

        for seed_point in seed_points:
            await self.image_processing_provider.flood_fill(processed_image, flood_mask, seed_point, fill_color, tolerance)

        background_mask = await self.image_processing_provider.create_color_mask(processed_image, fill_color)
        return processed_image, background_mask
