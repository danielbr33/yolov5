import json
import os
import shutil


def replace_filename_and_rename_images(anno_json, images_dir):
    """
    Odczytuje plik JSON z anotacjami COCO, podmienia nazwy plików obrazów na ich ID,
    zmienia nazwy plików na dysku, i aktualizuje anotacje.

    Parameters:
    - anno_json (str): Ścieżka do pliku JSON z anotacjami COCO.
    - images_dir (str): Ścieżka do folderu, gdzie znajdują się oryginalne obrazy.

    Returns:
    - None
    """
    # Odczytanie pliku JSON z anotacjami
    with open(anno_json, 'r') as f:
        coco_data = json.load(f)

    # Przechodzimy przez każdy obraz w pliku JSON
    for image in coco_data['images']:
        image_id = image['id']
        old_filename = image['file_name']
        directory, old_filename = os.path.split(old_filename)
        old_filepath = os.path.join("images/train", old_filename)

        # Sprawdzenie, czy plik obrazu istnieje
        if not os.path.exists(old_filepath):
            print(f"Plik {old_filename} nie został znaleziony. Pomijam.")
            continue

        # Nowa nazwa pliku - używamy ID obrazu, zachowując rozszerzenie pliku
        new_filename = f"{image_id}{os.path.splitext(old_filename)[1]}"
        new_filepath = os.path.join(images_dir, new_filename)

        # Zmiana nazwy pliku obrazu na dysku
        try:
            shutil.move(old_filepath, new_filepath)
            print(f"Zmieniono nazwę pliku: {old_filename} -> {new_filename}")
        except Exception as e:
            print(f"Błąd przy zmianie nazwy pliku {old_filename}: {e}")
            continue

        # Zaktualizowanie nazwy pliku w anotacjach
        image['file_name'] = new_filename

    # Zapisanie zmodyfikowanego pliku JSON z zaktualizowanymi nazwami plików
    with open(anno_json, 'w') as f:
        json.dump(coco_data, f, indent=4)

    print("Anotacje zostały zaktualizowane i zapisane.")


# Przykład użycia:
anno_json = "COCO_train.json"  # Ścieżka do pliku z anotacjami COCO
images_dir = "images/train"  # Ścieżka do folderu z obrazami
replace_filename_and_rename_images(anno_json, images_dir)
