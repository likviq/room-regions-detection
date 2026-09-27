class LabelRoomsService:
    def __init__(
        self,
        label_connected_regions_command,
        save_room_segments_command
    ):
        self.label_connected_regions_command = label_connected_regions_command
        self.save_room_segments_command = save_room_segments_command

    async def label_rooms(
        self,
        color_img,
        segmentation,
        minimum_room_area,
        overlay_alpha
    ):
        labeled_image, rooms = await self.label_connected_regions_command.execute(
            color_img,
            segmentation.first_region,
            segmentation.second_region,
            minimum_room_area,
            overlay_alpha
        )

        rooms_json = await self.save_room_segments_command.to_json_string(rooms)

        return labeled_image, rooms, rooms_json
