import re
import os

def read_strings_from_file(file_path):
    """
    Reads a text file and extracts strings that:
    - Start at the beginning of a new line
    - End with a comma
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    matches = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Strip trailing spaces/newlines
                line = line.strip()
                # Match strings starting at line start and ending with a comma
                #if re.fullmatch(r'^.+,$', line):
                if re.fullmatch(r'^(.+),$', line):
                    matches.append(re.match(r'^(.+),$', line).group(1))
                #    matches.append(line)
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return matches


# Example usage
if __name__ == "__main__":
    file_path = "puzzle9/puzzle.txt"  # Replace with your file path

    try:
        results = read_strings_from_file(file_path)
        if results:
            print("Matched strings:")
            for item in results:
                print(item)
        else:
            print("No matching strings found.")
    except FileNotFoundError as fnf:
        print(fnf)


