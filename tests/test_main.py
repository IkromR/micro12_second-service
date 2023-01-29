import requests
api_url = 'http://localhost:8001'


def test_healthcheck():
    responce = requests.get(f'{api_url}/__health')
    assert responce.status_code == 200


class TestLoyalty:
    def test_get_empty_loyalty(self):
        responce = requests.get(f'{api_url}/v1/loyalty')
        assert responce.status_code == 200
        assert len(responce.json()) == 0

    def test_create_loyalty(self):
        body = { "name": "nameTest" }
        responce = requests.post(f'{api_url}/v1/loyalty', json=body)
        assert responce.status_code == 200
        assert responce.json().get("name") == "nameTest"
        assert responce.json().get("id") == 0

    def test_get_loyalty_by_id(self):
        responce = requests.get(f'{api_url}/v1/loyalty/0')
        assert responce.status_code == 200
        assert responce.json().get("name") == "nameTest"
        assert responce.json().get("id") == 0

    def test_get_not_empty_loyalty(self):
        responce = requests.get(f'{api_url}/v1/loyalty')
        assert responce.status_code == 200
        assert len(responce.json()) == 1
