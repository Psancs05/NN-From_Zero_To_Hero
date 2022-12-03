import requests
import os
import tarfile
import glob
import numpy as np
import pandas as pd


def download_data():
    print("Downloading images.tar.gz...")
    url = 'https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz'
    r = requests.get(url)
    with open("images.tar.gz", 'wb') as f:
        f.write(r.content)
    print("Done!")


def extract_images():
    print("Extracting images.tar.gz...")
    file = tarfile.open('images.tar.gz')
    file.extractall()
    file.close()
    print("Done!")
    
    print('--------------')    
    print("Deleting images.tar.gz...")
    os.remove('images.tar.gz')
    print("Done!")
    
def divide_data():
    CATS = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British_Shorthair', 'Egyptian_Mau', 'Maine_Coon', 'Persian', 'Ragdoll', 'Russian_Blue', 'Siamese', 'Sphynx']
    cats_images = []
    dogs_images = []
    
    for img in glob.glob('images/*.jpg'):
        if any(cat in img for cat in CATS):
            cats_images.append(img)
        else:
            dogs_images.append(img)
            
    return cats_images, dogs_images


def split_data():
    #split the data into train, validation and test sets
    train_d, val_d, test_d = np.split(dogs, [int(len(dogs)*0.7), int(len(dogs)*0.8)])
    train_c, val_c, test_c = np.split(cats, [int(len(cats)*0.7), int(len(cats)*0.8)])
    
    train_dog_df = pd.DataFrame({'image':train_d, 'label':'dog'})
    val_dog_df = pd.DataFrame({'image':val_d, 'label':'dog'})
    test_dog_df = pd.DataFrame({'image':test_d, 'label':'dog'})

    train_cat_df = pd.DataFrame({'image':train_c, 'label':'cat'})
    val_cat_df = pd.DataFrame({'image':val_c, 'label':'cat'})
    test_cat_df = pd.DataFrame({'image':test_c, 'label':'cat'})
    
    train_df = pd.concat([train_dog_df, train_cat_df])
    val_df = pd.concat([val_dog_df, val_cat_df])
    test_df = pd.concat([test_dog_df, test_cat_df])
    
    return train_df, val_df, test_df




if __name__ == "__main__":

    if not os.path.exists("images.tar.gz"):
        #TODO: Download the images.tar.gz file from the following link
        download_data()
    else:
        print("images.tar.gz already exists")
        
    if not os.path.exists("images"):
       extract_images()
    else:
        print("images folder already exists")
        
        
    print('--------------')        
    print('There are {} images in the dataset'.format(len(glob.glob('images/*.jpg'))))

    cats, dogs = divide_data()
    
    print('There are {} images of cats'.format(len(cats)))
    print('There are {} images of dogs'.format(len(dogs)))
    
    #shuffle the lists
    np.random.shuffle(cats)
    np.random.shuffle(dogs)
    
    #split the data into train, validation and test sets
    train_df, val_df, test_df = split_data()
    
    print('--------------')
    print('There are {} images for training'.format(len(train_df)))
    print('There are {} images for validation'.format(len(val_df)))
    print('There are {} images for testing'.format(len(test_df)))
    
    #save the dataframes to csv files
    print('--------------')
    print('Saving the dataframes to csv files...')
    train_df.to_csv('train.csv', index=False)
    val_df.to_csv('val.csv', index=False)
    test_df.to_csv('test.csv', index=False)
    print('Data preprocessing done!')
    