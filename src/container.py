from src.commands.calculate_seed_points_command import CalculateSeedPointsCommand
from src.commands.detect_lines_command import DetectLinesCommand
from src.commands.find_color_region_command import FindColorRegionCommand
from src.commands.find_longest_line_command import FindLongestLineCommand
from src.commands.label_connected_regions_command import LabelConnectedRegionsCommand
from src.commands.remove_background_command import RemoveBackgroundCommand
from src.commands.resize_image_command import ResizeImageCommand
from src.commands.save_room_segments_command import SaveRoomSegmentsCommand
from src.providers.image_processing_provider import ImageProcessingProvider
from src.providers.image_storage_provider import ImageStorageProvider
from src.providers.json_storage_provider import JsonStorageProvider
from src.providers.line_detection_provider import LineDetectionProvider
from src.services.detect_lines_service import DetectLinesService
from src.services.label_rooms_service import LabelRoomsService
from src.services.preprocess_image_service import PreprocessImageService
from src.services.process_image_service import ProcessImageService
from src.services.segment_rooms_service import SegmentRoomsService


class Container:

    def __init__(self):
        self.image_processing_provider = None
        self.image_storage_provider = None
        self.line_detection_provider = None

    def get_image_processing_provider(self):
        if self.image_processing_provider is None:
            self.image_processing_provider = ImageProcessingProvider()
        image_processing_provider = self.image_processing_provider
        return image_processing_provider

    def get_image_storage_provider(self):
        if self.image_storage_provider is None:
            self.image_storage_provider = ImageStorageProvider()
        image_storage_provider = self.image_storage_provider
        return image_storage_provider

    def get_line_detection_provider(self):
        if self.line_detection_provider is None:
            image_processing_provider = self.get_image_processing_provider()
            self.line_detection_provider = LineDetectionProvider(image_processing_provider)
        line_detection_provider = self.line_detection_provider
        return line_detection_provider

    def create_process_image_service(self):
        image_processing_provider = self.get_image_processing_provider()
        line_detection_provider = self.get_line_detection_provider()
        json_storage_provider = JsonStorageProvider()

        resize_image_command = ResizeImageCommand(image_processing_provider)
        remove_background_command = RemoveBackgroundCommand(image_processing_provider)
        detect_lines_command = DetectLinesCommand(line_detection_provider)
        find_longest_line_command = FindLongestLineCommand()
        calculate_seed_points_command = CalculateSeedPointsCommand()
        find_color_region_command = FindColorRegionCommand(image_processing_provider)
        label_connected_regions_command = LabelConnectedRegionsCommand(image_processing_provider)
        save_room_segments_command = SaveRoomSegmentsCommand(json_storage_provider)

        preprocess_image_service = PreprocessImageService(resize_image_command, remove_background_command)
        detect_lines_service = DetectLinesService(detect_lines_command)
        segment_rooms_service = SegmentRoomsService(find_longest_line_command, calculate_seed_points_command, find_color_region_command)
        label_rooms_service = LabelRoomsService(label_connected_regions_command, save_room_segments_command)

        process_image_service = ProcessImageService(
            preprocess_image_service,
            detect_lines_service,
            segment_rooms_service,
            label_rooms_service,
        )
        return process_image_service
