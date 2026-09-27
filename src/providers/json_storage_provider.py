import json


class JsonStorageProvider:
    async def save(self, data, output_path):
        serialized_data = json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        )

        await self._write_file(output_path, serialized_data)

    async def _write_file(self, output_path, content):
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(content)
