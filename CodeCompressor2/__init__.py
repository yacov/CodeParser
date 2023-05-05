import ast
import os
import sys
import tokenize
import json
import zlib


def extract_info(directory_path):
    all_info = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_path.endswith('.py') or file_path.endswith('.cs') or file_path.endswith('.js'):
                with open(file_path, 'r') as file:
                    source_code = file.read()

                if file_path.endswith('.py'):
                    tree = ast.parse(source_code)
                    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]
                    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]
                    variables = [node.id for node in tree.body if isinstance(node, ast.Assign)]
                    token_count = len(list(tokenize.generate_tokens(file.readline)))
                    info = {'file_path': file_path, 'classes': classes, 'functions': functions, 'variables': variables,
                            'token_count': token_count}

                elif file_path.endswith('.cs'):
                    # Use the Microsoft.CodeAnalysis.CSharp library to extract information from C# files
                    # Code for extracting information from C# files goes here
                    pass

                elif file_path.endswith('.js'):
                    # Use the esprima library to extract information from JavaScript files
                    # Code for extracting information from JavaScript files goes here
                    pass

                # Compress the extracted information using JSON and zlib
                compressed_info = zlib.compress(json.dumps(info).encode())
                all_info.append(compressed_info)

    # Write the compressed information to a single file
    output_file_path = 'output.jsonz'
    with open(output_file_path, 'wb') as output_file:
        output_file.write(json.dumps(all_info).encode())


if __name__ == '__main__':
    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print('Directory not found')
        sys.exit(1)

    extract_info(directory_path)
