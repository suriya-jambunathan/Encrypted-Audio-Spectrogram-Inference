import os
import glob
import shutil
from tqdm import tqdm

datasets = []
all_images = glob.glob('./preprocessed_dataset/*/*')
for i in range(len(all_images)):
    dataset = all_images[i].split('/')[-1].split('__')[0]
    if dataset not in datasets:
        datasets.append(dataset)
        
for dataset in datasets:
    try:
        os.mkdir(f'./coarse_classes_dataset/{dataset}/')
    except:
        pass
    try:
        os.mkdir(f'./fine_classes_dataset/{dataset}/')
    except:
        pass
    dataset_images = glob.glob(f'./preprocessed_dataset/*/{dataset}*')
    coarse_classes = []
    fine_classes = []
    for i in tqdm(range(len(dataset_images))):
        temp = dataset_images[i].split('/')[-1].split('__')
        coarse_class = temp[1]
        fine_class = temp[2]
        if coarse_class not in coarse_classes:
            try:
                os.mkdir(f'./coarse_classes_dataset/{dataset}/{coarse_class}/')
            except:
                pass
            coarse_classes.append(coarse_class)
        if fine_class not in fine_classes:
            try:
                os.mkdir(f'./fine_classes_dataset/{dataset}/{fine_class}/')
            except:
                pass
            fine_classes.append(fine_class)
        
        source_file_name = dataset_images[i]
        destination_file_name = f"./coarse_classes_dataset/{dataset}/{coarse_class}/{source_file_name.split('/')[-1]}"
        shutil.copy(source_file_name, destination_file_name)
        
        source_file_name = dataset_images[i]
        destination_file_name = f"./fine_classes_dataset/{dataset}/{fine_class}/{source_file_name.split('/')[-1]}"
        shutil.copy(source_file_name, destination_file_name)