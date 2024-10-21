import unittest
from threading import Thread
from concurrent_collections.core import ConcurrentHashMap

class TestConcurrentHashMap(unittest.TestCase):

    def setUp(self):
        self.map = ConcurrentHashMap(capacity=10)

    def test_put_and_get(self):
        # Test inserting a value and retrieving it
        self.map.put('key1', 'value1')
        result = self.map.get('key1')
        self.assertEqual(result['key1'], 'value1')

    def test_get_non_existent_key(self):
        # Test retrieving a key that doesn't exist
        result = self.map.get('non_existent')
        self.assertIsNone(result)

    def test_contains_key(self):
        # Test checking for key existence
        self.map.put('key2', 'value2')
        result = self.map.contains_key('key2')
        self.assertTrue('key2' in result)
        self.assertIsNone(self.map.contains_key('non_existent'))

    def test_remove_key(self):
        # Test removing a key
        self.map.put('key3', 'value3')
        result = self.map.remove('key3')
        self.assertEqual(result, 'value3')
        self.assertIsNone(self.map.get('key3'))

    def test_clear(self):
        # Test clearing the map
        self.map.put('key4', 'value4')
        self.map.put('key5', 'value5')
        self.map.clear(None)
        self.assertEqual(len(self.map), 0)
        self.assertIsNone(self.map.get('key4'))

    def test_key_set(self):
        # Test retrieving all keys
        self.map.put('key6', 'value6')
        self.map.put('key7', 'value7')
        keys = self.map.key_set()
        self.assertIn('key6', keys)
        self.assertIn('key7', keys)

    def test_values(self):
        # Test retrieving all values
        self.map.put('key8', 'value8')
        self.map.put('key9', 'value9')
        values = self.map.values()
        self.assertIn('value8', values)
        self.assertIn('value9', values)

    def test_concurrent_put(self):
        # Test concurrent `put` operations
        def insert_values(start, end):
            for i in range(start, end):
                self.map.put(f'key{i}', f'value{i}')
        
        threads = [Thread(target=insert_values, args=(0, 100)), 
                   Thread(target=insert_values, args=(100, 200))]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(self.map), 200)
        self.assertEqual(self.map.get('key50')['key50'], 'value50')
        self.assertEqual(self.map.get('key150')['key150'], 'value150')

if __name__ == '__main__':
    unittest.main()
