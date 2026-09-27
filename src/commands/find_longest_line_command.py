from src.entities.detected_line_entity import DetectedLineEntity


class FindLongestLineCommand:

    async def execute(self, lines):
        longest_line = None
        longest_length = -1.0

        for line in lines:
            first_x, first_y, second_x, second_y = line.reshape(-1)
            detected_line = DetectedLineEntity((first_x, first_y), (second_x, second_y))
            line_length = await detected_line.calculate_length()

            if line_length > longest_length:
                longest_length = line_length
                longest_line = detected_line

        return longest_line, longest_length
