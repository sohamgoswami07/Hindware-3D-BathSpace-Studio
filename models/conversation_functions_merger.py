
import os
import argparse
import copy
from os.path import exists

def merge_files(parent_file_path, import_list):
    final_str = ""
    for imp in import_list:
        with open(imp) as file:
            for line in file:
                if not "dave_imports" in line:
                    final_str += line

    with open(parent_file_path) as file:
        for line in file:
            if not "dave_imports" in line:
                final_str += line
    
    
    return final_str        
                


def find_file_path(path,file_name):
    count = 0
    while count < 4:
        file_exists = exists(path+os.sep+file_name)
        if file_exists:
            return path+os.sep+file_name
        path = os.path.dirname(path)
        count+=1
    return None


def get_imports(conv1):
    import_list = []
    path_head, path_tail = os.path.split(conv1)
    original_functions = ""
    with open(conv1) as file:
        for line in file:
            if "dave_imports" in line:
                original_functions +="\n"+line.rstrip()
                current_import_list = line.rstrip()[13:].replace(" ","").split(",")
                current_import_list = ["{}/conversation_functions.py".format(dir_name) for dir_name in current_import_list]
                for i in current_import_list:
                    found_file_path = find_file_path(path_head, i)
                    if found_file_path:
                        import_list.append(found_file_path)
                        if i == path_tail:
                            exit()
                        sub_list = get_imports(found_file_path)
                        if len(sub_list):
                            import_list.append(sub_list)

    import_list = set(import_list)
    import_list = list(import_list)
    return import_list




def main():
    parser = argparse.ArgumentParser(description="Merge conversation JSONs")
    parser.add_argument("-f", "--file_path", help="Path to conversation function")
    args = (parser.parse_args())

    if args.file_path:
        conv1 = args.file_path
    else:
        print("file_path needed")

    path_head, path_tail = os.path.split(conv1)
    import_list = get_imports(conv1)
    file_merged_output = merge_files(conv1, import_list)
    with open("{}/conversation_functions_merged.py".format(path_head), "w") as text_file:
        text_file.write(file_merged_output)
    print(file_merged_output)
    
if __name__ == '__main__':
    main()

