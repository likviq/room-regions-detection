from src.entities.segmentation_entity import SegmentationEntity


class SegmentRoomsService:

    def __init__(self, find_longest_line_command, calculate_seed_points_command, find_color_region_command):
        self.find_longest_line_command = find_longest_line_command
        self.calculate_seed_points_command = calculate_seed_points_command
        self.find_color_region_command = find_color_region_command

    async def segment_rooms(self, color_image, lines, region_threshold, seed_offset):
        self._validate_lines(lines)

        longest_line, longest_length = await self.find_longest_line_command.execute(lines)
        seed_points = await self.calculate_seed_points_command.execute(longest_line, seed_offset)

        first_region = await self.find_color_region_command.execute(color_image, seed_points.first_point, region_threshold)
        second_region = await self.find_color_region_command.execute(color_image, seed_points.second_point, region_threshold)

        segmentation = SegmentationEntity(first_region, second_region, longest_line, seed_points)
        return segmentation

    def _validate_lines(self, lines):
        if lines is None or len(lines) == 0:
            raise ValueError("No lines were detected")
