from src.view_models.process_image.process_image_response import ProcessImageResponse


class ProcessImageService:

    def __init__(self, preprocess_image_service, detect_lines_service, segment_rooms_service, label_rooms_service):
        self.preprocess_image_service = preprocess_image_service
        self.detect_lines_service = detect_lines_service
        self.segment_rooms_service = segment_rooms_service
        self.label_rooms_service = label_rooms_service

    async def process_image(self, request):
        preprocessed_image = await self.preprocess_image_service.preprocess_image(
            request.image,
            request.target_width,
            request.target_height,
            request.background_removal_state,
            request.background_tolerance,
        )

        detected_lines = await self.detect_lines_service.detect_lines(preprocessed_image)
        segmentation = await self.segment_rooms_service.segment_rooms(
            preprocessed_image,
            detected_lines,
            request.region_threshold,
            request.seed_offset,
        )

        labeled_image, rooms, rooms_json = await self.label_rooms_service.label_rooms(
            preprocessed_image,
            segmentation,
            request.minimum_room_area,
            request.overlay_alpha,
        )

        labeled_image = labeled_image
        response = ProcessImageResponse(preprocessed_image, detected_lines, segmentation, labeled_image, rooms, rooms_json)
        return response
