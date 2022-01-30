import os
import shutil
import subprocess
import tempfile
import unittest
from donkeycar.parts.tub_v2 import Tub


class TestTub(unittest.TestCase):

    def setUp(self):
        self._path = tempfile.mkdtemp()
        inputs = ['input']
        types = ['int']
        metadata = [("meta1", "metavalue1")]
        self.tub = Tub(self._path, inputs, types, metadata)


    def test_basic_tub_operations(self):
        entries = list(self.tub)
        self.assertEqual(len(entries), 0)
        write_count = 10
        delete_indexes = [0, 8]

        records = [{'input': i} for i in range(write_count)]
        
        for record in records:
            self.tub.write_record(record)
        
        for index in delete_indexes:
            self.tub.delete_records(index)

        count = 0
        for record in self.tub:
            print('Record %s' % (record))
            count += 1
        # assert True == False
        self.assertEqual(count, (write_count - len(delete_indexes)))
        self.assertEqual(len(self.tub), (write_count - len(delete_indexes)))

        # Note that self.tub.metadata is an array of tuples
        print(self.tub.metadata)
        assert ("meta1", "metavalue1") in self.tub.metadata 

    # def test_delete_last_n_records(self):
    #     start_len = len(self.tub)
    #     self.tub.delete_last_n_records(2)
    #     self.assertEqual(start_len - 2, len(self.tub),
    #                      "error in deleting 2 last records")
    #     self.tub.delete_last_n_records(3)
    #     self.assertEqual(start_len - 5, len(self.tub),
    #                      "error in deleting 3 last records")
    
    def test_empty_tub(self):
        assert len(self.tub) == 0
        tub_iter = iter(self.tub)

        self.assertRaises(StopIteration, next, tub_iter)

    def tearDown(self):
        if os.name == 'nt':
            # if the platform is Windows
            subprocess.Popen(f"rmdir /S /Q {self._path}") # for Windows only
        else:
            shutil.rmtree(self._path) # this line is not for Windows

        # Note that self.tub.manifest.metadata is a dict
        assert self.tub.manifest.metadata['meta1'] == "metavalue1"


if __name__ == '__main__':
    unittest.main()