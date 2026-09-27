from src.constants.image_constants import ImageConstants


class ResizeImageCommand:

    def __init__(self, image_processing_provider):
        self.image_processing_provider = image_processing_provider

    async def execute(self, image, target_width, target_height):
        image_height, image_width = image.shape[:2]

        if target_width is None and target_height is None:
            target_width = image_width
            target_height = image_height
        elif target_width is not None and target_height is None:
            resize_ratio = target_width / float(image_width)
            target_height = int(image_height * resize_ratio)
        elif target_height is not None and target_width is None:
            resize_ratio = target_height / float(image_height)
            target_width = int(image_width * resize_ratio)

        resized_image = await self.image_processing_provider.resize_image(image, target_width, target_height)
        return resized_image
