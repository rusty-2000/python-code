def test_upload_csv(client):
    with open('tests/data/test_data.csv', 'rb') as test_file:
        response = client.post('/api/v1/upload', data={'file': test_file})
        assert response.status_code == 200
        assert 'request_id' in response.json

