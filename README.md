# suse-scc-packages
List packages of a given SUSE product

## Setup
1. (optional) Create and enter virtual Python environment:
   ```shell
   $ cd <my-project-dir>
   $ python3 -m venv ./venv
   $ source venv/bin/activate
   ```

2. Install required dependencies:
   ```shell
   $ cd <my-project-dir>
   $ pip3 install -r requirements.txt
   ```

## Usage
```shell
$ python3 suse-scc-packages.py -h

usage: suse-scc-packages.py [-d <output_directory>]
    General:
        -h,   --help              print this help

    Optional:
        -d,   --directory=DIR     create CSV file in output directory (instead of stdout)
```

### Write results to stdout
```shell
$ python3 suse-scc-packages.py
```

### Write results to CSV file
```shell
$ python3 suse-scc-packages.py -d /tmp
```
