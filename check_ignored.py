import argparse
import os
import re

# run:
# py -3 check_ignored.py --project_dir=path\\to\\repo


def norm_path(path):
    return path.replace('\\', '/')


def parse_gitignore(gitignore_path):
    exact_rules = []
    wildcard_rules = []

    with open(gitignore_path, 'r', encoding='utf-8') as file:
        for raw_line in file:
            line = raw_line.strip()
            if not line or line.startswith('#'):
                continue

            rule = norm_path(line)
            if rule.startswith('*'):
                regex_text = '^' + re.escape(rule).replace(r'\*', '.*') + '$'
                wildcard_rules.append((rule, re.compile(regex_text)))
            else:
                exact_rules.append(rule)

    return exact_rules, wildcard_rules


def make_out_path(project_dir, rel_path):
    project_name = os.path.basename(os.path.normpath(project_dir))
    return norm_path(os.path.join(project_name, rel_path))


def find_ignored(project_dir, exact_rules, wildcard_rules):
    ignored = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d != '.git']

        for file_name in files:
            full_path = os.path.join(root, file_name)
            rel_path = norm_path(os.path.relpath(full_path, project_dir))

            matched = False

            for rule in exact_rules:
                if rel_path == rule:
                    ignored.append((make_out_path(project_dir, rel_path), rule))
                    matched = True
                    break

            if matched:
                continue

            for rule, regex in wildcard_rules:
                if regex.match(rel_path):
                    ignored.append((make_out_path(project_dir, rel_path), rule))
                    break

    return ignored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', required=True)
    args = parser.parse_args()

    gitignore_path = os.path.join(args.project_dir, '.gitignore')
    if not os.path.isfile(gitignore_path):
        raise FileNotFoundError(f'.gitignore not found: {gitignore_path}')

    exact_rules, wildcard_rules = parse_gitignore(gitignore_path)
    ignored_files = find_ignored(args.project_dir, exact_rules, wildcard_rules)

    print('Ignored files:')
    for file_path, rule in ignored_files:
        print(f'{file_path} ignored by expression {rule}')


if __name__ == '__main__':
    main()
