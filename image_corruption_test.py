import PIL
from PIL import Image
import os

folder_paths = ['pics','uploads']

for folder_path in folder_paths:
  for filename in os.listdir(folder_path):
      try:
          image = Image.open(os.path.join(folder_path, filename))
      except PIL.UnidentifiedImageError as e:
          print(f"Error in file {filename}: {e}")
          #os.remove(os.path.join(folder_path, filename))
          #print(f"Removed file {filename}")
