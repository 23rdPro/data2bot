import unittest
import json
from src.config.files import file2, t1, t2
from src.response.file_reader import JSONFileReader


class TestJSONFileReader(unittest.TestCase):
    def setUp(self) -> None:
        f1 = open(file2)
        f2 = open(file2)
        self.data = json.loads(f1.read())
        self.copy = json.loads(f2.read())
        f1.close()
        f2.close()

    def test_data_padding(self):
        self.assertDictEqual(self.data, self.copy)
        self.assertNotIn('tag', self.data["message"])
        self.assertNotIn("description", self.data["message"])
        self.assertNotIn("required", self.data["message"])
        instance = JSONFileReader()
        instance.pad_attrs(self.data)
        self.assertNotEqual(self.data, self.copy)
        self.assertNotEqual(self.data["message"], self.copy["message"])
        self.assertIn('tag', self.data["message"])
        self.assertIn("description", self.data["message"])
        self.assertIn("required", self.data["message"])

    def test_value_types(self):
        a = JSONFileReader()
        b = JSONFileReader()
        a.perform_ops(self.data, t1)
        b.perform_ops(self.copy, t2)

        out1 = open(t1)
        out2 = open(t2)

        out_d_1 = json.loads(out1.read())
        out_d_2 = json.loads(out2.read())

        def dfs(d, output=None):
            if output is None:
                output = []
            for k, v in d.items():
                if isinstance(v, dict):
                    dfs(v, output)
                else:
                    if isinstance(v, str):
                        output.append("STRING")
                    elif isinstance(v, int):
                        output.append("INTEGER")
                    elif v and isinstance(v, list) and \
                            isinstance(v[0], str):
                        output.append("ENUM")
                    elif v and isinstance(v, list) and \
                            isinstance(v[0], dict):
                        output.append("ARRAY")
            return output

        self.assertListEqual(dfs(out_d_1), dfs(out_d_2))
        out1.close()
        out2.close()

