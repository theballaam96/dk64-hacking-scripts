import os

versions = ["us","pal","jp","lodgenet"]

old_version = None
new_version = None

def list_files_exclude_objzips(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        # Skip the 'objzips' subdirectory
        if 'objzips' in dirs:
            dirs.remove('objzips')
        # Add all files in the current directory
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

with open("diff.txt", "w") as fk:
    for v_i in range(len(versions) - 1):
        old_v = versions[v_i]
        new_v = versions[v_i + 1]
        
        old_files = list_files_exclude_objzips(f"../bin/collision/{old_v}/")
        new_files = list_files_exclude_objzips(f"../bin/collision/{new_v}/")
        for index in range(len(old_files)):
            old_file = None
            new_file = None
            with open(old_files[index], "r") as fh:
                old_file = fh.read()
            with open(new_files[index], "r") as fh:
                new_file = fh.read()
            if "Geometry.obj" in old_files[index] or "Event Triggers.obj" in old_files[index]:
                if old_v == "jp" or new_v == "jp":
                    old_file = "\n".join([" ".join(x.split(" ")[:4]) if x.split(" ")[0] == "v" else x for x in old_file.split("\n")])
                    new_file = "\n".join([" ".join(x.split(" ")[:4]) if x.split(" ")[0] == "v" else x for x in new_file.split("\n")])
            if old_file != new_file:
                fk.write(f"Difference between {old_v} and {new_v} in {old_files[index]}\n")