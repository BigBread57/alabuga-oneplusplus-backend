import os

import django

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alabuga.settings")
django.setup()

from django.apps import apps


def get_models_info():
    """Получает информацию о моделях в требуемом формате"""
    models_data = []

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_info = {
                "name_model": model.__name__,
                "description": model.__doc__ or "Нет документации",
                "fields": [],
            }

            for field in model._meta.get_fields():
                field_info = {"name_field": field.name, "description": getattr(field, "help_text", "") or ""}
                model_info["fields"].append(field_info)

            models_data.append(model_info)

    return models_data


def print_models_info():
    """Выводит информацию о моделях в требуемом формате"""
    models_data = get_models_info()

    for model_info in models_data:
        print(f"\nname_model: {model_info['name_model']}")
        print(f"description: {model_info['description']}")
        print("fields:")

        for field in model_info["fields"]:
            print(f"  - name_field: {field['name_field']}")
            print(f"    description: {field['description']}")


def export_models_info_to_dict():
    """Возвращает данные в виде словаря"""
    return get_models_info()


if __name__ == "__main__":
    print_models_info()
