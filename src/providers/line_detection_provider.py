class LineDetectionProvider:

    def __init__(self, image_processing_provider):
        self.image_processing_provider = image_processing_provider

    async def create_detector(self):
        line_detector = await self.image_processing_provider.create_line_detector()
        return line_detector

    async def detect_lines(self, image, line_detector):
        lines = await self.image_processing_provider.detect_lines(image, line_detector)
        return lines

    async def split_channels(self, image):
        channels = await self.image_processing_provider.split_color_channels(image)
        return channels

    async def draw_segments(self, image, lines, line_detector):
        drawn_image = await self.image_processing_provider.draw_segments(image, lines, line_detector)
        return drawn_image
