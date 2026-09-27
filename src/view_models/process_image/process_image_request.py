class ProcessImageRequest:

    def __init__(self, image, target_width, target_height, background_removal_state, background_tolerance, region_threshold, seed_offset, minimum_room_area, overlay_alpha):
        self.image = image
        self.target_width = target_width
        self.target_height = target_height
        self.background_removal_state = background_removal_state
        self.background_tolerance = background_tolerance
        self.region_threshold = region_threshold
        self.seed_offset = seed_offset
        self.minimum_room_area = minimum_room_area
        self.overlay_alpha = overlay_alpha
