import tarfile
import os

# unzip the all ".tar.gz" files in my local folder
tarfiles_from = "/Users/sihanliu/Desktop/compressed_full_dataset/quotes"
# The output are stored in the directory where this Python file is located
# Then I move them to Data Folder
for path, directories, files in os.walk(tarfiles_from):
    for f in files:
        if f.endswith(".tar.gz"):
            tar = tarfile.open(os.path.join(path,f), 'r:gz')
            tar.extractall()
            tar.close()
