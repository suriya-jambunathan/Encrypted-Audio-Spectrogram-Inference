from torchvision import transforms
from PIL import Image
import os
from tqdm import tqdm

def preprocess_and_save_dataset(input_dataset_path, output_dataset_path, transform):
    if not os.path.exists(output_dataset_path):
        os.makedirs(output_dataset_path)

    classes = os.listdir(input_dataset_path)
    for cls in tqdm(classes, desc="Processing classes", mininterval=1.0):
        class_dir = os.path.join(input_dataset_path, cls)
        if not os.path.isdir(class_dir):
            continue

        output_class_dir = os.path.join(output_dataset_path, cls)
        if not os.path.exists(output_class_dir):
            os.makedirs(output_class_dir)

        img_names = os.listdir(class_dir)
        if len(img_names) > 100:
            img_names = tqdm(img_names, desc=f"Processing images in class {cls}", leave=False, mininterval=30.0)
        
        for img_name in img_names:
            if img_name.startswith('.'):  # Skip hidden files and directories
                continue

            img_path = os.path.join(class_dir, img_name)
            try:
                img = Image.open(img_path)
                img = img.convert('L')
                img = transform(img)
                output_img_path = os.path.join(output_class_dir, img_name)
                img.save(output_img_path)
            except IOError:
                print(f"Skipping file (not an image): {img_path}")

transform = transforms.Compose([
    transforms.Resize((28, 28)),
])

input_dataset_path = "dataset"
output_dataset_path = "preprocessed_dataset"

preprocess_and_save_dataset(input_dataset_path, output_dataset_path, transform)