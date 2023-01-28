import json


class JSONFileReader:

    def __init__(self):
        pass

    def perform_ops(self, file_data, dump_dir):
        self.pad_attrs(file_data)
        msg_key = file_data["message"]
        annotate = self.annotate_data(msg_key)
        output = {"message": annotate}
        with open(dump_dir, 'w') as File:
            File.write(json.dumps(output, indent=4))

    @staticmethod
    def pad_attrs(file: dict) -> None:
        for attr in file:
            file[attr]["tag"] = ''
            file[attr]["description"] = ''
            file[attr]["required"] = False
        return

    @staticmethod
    def annotate_data(file: dict) -> dict:

        def dfs(d: dict) -> dict:
            for k, v in d.items():
                if isinstance(v, dict):
                    dfs(v)
                else:
                    if isinstance(v, str):
                        d[k] = "STRING"
                    elif isinstance(v, int):
                        d[k] = "INTEGER"
                    elif v and isinstance(v, list) and \
                            isinstance(v[0], str):
                        d[k] = "ENUM"
                    elif v and isinstance(v, list) and \
                            isinstance(v[0], dict):
                        d[k] = "ARRAY"
            return d

        return dfs(file)
