import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

# Define the base directory where the folders are located
base_dir = '/mnt/data/final_dataset'  # Replace with the path to your base directory

# Create directories for positive and negative spectrogram images if they do not exist
positive_images_dir = os.path.join(base_dir, 'positive_images')
negative_images_dir = os.path.join(base_dir, 'negative_images')

os.makedirs(positive_images_dir, exist_ok=True)
os.makedirs(negative_images_dir, exist_ok=True)

# Function to process an audio file and save its Mel spectrogram
def process_and_save_audio(audio_path, save_dir, dpi=100):
    try:
        y, sr = librosa.load(audio_path)
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        log_S = librosa.power_to_db(S, ref=np.max)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        mel_spectrogram_path = os.path.join(save_dir, os.path.basename(audio_path).replace('.wav', '_mel_spectrogram.png'))
        
        plt.savefig(mel_spectrogram_path, bbox_inches='tight', pad_inches=0, dpi=dpi)
        plt.close()
    except Exception as e:
        print(f"Could not process file {audio_path}: {e}")

# Loop through the folders and process each audio file
for folder in os.listdir(base_dir):
    if folder in ['ACFESD', 'AESDD', 'ASVPESD', 'CREMAD', 'EESC', 'EMOVO', 'JLC', 'MESD', 'RAVDESS', 'SYNCAT', 'TESS', 'URDU']:
        folder_path = os.path.join(base_dir, folder)
        
        # Process each audio file in the folder using a single progress bar
        for sentiment in ['negative', 'positive']:
            sentiment_folder_path = os.path.join(folder_path, sentiment)
            if os.path.exists(sentiment_folder_path):
                audio_files = [f for f in os.listdir(sentiment_folder_path) if f.endswith('.wav')]
                for filename in tqdm(audio_files, desc=f'Processing {folder} - {sentiment}'):
                    audio_path = os.path.join(sentiment_folder_path, filename)
                    save_dir = positive_images_dir if sentiment == 'positive' else negative_images_dir
                    mel_spectrogram_path = os.path.join(save_dir, os.path.basename(audio_path).replace('.wav', '_mel_spectrogram.png'))

                    # Skip the file if the spectrogram image already exists
                    if not os.path.isfile(mel_spectrogram_path):
                        try:
                            process_and_save_audio(audio_path, save_dir)
                        except Exception as e:
                            print(f"Could not process file {audio_path}: {e}")
                    else:
                        print(f"Skipped {audio_path}, already processed.")