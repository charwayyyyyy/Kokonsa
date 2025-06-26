def test_hello_plugin(client):
    resp = client.get('/hello-plugin')
    assert resp.status_code == 200
    assert b'Hello from plugin!' in resp.data
