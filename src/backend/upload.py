import os
def save_uploaded_files(files, save_dir="uploads"):
   os.makedirs(save_dir, exist_ok=True)
   filepaths = []
   for file in files:
       filepath = os.path.join(save_dir, file.name)
       with open(filepath, "wb") as f:
           f.write(file.read())
       filepaths.append(filepath)
   return filepaths