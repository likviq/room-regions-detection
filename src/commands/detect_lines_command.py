import numpy as np


class DetectLinesCommand:

    def __init__(self, line_detection_provider):
        self.line_detection_provider = line_detection_provider

    async def execute(self, image):
        line_detector = await self.line_detection_provider.create_detector()
        channels = await self.line_detection_provider.split_channels(image)
        detected_lines = []

        for channel in channels:
            channel_lines = await self.line_detection_provider.detect_lines(channel, line_detector)

            if channel_lines is not None:
                detected_lines.extend(channel_lines)

        if detected_lines:
            detected_lines_array = np.array(detected_lines)
        else:
            detected_lines_array = None

        return detected_lines_array
