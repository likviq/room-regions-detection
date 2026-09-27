class DetectLinesService:

    def __init__(self, detect_lines_command):
        self.detect_lines_command = detect_lines_command

    async def detect_lines(self, image):
        detected_lines = await self.detect_lines_command.execute(image)
        return detected_lines
