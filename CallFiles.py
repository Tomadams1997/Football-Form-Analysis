import os
def process_folder(folder_path,function):
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]
    [function(x) for x in file_paths]

