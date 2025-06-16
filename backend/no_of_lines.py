import os

def count_lines_in_py_files(directory):
    total_lines = 0
    py_files = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        line_count = len(lines)
                        total_lines += line_count
                        py_files.append((file_path, line_count))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return total_lines, py_files

if __name__ == "__main__":
    src_dir = 'src'
    if not os.path.exists(src_dir):
        print(f"Directory '{src_dir}' does not exist.")
    else:
        total_lines, py_files = count_lines_in_py_files(src_dir)
        print(f"Found {len(py_files)} Python files in {src_dir}")
        print("\nFile details:")
        for file_path, line_count in py_files:
            print(f"{file_path}: {line_count} lines")
        print(f"\nTotal lines of Python code: {total_lines}")