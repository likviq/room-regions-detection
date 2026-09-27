import json


class SaveRoomSegmentsCommand:
    def __init__(self, json_storage_provider):
        self.json_storage_provider = json_storage_provider

    async def execute(self, rooms, output_path):
        data = await self._create_data(rooms)
        await self.json_storage_provider.save(data, output_path)

    async def to_json_string(self, rooms):
        data = await self._create_data(rooms)
        return json.dumps(data, indent=2, ensure_ascii=False)

    async def _create_data(self, rooms):
        room_data = []

        for room in rooms:
            segments = []

            for segment in room.segments:
                segment_data = {
                    "start": list(segment.start_point),
                    "end": list(segment.end_point)
                }

                segments.append(segment_data)

            data = {
                "id": room.room_identifier,
                "area": room.area,
                "centroid": room.centroid,
                "segments": segments
            }

            room_data.append(data)

        return {"rooms": room_data}
