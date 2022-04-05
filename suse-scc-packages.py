#!/usr/bin/python3

# Copyright 2022 Thomas Schulte
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import requests
import json
import enquiries
import csv
import getopt
import sys


def fetch_products(url):
    result = {}

    try:
        r = requests.get(url)
        r.raise_for_status()
        products_data = json.loads(r.content.decode())

        for product in products_data['data']:
            if not product['name'] in result:
                result[product['name']] = {}

            if not product['edition'] in result[product['name']]:
                result[product['name']][product['edition']] = {}
                result[product['name']][product['edition']]['archs'] = {}

            if not product['architecture'] in result[product['name']][product['edition']]:
                result[product['name']][product['edition']]['archs'][product['architecture']] = product['identifier']

    except Exception as exc:
        print(exc)
        return None

    return result


def chooser(items):
    try:
        product = enquiries.choose('Choose a product: ', items)
        edition = enquiries.choose('Choose an edition: ', items[product])
        arch = enquiries.choose('Choose an architecture: ', items[product][edition]['archs'])
        result = items[product][edition]['archs'][arch]
    except Exception as exc:
        print(exc)
        return None

    return result


def fetch_packages(url):
    pkgs = []

    try:
        r = requests.get(url)
        r.raise_for_status()
        packages_data = json.loads(r.content.decode())

        for pkg in packages_data['data']:
            line = pkg['name'], pkg['products'][0]['name']
            pkgs.append(tuple(line))

    except Exception as exc:
        print(exc)
        return None

    return pkgs


def write_to_csv(data, outfile):
    csvfile = open(outfile, "w")
    writer = csv.writer(csvfile)

    for row in data:
        writer.writerow(row)

    csvfile.close()


def print_cmd_info():
    print("""usage: %s [-d <output_directory>]
    General:
        -h,   --help              print this help

    Optional:
        -d,   --directory=DIR     create CSV file in output directory (instead of stdout)"""
          % os.path.basename(__file__))


if __name__ == '__main__':
    output_directory = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "directory="])

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print_cmd_info()
                exit()
            elif opt in ('-d', '--directory'):
                if not arg.endswith('/'):
                    arg = arg + '/'
                output_directory = arg

    except getopt.GetoptError:
        print_cmd_info()
        exit(2)

    products_url = 'https://scc.suse.com/api/package_search/products'
    products = fetch_products(products_url)

    if not products:
        print("Could not fetch products.")
        exit(1)

    identifier = chooser(products)

    if not identifier:
        print("Could not fetch identifier.")
        exit(1)

    packages_url = 'https://scc.suse.com/api/package_search/packages?product_id=' + str(identifier)
    packages = fetch_packages(packages_url)

    if not packages:
        print("Could not fetch packages.")
        exit(1)

    if output_directory:
        version_str = str(identifier.replace('/', '-'))
        output_file = output_directory + 'packages_' + version_str + '.csv'

        try:
            write_to_csv(packages, output_file)
            print("File " + output_file + " successfully written.")
            exit(0)
        except Exception as err:
            print("Failed to write " + output_file + ". (" + str(err) + ")")
            exit(1)
    else:
        for package in packages:
            print("%s,%s" % package)
