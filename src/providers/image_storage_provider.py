import asyncio

import cv2


class ImageStorageProvider:

    async def read_image(self, image_path):
        image = await asyncio.to_thread(cv2.imread, image_path)
        return image

    async def write_image(self, image_path, image):
        write_completed = await asyncio.to_thread(cv2.imwrite, image_path, image)
        return write_completed
