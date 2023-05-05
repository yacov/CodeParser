import os
import json
import ast
import esprima
import clr

import nltk


class Item:
    def __init__(self, item_type, name, content):
        self.item_type = item_type
        self.name = name
        self.content = content

    def to_dict(self):
        return {
            'type': self.item_type,
            'name': self.name,
            'content': self.content
        }


def extract_classes_csharp(file_content):
    class_pattern = r'(?:public|private|protected)?\s*class\s+(\w+)\s*(?::\s*\w+\s*)?{([\s\S]*?)}'
    class_matches = re.findall(class_pattern, file_content)

    class_items = []
    for cls in class_matches:
        class_name, class_content = cls
        class_item = Item('class', class_name, class_content)
        class_items.append(class_item)

    return class_items


def extract_classes_javascript(file_content):
    tree = esprima.parseScript(file_content, {'loc': True})
    class_items = []

    for node in esprima.walk(tree):
        if node.type == 'ClassDeclaration':
            class_item = Item('class', node.id.name, file_content[node.start:node.end])
            class_items.append(class_item)

    return class_items


def extract_classes_python(file_content):
    tree = ast.parse(file_content)
    class_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    class_items = []

    for cls in class_nodes:
        start_lineno, end_lineno = cls.lineno, cls.end_lineno
        class_content = "\n".join(file_content.splitlines()[start_lineno - 1:end_lineno])
        class_item = Item('class', cls.name, class_content)
        class_items.append(class_item)

    return class_items


def compress_project(project_path, project_type):
    extractors = {
        'csharp': extract_classes_csharp,
        'javascript': extract_classes_javascript,
        'python': extract_classes_python
    }

    if project_type not in extractors:
        raise ValueError(f"Unsupported project type: {project_type}")

    file_extensions = {
        'csharp': '.cs',
        'javascript': '.js',
        'python': '.py'
    }

    result = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(file_extensions[project_type]):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    classes = extractors[project_type](content)
                    class_dicts = [cls.to_dict() for cls in classes]

                    result.append({
                        'path': file_path.replace(project_path, ''),
                        'classes': class_dicts
                    })
    return result


def compress_project(project_path, project_type):
    extractors = {
        'csharp': extract_classes_csharp,
        'javascript': extract_classes_javascript,
        'python': extract_classes_python
    }

    if project_type not in extractors:
        raise ValueError(f"Unsupported project type: {project_type}")

    file_extensions = {
        'csharp': '.cs',
        'javascript': '.js',
        'python': '.py'
    }

    result = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(file_extensions[project_type]):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    classes = extractors[project_type](content)
                    class_dicts = [cls.to_dict() for cls in classes]

                    result.append({
                        'path': file_path.replace(project_path, ''),
                        'classes': class_dicts
                    })
    return result


def encode_project(project_data):
    formatted_project = json.dumps(project_data, ensure_ascii=False)
    return formatted_project


# def count_tokens(text):
#     tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+|\$[\d\.]+|\S+')
#     tokens = tokenizer.tokenize(text)
#     token_count = len(tokens)
#     return token_count


def main():
    project_path = 'C:\development\KnowYourCustomer\kyc_autotests'
    project_type = 'csharp'  # Replace with 'javascript' or 'python' as needed
    compressed_project = compress_project(project_path, project_type)
    encoded_project = encode_project(compressed_project)

   # token_count = count_tokens(encoded_project)
    #print(f'Token count: {token_count}')
    with open('encoded_project.txt', 'w', encoding='utf-8') as f:f.write(encoded_project)

if __name__ == '__main__':
    main()
