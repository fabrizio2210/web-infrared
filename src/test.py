import unittest
import json
import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status, '404 NOT FOUND')

    def test_post_item(self):
        body = {'price': 11.99, 'name': 'piano'}
        rv = self.app.post('/item/piano', data=body)
        self.assertEqual(rv.status, '201 CREATED')
        self.assertEqual(json.loads(rv.data.decode("utf-8")), body)

    def test_put_item(self):
        name = 'piano2'
        body = {'price': 11.99, 'name': name}
        rv = self.app.put('/item/{}'.format(name), data=body)
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data.decode("utf-8")), body)

    def test_put_item2(self):
        name = 'piano3'
        body = {'price': 11.99, 'name': name}
        self.app.post('/item/{}'.format(name), data=body)
        body = {'price': 12.99, 'name': name}
        self.app.put('/item/{}'.format(name), data=body)
        rv = self.app.get('/item/{}'.format(name))
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data.decode("utf-8")), {'item':body})

    def test_get_item(self):
        name = 'piano4'
        body = {'price': 12.99, 'name': name}
        self.app.put('/item/{}'.format(name), data=body)
        rv = self.app.get('/item/{}'.format(name))
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data.decode("utf-8")), {'item':body})

    def test_get_item2(self):
        name = 'piano5'
        body = {'price': 11.99, 'name': name}
        self.app.post('/item/{}'.format(name), data=body)
        rv = self.app.get('/item/{}'.format(name))
        self.assertEqual(rv.status, '200 OK')
        self.assertEqual(json.loads(rv.data.decode("utf-8")), {'item':body})

    def test_get_inexistent_item(self):
        name = 'piano6'
        rv = self.app.get('/item/{}'.format(name))
        self.assertEqual(rv.status, '404 NOT FOUND')

if __name__ == '__main__':
    unittest.main()
