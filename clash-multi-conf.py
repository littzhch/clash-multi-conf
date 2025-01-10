#!/usr/bin/python3

import os
import argparse
from tempfile import NamedTemporaryFile
from os.path import join, exists
import yaml
import deepmerge
from deepmerge import STRATEGY_END


def custom_list(_config, path, base_val, nxt):
    if path[0] == "proxy-groups":
        for item in nxt:
            for origin in base_val:
                if origin['name'] == item['name'] and origin['type'] == item[
                        'type']:
                    origin['proxies'].extend(item['proxies'])
        return base_val
    return STRATEGY_END


merger = deepmerge.Merger([(list, [custom_list, "append"]), (dict, ["merge"]),
                           (set, ["union"])], ["override"], ["override"])


def clash_config_dir() -> str:
    return join(os.environ['HOME'], '.config', 'clash')


# return a list of path
def find_all_config_files(config_dir: str) -> list[str]:
    conf_d = join(config_dir, 'conf.d')
    config_files = []

    if exists(join(config_dir, 'config.yaml')):
        config_files.append(join(config_dir, 'config.yaml'))

    if exists(conf_d):
        for file in sorted(os.listdir(conf_d)):
            if file.endswith('.yaml') and os.path.isfile(join(conf_d, file)):
                config_files.append(join(conf_d, file))

    return config_files


def merge_config_files(config_files: list[str]) -> str:
    merged_config = {}
    for file in config_files:
        with open(file, 'r', encoding="UTF-8") as f:
            config = yaml.safe_load(f)
            if config is not None:
                merged_config = merger.merge(merged_config, config)

    return yaml.dump(merged_config)


def main():
    args = get_args()
    args_list = ["clash"]
    if args.d:
        args_list += ["-d", args.d]
    if args.ext_ctl:
        args_list += ["-ext-ctl", args.ext_ctl]
    if args.ext_ui:
        args_list += ["-ext-ui", args.ext_ui]
    if args.f:
        args_list += ["-f", args.f]
    if args.secret:
        args_list += ["-secret", args.secret]
    if args.t:
        args_list += ["-t"]
    if args.v:
        args_list += ["-v"]

    config_dir = clash_config_dir()
    if args.f:
        os.execvp("clash", args_list)
    if args.d:
        config_dir = args.d

    config_files = find_all_config_files(config_dir)
    merged_config = merge_config_files(config_files)

    if len(merged_config) <= 3:
        os.execvp("clash", args_list)

    tmpfile = NamedTemporaryFile(delete=False)
    tmpfile.write(bytes(merged_config, encoding="UTF-8"))
    args_list += ["-f", tmpfile.name]

    os.execvp("clash", args_list)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type=str, help='set configuration directory')
    parser.add_argument('-ext-ctl',
                        type=str,
                        help='override external controller address')
    parser.add_argument('-ext-ui',
                        type=str,
                        help='override external ui directory')
    parser.add_argument(
        '-f',
        type=str,
        help='specify configuration file. if set, multi-conf will be disabled')
    parser.add_argument('-secret',
                        type=str,
                        help='override secret for RESTful API')
    parser.add_argument('-t',
                        action='store_true',
                        help='test configuration and exit')
    parser.add_argument('-v',
                        action='store_true',
                        help='show current version of clash')
    return parser.parse_args()


if __name__ == '__main__':
    main()
