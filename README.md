# clash-multi-conf
A simple clash wrapper making clash support multiple config files.

## Multiple Config Files
an example:
```bash
clash-conf-dir
├── config.yaml
└── conf.d
    ├── 00-conf1.yaml
    ├── 01-conf2.yaml
    └── 02-conf3.yaml
```
the script will try to merge all the yaml files, if there are conflicts,
the value in later file will overwrite the value in previous one.

if you use `-f` option, the multiple config files function will be disabled,
the script will act exactly the same as the original clash.

## ArchLinux Installation
```bash
1. clone this repo and cd into it
2. $ paru -S python-deepmerge
3. $ makepkg -si
```

## Usage
1. make sure clash is in your $PATH
2. run clash-multi-conf.py the same way you would run clash



