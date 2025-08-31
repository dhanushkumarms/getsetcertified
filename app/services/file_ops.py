import os, shutil

def ensure_dirs(*dirs):
    for d in dirs:
        os.makedirs(d, exist_ok=True)

def empty_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        return
    for item in os.listdir(path):
        p = os.path.join(path, item)
        if os.path.isfile(p):
            os.remove(p)
        else:
            shutil.rmtree(p)
