# /usr/bin/env python3

import argparse
import logging


def argument_parser():

    parser = argparse.ArgumentParser(
        description='This script will parse nginx log file and return the number of occurrences of evert status code')
    parser.add_argument('-file', '-f', dest='nginx_log_file',
                        help='Path to NGINX log file',
                        required=True
                        )
    args = parser.parse_args()
    return args


def open_file(file):

    try:
        with open(file) as access_log:
            access_log = access_log.read()
            return access_log
    except:
        logging.error(f'Failed to open file: {file}')
        exit(2)


def build_status_code_dictionary(access_log):

    status_code_d = {}
    for line in access_log.splitlines():
        strip_string = line.strip()
        status_code = strip_string.split()[8]
        status_code_d[status_code] = status_code_d.get(status_code, 0) + 1
    return status_code_d


def print_dictionary_table(status_code_dictionary):

    str_fmt = "{:<15}  {:<15}"
    print(str_fmt.format('STATUS_CODE', 'OCCURRENCES'))
    for k, v in status_code_dictionary.items():
        print(str_fmt.format(k, v))


def main():

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='[%Y-%m-%dT%H:%M:%S]',
        level=logging.INFO
    )
    args = argument_parser()
    file_name = args.nginx_log_file
    nginx_log = open_file(file_name)
    status_code_dictionary = build_status_code_dictionary(nginx_log)
    print_dictionary_table(status_code_dictionary)


if __name__ == "__main__":
    main()
