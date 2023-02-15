import requests
import os
import shutil
import zipfile
import tarfile
import glob
import splitfolders

FILE_NAME = 'images.zip'


def download_data():
    print("Downloading files...")
    url = 'https://data.caltech.edu/records/mzrjq-6wc02/files/caltech-101.zip?download=1'
    r = requests.get(url)
    with open(FILE_NAME, 'wb') as f:
        f.write(r.content)
    print("Done!")


def extract_images():
    print("Extracting files...")
    
    with zipfile.ZipFile(FILE_NAME, 'r') as file_1:
        file_1.extract('caltech-101/101_ObjectCategories.tar.gz', '.')
        file_1.close()
        
    # Move the file caltech-101/101_ObjectCategories.tar.gz to the current directory
    shutil.move('caltech-101/101_ObjectCategories.tar.gz', '.')
    
    # Delete the folder caltech-101
    shutil.rmtree('caltech-101')
      
    # Extract the images from 101_ObjectCategories.tar.gz
    with tarfile.open('101_ObjectCategories.tar.gz', 'r') as file_2:
        file_2.extractall()
        file_2.close()
   
    # Delete unnecessary files
    os.remove(FILE_NAME)
    os.remove('101_ObjectCategories.tar.gz')
    
    # Rename the folder 101_ObjectCategories to images
    os.rename('101_ObjectCategories', 'downloaded_images')
   
    print("Done!")


def split_folders():
    print("Dividing the images into train, validation and test sets...")
    # Split the images into train, validation and test sets
    # The ratio is 70% for training, 10% for validation and 20% for testing
    splitfolders.ratio("downloaded_images", output="images",
        seed=1337, ratio=(.7, .1, .2), move=True)
    # Delete the folder downloaded_images
    shutil.rmtree('downloaded_images')
    print("Done!")

if __name__ == "__main__":

    if not os.path.exists(FILE_NAME) and not os.path.exists("images"):
        download_data()
    else:
        print(FILE_NAME, "already exists")
        
    if not os.path.exists("images"):
       extract_images()
    else:
        print("images folder already exists")
        
    if not os.path.exists("images"):
        split_folders()
    else:
        print("images folder already exists")
        
        
    print('--------------')        
    print('There are {} images in the dataset'.format(len(glob.glob('images/*/*/*.jpg'))))
    print(' - There are {} images for training'.format(len(glob.glob('images/train/*/*.jpg'))))
    print(' - There are {} images for validation'.format(len(glob.glob('images/val/*/*.jpg'))))
    print(' - There are {} images for testing'.format(len(glob.glob('images/test/*/*.jpg'))))
    
    print('Data preprocessing done!')
    