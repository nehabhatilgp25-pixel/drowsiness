import os #to interact with OS
import shutil #file operations
import random

# ------------ SET THESE ------------
SOURCE_OPEN = "Open_Eyes" #the file where the open eyes were stored
SOURCE_CLOSED = "Closed_Eyes" #file where closed eyes were stored
DEST = "data"   # final dataset folder
# ----------------------------------

# Create folders
for split in ["train", "val", "test"]: #just a loop
    for cls in ["open", "closed"]: #another loop
        os.makedirs(os.path.join(DEST, split, cls), exist_ok=True) #making the individual files of test, val, data with open and close below them.
        #exist_ok=True suppresses an error if the directory already exists

def split_and_copy(src_folder, dest_class_name):
    images = os.listdir(src_folder) #
    random.shuffle(images) #mixing up the images

    n = len(images) #number of images
    train_end = int(0.7 * n) 
    val_end = int(0.9 * n)

    train_files = images[:train_end] #0 to 70%
    val_files = images[train_end:val_end] #70% to 90%
    test_files = images[val_end:] # 90% to 100%

    # copy to train
    for f in train_files:
        shutil.copy(os.path.join(src_folder, f),
                    os.path.join(DEST, "train", dest_class_name, f))

    # copy to val
    for f in val_files:
        shutil.copy(os.path.join(src_folder, f),
                    os.path.join(DEST, "val", dest_class_name, f))

    # copy to test
    for f in test_files:
        shutil.copy(os.path.join(src_folder, f),
                    os.path.join(DEST, "test", dest_class_name, f))

    print(f"Done splitting {src_folder}: {n} images")

# Run splitting
split_and_copy(SOURCE_OPEN, "open")
split_and_copy(SOURCE_CLOSED, "closed")

print("Dataset split complete!")