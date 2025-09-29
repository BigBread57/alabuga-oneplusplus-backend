import json
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alabuga.settings")
django.setup()

from django.apps import apps


def get_models_info():
    """Получает информацию о моделях в требуемом формате"""
    models_data = []

    for app_config in apps.get_app_configs():
        print(app_config)
        for model in app_config.get_models():
            if model.__name__ in {
                "Rank",
                "Competency",
                "RequiredRankCompetency",
                "ActivityCategory",
                "Artifact",
                "Event",
                "EventArtifact",
                "EventCompetency",
                "GameWorldStory",
                "Mission",
                "MissionArtifact",
                "MissionCompetency",
                "MissionBranch",
                "MissionLevel",
            }:
                model_info = {
                    "name_model": model.__name__,
                    "description": model.__doc__ or "Нет документации",
                    "fields": [],
                }

                for field in model._meta.get_fields():
                    if getattr(field, "help_text", ""):
                        field_info = {
                            "name_field": field.name,
                            "description": str(getattr(field, "help_text", "")) or "",
                        }
                        model_info["fields"].append(field_info)

                models_data.append(model_info)

    return models_data


def save_models_info_to_file(filename="models_info.txt", format_type="text"):
    """
    Сохраняет информацию о моделях в файл

    Args:
        filename (str): имя файла для сохранения
        format_type (str): формат сохранения ("text", "json")
    """
    models_data = get_models_info()

    if format_type == "json":
        # Сохранение в JSON формате
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(models_data, f, ensure_ascii=False, indent=2)
        print(f"Информация о моделях сохранена в файл {filename} (JSON формат)")

    else:
        # Сохранение в текстовом формате
        with open(filename, "w", encoding="utf-8") as f:
            for model_info in models_data:
                f.write(f"\nname_model: {model_info['name_model']}\n")
                f.write(f"description: {model_info['description']}\n")
                f.write("fields:\n")

                for field in model_info["fields"]:
                    f.write(f"  - name_field: {field['name_field']}\n")
                    f.write(f"    description: {field['description']}\n")

        print(f"Информация о моделях сохранена в файл {filename} (текстовый формат)")


def export_models_info_to_dict():
    """Возвращает данные в виде словаря"""
    return get_models_info()


if __name__ == "__main__":
    # Сохранение в текстовый файл
    save_models_info_to_file("models_info.txt", "text")

    # Сохранение в JSON файл (опционально)
    save_models_info_to_file("models_info.json", "json")
