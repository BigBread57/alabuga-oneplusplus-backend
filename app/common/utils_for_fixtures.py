import json
from datetime import UTC, datetime


def add_timestamps_to_fixture_file(input_file, output_file=None):
    """
    Читает фикстуру из файла, добавляет временные метки и сохраняет результат
    """
    if output_file is None:
        output_file = input_file

    # Читаем исходную фикстуру
    with open(input_file, encoding="utf-8") as f:
        fixture_data = json.load(f)

    current_time = datetime.now(UTC).isoformat()

    for item in fixture_data:
        fields = item.get("fields", {})

        # Добавляем временные метки, если их нет
        if "created_at" not in fields:
            fields["created_at"] = current_time
        if "updated_at" not in fields:
            fields["updated_at"] = current_time

        item["fields"] = fields

    # Сохраняем обновленную фикстуру
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixture_data, f, ensure_ascii=False, indent=2, default=str)

    print(f"Фикстура успешно обновлена и сохранена в {output_file}")


# Использование
if __name__ == "__main__":
    add_timestamps_to_fixture_file("fixtures.json", "new_fixtures.json")
