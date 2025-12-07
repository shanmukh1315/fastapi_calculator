def test_calculations_page_serves_html(client):
    resp = client.get('/calculations')
    assert resp.status_code == 200
    assert 'Calculations (BREAD)' in resp.text
