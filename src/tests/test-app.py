import unittest
import json
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import app

televisore = {
        "name": "televisore",
        "keys": [
            {
                "id": "KEY_5",
                "name": "5"
            },
            {
                "id": "KEY_3",
                "name": "3"
            },
            {
                "id": "KEY_9",
                "name": "9"
            },
            {
                "id": "KEY_MUTE",
                "name": "MUTE"
            },
            {
                "id": "KEY_7",
                "name": "7"
            },
            {
                "id": "KEY_VOLUMEDOWN",
                "name": "VOLUMEDOWN"
            },
            {
                "id": "KEY_CHANNELDOWN",
                "name": "CHANNELDOWN"
            },
            {
                "id": "KEY_CHANNELUP",
                "name": "CHANNELUP"
            },
            {
                "id": "KEY_4",
                "name": "4"
            },
            {
                "id": "KEY_8",
                "name": "8"
            },
            {
                "id": "KEY_POWER",
                "name": "POWER"
            },
            {
                "id": "KEY_2",
                "name": "2"
            },
            {
                "id": "KEY_1",
                "name": "1"
            },
            {
                "id": "KEY_0",
                "name": "0"
            },
            {
                "id": "KEY_VOLUMEUP",
                "name": "VOLUMEUP"
            },
            {
                "id": "KEY_6",
                "name": "6"
            }
        ]
    }

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '200 OK')

    def test_post_key(self):
        rv = self.app.post('/device/televisore/key/POWER')
        self.assertEqual(rv.status, '500 INTERNAL SERVER ERROR')
        #self.assertEqual(json.loads(rv.data.decode("utf-8")), {"message": "Action executed"})

    def test_get_device(self):
        name = "televisore"
        body = televisore
        rv = self.app.get('/device/{}'.format(name))
        self.assertEqual(rv.status, '200 OK')
        self.maxDiff = None
        dict_received = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(dict_received['device']['name'], name)
        pairs = zip(dict_received['device']['keys'],body['keys'])
        same = any(x != y for x, y in pairs)
        self.assertEqual(same, True)

    def test_get_remote_control(self):
        name = 'piano5'
        rv = self.app.get('/remote_control')
        self.assertEqual(rv.status, '200 OK')
        dict_received = json.loads(rv.data.decode("utf-8"))
        devices = ('televisore', 'stereo', 'proiettore')
        notfound = {}
        for device in devices:
          notfound[device] = True
        for x in dict_received['devices']:
          for device in devices:
            if x['name'] == device:
              notfound[device] = False
        self.assertEqual(any(notfound.values()), False)

    def test_get_inexistent_item(self):
        name = 'piano6'
        rv = self.app.get('/item/{}'.format(name))
        self.assertEqual(rv.status, '404 NOT FOUND')

if __name__ == '__main__':
    unittest.main()
