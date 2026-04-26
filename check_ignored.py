import argparse
import os
import re

# run:
# py -3 check_ignored.py --project_dir=path\\to\\repo


def norm_path(path):
    return path.replace('\\', '/')


def parse_gitignore(gitignore_path):
    rules = []

    with open(gitignore_path, 'r', encoding='utf-8') as file:
        for raw_line in file:
            line = raw_line.strip().lstrip('\ufeff')
            if not line or line.startswith('#'):
                continue

            rule = norm_path(line)
            if rule.startswith('*'):
                regex_text = '^' + re.escape(rule).replace(r'\*', '.*') + '$'
                rules.append(('wild', rule, re.compile(regex_text)))
            else:
                rules.append(('exact', rule, None))

    return rules


def collect_files(project_dir):
    result = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = sorted([d for d in dirs if d != '.git'])
        files = sorted(files)

        for file_name in files:
            full_path = os.path.join(root, file_name)
            rel_path = norm_path(os.path.relpath(full_path, project_dir))
            result.append(rel_path)

    return result


def make_out_path(project_dir, rel_path):
    if '/' not in rel_path:
        return rel_path

    project_name = os.path.basename(os.path.normpath(project_dir))
    return norm_path(os.path.join(project_name, rel_path))


def find_ignored(project_dir, rules):
    files = collect_files(project_dir)
    used = set()
    ignored = []

    for rule_type, rule_value, rule_regex in rules:
        for rel_path in files:
            if rel_path in used:
                continue

            matched = False
            if rule_type == 'exact' and rel_path == rule_value:
                matched = True
            if rule_type == 'wild' and rule_regex.match(rel_path):
                matched = True

            if matched:
                used.add(rel_path)
                out_path = make_out_path(project_dir, rel_path)
                ignored.append((out_path, rule_value))

    return ignored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', required=True)
    args = parser.parse_args()

    gitignore_path = os.path.join(args.project_dir, '.gitignore')
    if not os.path.isfile(gitignore_path):
        raise FileNotFoundError(f'.gitignore not found: {gitignore_path}')

    rules = parse_gitignore(gitignore_path)
    ignored_files = find_ignored(args.project_dir, rules)

    print('Ignored files:')
    for file_path, rule in ignored_files:
        print(f'{file_path} ignored by expression {rule}')


if __name__ == '__main__':
    main()
