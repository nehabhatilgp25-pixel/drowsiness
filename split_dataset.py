import os
import shutil
import random

# ------------ SET THESE ------------
SOURCE_OPEN = "Open_Eyes"
SOURCE_CLOSED = "Closed_Eyes"
DEST = "data"   # final dataset folder
# ----------------------------------

# Create folders
for split in ["train", "val", "test"]:
    for cls in ["open", "closed"]:
        os.makedirs(os.path.join(DEST, split, cls), exist_ok=True)

def split_and_copy(src_folder, dest_class_name):
    images = os.listdir(src_folder)
    random.shuffle(images)

    n = len(images)
    train_end = int(0.7 * n)
    val_end = int(0.9 * n)

    train_files = images[:train_end]
    val_files = images[train_end:val_end]
    test_files = images[val_end:]

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