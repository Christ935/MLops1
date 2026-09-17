from pathlib import Path
from PIL import Image
import shutil

CATEGORIES = {
    "0": "Bread",
    "1": "Dairy product",
    "2": "Dessert",
    "3": "Egg",
    "4": "Fried food",
    "5": "Meat",
    "6": "Noodles-Pasta",
    "7": "Rice",
    "8": "Seafood",
    "9": "Soup",
    "10": "Vegetable-Fruit",
}

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "food11_raw"
PROCESSED = ROOT / "data" / "food11_processed"
MINI = ROOT / "data" / "food11_processed_mini"

SPLITS = ["training", "evaluation", "validation"]


def prepare_dataset():
    # Remove old processed folders if they already exist
    if PROCESSED.exists():
        shutil.rmtree(PROCESSED)

    if MINI.exists():
        shutil.rmtree(MINI)

    for split in SPLITS:
        source_folder = RAW / split

        mini_counts = {category: 0 for category in CATEGORIES.values()}

        for image_path in source_folder.iterdir():

            if not image_path.is_file():
                continue

            # Category number is the first part of the filename
            category_number = image_path.stem.split("_")[0]

            if category_number not in CATEGORIES:
                continue

            category_name = CATEGORIES[category_number]

            processed_folder = PROCESSED / split / category_name
            mini_folder = MINI / split / category_name

            processed_folder.mkdir(parents=True, exist_ok=True)
            mini_folder.mkdir(parents=True, exist_ok=True)

            try:
                with Image.open(image_path) as image:
                    image = image.convert("RGB")
                    image = image.resize((128, 128))

                    # Save full processed dataset
                    image.save(processed_folder / image_path.name)

                    # Save maximum 100 images per category in mini dataset
                    if mini_counts[category_name] < 100:
                        image.save(mini_folder / image_path.name)
                        mini_counts[category_name] += 1

            except Exception as error:
                print(f"Error processing {image_path}: {error}")

    print("Food-11 processing complete.")


if __name__ == "__main__":
    prepare_dataset()