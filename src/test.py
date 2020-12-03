import glob
from os import path

if __name__ == "__main__":
    folder_list = glob.glob('./data/*')
    for folder in folder_list:
        if path.isdir(folder):
            print('{} is folder'.format(folder))