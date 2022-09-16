import json
import csv
import argparse
import os


def find_all_file_in_directory(dir_path: str, file_types: list):
    result_file_list = []
    print(dir_path)
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            file_key, file_extension = os.path.splitext(file_path)
            if file_extension.lower() in map(lambda x: x.lower(), file_types):
                result_file_list.append(file_path)
    return result_file_list

def parse_annotation(annotation: dict, workloads: list):
    if annotation['type'] == 'slotChildren':
        workloads.extend(get_single_slot_or_input_workload(annotation, 'slots'))
        for child in annotation['children']:
            parse_annotation(child, workloads)
    if annotation['type'] == 'slot':
        workloads.extend(get_single_slot_or_input_workload(annotation, 'slots'))
    if annotation['type'] == 'input':
        workloads.extend(get_single_slot_or_input_workload(annotation, 'inputs'))

def get_single_slot_or_input_workload(annotation: dict, annotation_type: str):
    workloads = []
    for item in annotation[annotation_type].values():
        workloads.append({'teamName': item['teamName'] if 'teamName' in item else '', 'userName': item['userName'], 'poolName': item['poolName'], 'key': annotation['key'], 'label': annotation['label'], 'count': item['count']})
    return workloads


def run(test_path):
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir_path', default=test_path)
    args = parser.parse_args()

    json_file_paths = find_all_file_in_directory(args.json_dir_path, ['.json'])
    for json_file_path in json_file_paths:
        with open(json_file_path, 'r', encoding='utf-8') as json_io:
            json_data = json.load(json_io)

        workloads = []
        for annotation in json_data:
            parse_annotation(annotation, workloads)

        headers = ['teamName', 'userName', 'poolName', 'key', 'label', 'count']
        file_path, _ = os.path.splitext(json_file_path)
        with open(f'{json_file_path}.csv', 'w', encoding='utf8', newline='') as csv_io:
            writer = csv.DictWriter(csv_io, headers)
            writer.writeheader()
            for item in workloads:
                writer.writerow(item)


if __name__ == '__main__':
    test_path = '/Users/apple/Desktop/cmu'
    run(test_path)
