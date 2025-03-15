import pytest
from app.models.black_white_list import BlackWhiteList

def test_create_black_white_list(client):
    response = client.post('/api/black-white-list', json={
        'address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'operator': 'Admin',
        'type': 1,
        'organization': '中国人民银行',
        'region': '香港'
    })
    
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert response.json['data']['address'] == '0x742d35Cc6634C0532925a3b844Bc454e4438f44e'

def test_get_black_white_list(client):
    # First create a test record
    client.post('/api/black-white-list', json={
        'address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'operator': 'Admin',
        'type': 1,
        'organization': '中国人民银行',
        'region': '香港'
    })
    
    response = client.get('/api/black-white-list')
    assert response.status_code == 200
    assert response.json['code'] == 200
    assert len(response.json['data']['list']) > 0

def test_duplicate_address(client):
    # Create first record
    client.post('/api/black-white-list', json={
        'address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'operator': 'Admin',
        'type': 1,
        'organization': '中国人民银行',
        'region': '香港'
    })
    
    # Try to create duplicate
    response = client.post('/api/black-white-list', json={
        'address': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'operator': 'Admin',
        'type': 2,
        'organization': '中央网信办',
        'region': '深圳'
    })
    
    assert response.status_code == 400
    assert response.json['message'] == 'Address already exists' 