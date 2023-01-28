import json

from src.config.files import (
    file1,
    file2,
    file3,
    file4
)

from src.response.file_reader import JSONFileReader


def main():
    with open(file1, 'r') as File1:
        data1 = json.loads(File1.read())

    with open(file2, 'r') as File2:
        data2 = json.loads(File2.read())

    instance = JSONFileReader()

    for data, file in iter([(data1, file3), (data2, file4)]):
        instance.perform_ops(data, file)


if __name__ == "__main__":
    main()
