import argparse
import os
import time

# run:
# py -3 clean_trash.py --trash_folder_path=path\\to\\trash --age_thr=120
# stop: Ctrl+C

LOG_FILE_NAME = 'clean_trash.log'


def write_log(log_file, path):
    log_file.write(f'{path}\n')


def is_old(file_path, now_ts, age_thr):
    return now_ts - os.path.getmtime(file_path) > age_thr


def clean_old_files(trash_folder_path, age_thr, log_file):
    now_ts = time.time()

    for root, _, files in os.walk(trash_folder_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if is_old(file_path, now_ts, age_thr):
                try:
                    os.remove(file_path)
                    write_log(log_file, file_path)
                except OSError:
                    continue


def clean_empty_dirs(trash_folder_path, log_file):
    for root, dirs, _ in os.walk(trash_folder_path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                os.rmdir(dir_path)
                write_log(log_file, dir_path)
            except OSError:
                continue


def run_cleaner(trash_folder_path, age_thr):
    with open(LOG_FILE_NAME, 'a', encoding='utf-8') as log_file:
        while True:
            clean_old_files(trash_folder_path, age_thr, log_file)
            clean_empty_dirs(trash_folder_path, log_file)
            log_file.flush()
            time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--trash_folder_path', required=True)
    parser.add_argument('--age_thr', type=int, required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.trash_folder_path):
        raise NotADirectoryError(f'trash folder does not exist: {args.trash_folder_path}')

    if args.age_thr < 0:
        raise ValueError('--age_thr must be non-negative')

    run_cleaner(args.trash_folder_path, args.age_thr)


if __name__ == '__main__':
    main()
