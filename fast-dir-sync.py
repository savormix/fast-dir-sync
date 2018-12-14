import argparse
import os
import os.path
import shutil


total_files = 0


def sync_dir(dir_from, dir_to, dry_run):
    if not os.path.exists(dir_to):
        # print(f'[MISS]: "{dir_from}"->"{dir_to}"')
        print('[MISS]: "{}"->"{}"'.format(dir_from, dir_to))
        if not dry_run:
            os.makedirs(dir_to, exist_ok=True)
    for path in sorted(os.listdir(dir_from)):
        full_path = os.path.join(dir_from, path)
        if os.path.isdir(full_path):
            sync_dir(full_path, os.path.join(dir_to, path), dry_run)
        else:
            sync_file(full_path, os.path.join(dir_to, path), dry_run)
        

def sync_file(file_from, file_to, dry_run):
    global total_files
    
    reason = ''
    if not os.path.exists(file_to):
        reason = 'MISS'
    elif os.path.getsize(file_from) != os.path.getsize(file_to):
        reason = 'SIZE'
    elif os.path.getmtime(file_from) != os.path.getmtime(file_to):
        reason = 'MODT'
    
    if reason == '':
        return
    
    # print(f'[{reason}]: "{file_from}"->"{file_to}"')
    print('[{}]: "{}"->"{}"'.format(reason, file_from, file_to))
    total_files += 1
    if not dry_run:
        shutil.copy2(file_from, file_to)


def main():
    global total_files
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true', help='Simply print files that need sync')
    parser.add_argument('dir_from')
    parser.add_argument('dir_to')
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir_from) or not os.path.isdir(args.dir_to):
        print('Can only sync existent directory trees')
        return
    
    sync_dir(args.dir_from, args.dir_to, args.dry_run)
    action = 'pending sync' if args.dry_run else 'synchronized'
    # print(f'Total {total_files} file(s) {action}')
    print('Total {} file(s) {}'.format(total_files, action))


main()
