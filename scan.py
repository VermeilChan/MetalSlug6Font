import os

def generate_tree(root_dir, indent=''):
    tree = ""
    items = os.listdir(root_dir)
    
    for idx, item in enumerate(items):
        path = os.path.join(root_dir, item)
        is_last_item = idx == len(items) - 1

        tree += f"{indent}{'└─' if is_last_item else '├─'} {item}\n"

        if os.path.isdir(path):
            sub_indent = indent + ('    ' if is_last_item else '│   ')
            tree += generate_tree(path, sub_indent)
    
    return tree

def generate_directory_tree(root_dir, output_file):
    tree = generate_tree(root_dir)
    with open(output_file, 'w', encoding='utf-8') as file:  # Specify UTF-8 encoding
        file.write(tree)

if __name__ == "__main__":
    target_directory = "."  # Change this to the desired directory path
    output_filename = "directory_tree.txt"

    generate_directory_tree(target_directory, output_filename)
    print(f"Directory tree saved to {output_filename}")
