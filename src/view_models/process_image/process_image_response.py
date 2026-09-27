class ProcessImageResponse:

    def __init__(self, preprocessed_image, detected_lines, segmentation, labeled_image, room_labels, rooms_json):
        self.preprocessed_image = preprocessed_image
        self.detected_lines = detected_lines
        self.segmentation = segmentation
        self.labeled_image = labeled_image
        self.room_labels = room_labels
        self.rooms_json = rooms_json
