from src.entities.seed_points_entity import SeedPointsEntity


class CalculateSeedPointsCommand:

    async def execute(self, longest_line, seed_offset):
        first_x, first_y = longest_line.first_point
        second_x, second_y = longest_line.second_point

        direction_x = second_x - first_x
        direction_y = second_y - first_y
        line_length = (direction_x ** 2 + direction_y ** 2) ** 0.5

        if line_length == 0:
            raise ValueError("The longest detected line has zero length")

        normalized_direction_x = direction_x / line_length
        normalized_direction_y = direction_y / line_length
        normal_x = -normalized_direction_y
        normal_y = normalized_direction_x

        middle_x = (first_x + second_x) / 2
        middle_y = (first_y + second_y) / 2

        first_seed_point = (middle_x + normal_x * seed_offset, middle_y + normal_y * seed_offset)
        second_seed_point = (middle_x - normal_x * seed_offset, middle_y - normal_y * seed_offset)

        seed_points = SeedPointsEntity(first_seed_point, second_seed_point)
        return seed_points
