class DetectedLineEntity:

    def __init__(self, first_point, second_point):
        self.first_point = first_point
        self.second_point = second_point

    async def calculate_length(self):
        first_x, first_y = self.first_point
        second_x, second_y = self.second_point
        length = ((second_x - first_x) ** 2 + (second_y - first_y) ** 2) ** 0.5
        return length
