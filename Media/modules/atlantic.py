import json
import uuid
import qrcode
import hashlib
import requests
from httpx import AsyncClient
from Media.config import API_KEY_ATLANTIC

POST = 'https://atlantich2h.com'

async def generate_unique_ref_id():
    return 'CFx' + uuid.uuid4().hex[:16].upper()

async def cek_informasi_account():
    api_key = API_KEY_ATLANTIC
    payload = {
        'api_key': api_key,
        'name': 'name',
        'username': 'username',
        'email': 'email',
        'phone': 'phone',
        'balance': 'balance'
    }
    url = f'{POST}/get_profile'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers,
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e

async def list_harga(code):
    api_key = API_KEY_ATLANTIC
    payload = {
        'api_key': api_key,
        'code': code,
        'type': 'prabayar',
    }
    url = f'{POST}/layanan/price_list'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers,
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e
            
async def new_transaksi(reff_id, code, target):
    api_key = API_KEY_ATLANTIC
    payload = {
        'api_key': api_key,
        'reff_id': reff_id,
        'code': code,
        'target': target,
    }
    url = f'{POST}/transaksi/create'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers,
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e

async def status_transaksi(id, reff_id):
    api_key = API_KEY_ATLANTIC
    payload = {
        'api_key': api_key,
        'id': id,
        'reff_id': reff_id,
        'type': 'prabayar',
    }
    url = f'{POST}/transaksi/status'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers,
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e
            
async def cancel_deposit(id):
    api_key = API_KEY_ATLANTIC
    payload = {
        'id': id,
        'api_key': api_key,
        'status': 'cancel'
    }
    url = f'{POST}/deposit/cancel'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers,
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e
            
async def new_deposit(reff_id, metode, nominal, tambahan, fee, get_balance):
    api_key = API_KEY_ATLANTIC
    payload = {
        'api_key': api_key,
        'reff_id': reff_id,
        'nominal': nominal,
        'tambahan': tambahan,
        'fee': fee,
        'get_balance': get_balance,
        'type': 'ewallet',
        'metode': metode 
    }
    url = f'{POST}/deposit/create'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers, 
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e

async def view_deposit(id, reff_id):
    api_key = API_KEY_ATLANTIC
    payload = {
        'id': id,
        'api_key': api_key,
        'reff_id': reff_id
    }
    url = f'{POST}/deposit/status'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with AsyncClient() as session:
        try:
            response = await session.post(
                url, headers=headers, 
                data=payload
            )
            data = response.json()
            return data
        except BaseException as e:
            return e
            
async def create_qris(data, path):
    # Membuat objek QR Code
    qr = qrcode.QRCode(
        version=1,  # Mengontrol ukuran QR Code (1 adalah ukuran terkecil)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Mengontrol level koreksi kesalahan
        box_size=10,  # Ukuran tiap kotak dalam QR Code
        border=4,  # Lebar border di sekitar QR Code
    )

    # Menambahkan data ke QR Code
    qr.add_data(data)
    qr.make(fit=True)

    # Membuat gambar QR Code
    img = qr.make_image(fill='black', back_color='white')

    # Menyimpan gambar QR Code
    
    img.save(path)
    return path
