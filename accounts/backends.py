# your_app/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import IncUsers # Asumsikan model user Anda bernama Siswa
# Anda mungkin perlu mengimpor library hashing yang sesuai jika hash Anda bukan SHA256 biasa
import hashlib
import bcrypt

class OracleIncUsersBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Ambil user dari model Siswa Anda menggunakan NIK
            user = IncUsers.objects.get(nik=username)
        except IncUsers.DoesNotExist:
            return None # User tidak ditemukan

        # VERIFIKASI PASSWORD
        # Ini adalah bagian terpenting. Anda harus tahu algoritma hashing yang digunakan
        # untuk menghasilkan hash di kolom SISWA.PASSWORD Anda.
        # Dari screenshot, 'BFEBEA6C5DB101150499C41C526F7D26BF035F216C6E8908320496E781B851D6'
        # terlihat seperti hash SHA256 (64 karakter heksadesimal).

        # Contoh VERIFIKASI DENGAN SHA256 (jika itu adalah algoritma yang digunakan)
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                
                return user # Password cocokelse:                logger.warning(f"Login failed: Password mismatch for user {username}.")
                returnNone

        if hashed_input_password == user.password: # Bandingkan dengan hash dari DB
            # Jika cocok, kembalikan objek user
            # Penting: Pastikan user_obj ini adalah instance dari model user yang dipakai Django
            # (misal: django.contrib.auth.models.User)
            # Jika Siswa adalah model user utama Anda, pastikan Siswa mewarisi AbstractBaseUser
            # atau memiliki field-field yang dibutuhkan Django auth.
            return user 
        return None # Password tidak cocok

    def get_user(self, user_id):
        try:
            return IncUsers.objects.get(pk=user_id)
        except IncUsers.DoesNotExist:
            return None
