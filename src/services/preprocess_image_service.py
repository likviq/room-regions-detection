from src.enums.background_removal_state import BackgroundRemovalState


class PreprocessImageService:

    def __init__(self, resize_image_command, remove_background_command):
        self.resize_image_command = resize_image_command
        self.remove_background_command = remove_background_command

    async def preprocess_image(self, image, target_width, target_height, background_removal_state, background_tolerance):
        resized_image = await self.resize_image_command.execute(image, target_width, target_height)

        if background_removal_state == BackgroundRemovalState.ENABLED:
            processed_image, background_mask = await self.remove_background_command.execute(resized_image, background_tolerance)
            return processed_image

        processed_image = resized_image
        return processed_image
