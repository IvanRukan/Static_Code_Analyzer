import argparse
import os
import re
import ast


def s001(index, line, path):
    if len(line) > 79:
        return f'{path}: Line {index + 1}: S001 Too long'


def s002(index, line, path):
    count = 0
    line_copy = line.replace(' ', '')
    if len(line_copy) == 0:
        return None
    for each in line:
        if each == ' ':
            count += 1
        else:
            break
    if count % 4 != 0 and count != 0:
        return f'{path}: Line {index + 1}: S002 Indentation is not a multiple of four'


def s003(index, line, path):
    if '#' not in line:
        line = line.split()
        for each in line:
            if each.endswith(';'):
                return f'{path}: Line {index + 1}: S003 Unnecessary semicolon'
    elif '#' in line:
        hash = line.find('#')
        semi = line.find(';')
        if semi < hash and semi != -1:
            return f'{path}: Line {index + 1}: S003 Unnecessary semicolon'


def s004(index, line, path):
    count = 0
    for each in line:
        if each == ' ':
            count += 1
        elif each == '#':
            hash = line.find('#')
            if count < 2 and hash != 0:
                return f'{path}: Line {index + 1}: S004 At least two spaces required before inline comments'
            break
        else:
            count = 0


def s005(index, line, path):
    needed = line.find('#')
    line = line[needed::].split()
    for each in line:
        if each.lower().strip('#') == 'todo':
            return f'{path}: Line {index + 1}: S005 TODO found'


def s006(index, path):
    global empty_lines
    empty_lines = 0
    return f'{path}: Line {index + 1}: S006 More than two blank lines used before this line'


def s007(index, line, path):
    if "class" in line:
        constructor = 'class'
        spaces_counter = 0
        pos = line.index(constructor) + 5
        for i in range(pos, len(line)):
            if line[i] == ' ':
                spaces_counter += 1
            else:
                break
        if spaces_counter > 1:
            return f"{path}: Line {index + 1}: S007 Too many spaces after '{constructor}'"
    elif "def" in line:
        constructor = 'def'
        spaces_counter = 0
        pos = line.index(constructor) + 3
        for i in range(pos, len(line)):
            if line[i] == ' ':
                spaces_counter += 1
            else:
                break
        if spaces_counter > 1:
            return f"{path}: Line {index + 1}: S007 Too many spaces after '{constructor}'"


def s008(index, line, path):
    template = '[A-Z][a-z]*'
    if "class" in line:
        line_copy = line.split()
        name = line_copy.index("class")
        name += 1
        name = line_copy[name].strip()
        name = name.rstrip(':')
        if re.match(template, name):
            pass
        else:
            return f"{path}: Line {index + 1}: S008 Class name '{name}' should use CamelCase"


def s009(index, line, path):
    template = '_*[-a-z]+_*'
    if "def" in line:
        line_copy = line.split()
        name = line_copy.index("def")
        name += 1
        name = line_copy[name].strip()
        name = name.rstrip('():')
        if re.match(template, name):
            pass
        else:
            return f"{path}: Line {index + 1}: S009 Function name '{name}' should use snake_case"


def s010(index, line, path):
    template = '_*[-a-z]+_*'
    line = line.strip()
    if 'def' in line or 'class' in line:
        line += """
    pass"""
    if '@' in line:
        line += """
def func():
    pass"""
    tree = ast.parse(line)
    res = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = [a.arg for a in node.args.args]
            for arg in args:
                if not re.match(template, arg):
                    res.append(f"{path}: Line {index + 1}: S010 Argument name '{arg}' should be snake_case")
    return res


def s011(index, line, path):
    template = '_*[-a-z]+_*'
    spaces = 0
    for each in line:
        if each == ' ':
            spaces += 1
        else:
            break
    if spaces < 4:
        return None
    line = line.strip()
    if 'def' in line or 'class' in line:
        line += """
    pass"""
    if '@' in line:
        line += """
def func():
    pass"""
    tree = ast.parse(line)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            try:
                var_name = node.targets[0].id
                if not re.match(template, var_name):
                    return f"{path}: Line {index + 1}: S011 Variable '{var_name}' in function should be snake_case"
            except AttributeError:
                return None


def s012(index, line, path):
    line = line.strip()
    if 'def' in line or 'class' in line:
        line += """
    pass"""
    if '@' in line:
        line += """
def func():
    pass"""
    tree = ast.parse(line)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            mutable = node.args.defaults
            if mutable:
                for mute in mutable:
                    if isinstance(mute, ast.List) or isinstance(mute, ast.Dict) or (isinstance(mute, ast.Set)):
                        return f"{path}: Line {index + 1}: S012 Default argument is mutable"


def printer(*issues):
    for issue in issues:
        if type(issue) == list:
            issue = '\n'.join(issue)
        if issue:
            print(issue)


def dirs(arg):
    global empty_lines
    files = os.listdir(arg)
    for each in files:
        if '.py' not in each:
            continue
        with open(f'{arg}\\{each}', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip('\n') for line in lines]
            for index, line in enumerate(lines):
                if line == '':
                    empty_lines += 1
                    continue
                issues = []
                path = name.filename + '\\' + each
                issues.append(s001(index, line, path))
                issues.append(s002(index, line, path))
                issues.append(s003(index, line, path))
                issues.append(s004(index, line, path))
                issues.append(s005(index, line, path))
                if empty_lines > 2:
                    issues.append(s006(index, path))
                issues.append(s007(index, line, path))
                issues.append(s008(index, line, path))
                issues.append(s009(index, line, path))
                issues.append(s010(index, line, path))
                issues.append(s011(index, line, path))
                issues.append(s012(index, line, path))
                printer(*issues)
                empty_lines = 0


def files(arg):
    global empty_lines
    with open(f'{arg}', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.strip('\n') for line in lines]
        for index, line in enumerate(lines):
            if line == '' or line.replace(' ', '') == '':
                empty_lines += 1
                continue
            issues = []
            issues.append(s001(index, line, str(name.filename)))
            issues.append(s002(index, line, str(name.filename)))
            issues.append(s003(index, line, str(name.filename)))
            issues.append(s004(index, line, str(name.filename)))
            issues.append(s005(index, line, str(name.filename)))
            if empty_lines > 2:
                issues.append(s006(index, str(name.filename)))
            issues.append(s007(index, line, str(name.filename)))
            issues.append(s008(index, line, str(name.filename)))
            issues.append(s009(index, line, str(name.filename)))
            issues.append(s010(index, line, str(name.filename)))
            issues.append(s011(index, line, str(name.filename)))
            issues.append(s012(index, line, str(name.filename)))
            printer(*issues)
            empty_lines = 0


p = argparse.ArgumentParser()
p.add_argument('filename')
name = p.parse_args()
empty_lines = 0
try:
    dirs(name.filename)
except NotADirectoryError:
    files(name.filename)

