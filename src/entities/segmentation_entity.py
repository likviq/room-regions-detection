class SegmentationEntity:

    def __init__(self, first_region, second_region, longest_line, seed_points):
        self.first_region = first_region
        self.second_region = second_region
        self.longest_line = longest_line
        self.seed_points = seed_points
