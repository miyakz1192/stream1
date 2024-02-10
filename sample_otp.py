import pyotp

totp = pyotp.TOTP('base32secret3232') # サーバー側であらかじめ指定する一意の値
totp.now() # => '492039'                # nowメソッドで値の確認

print(totp.now())
print(totp.verify('275734') )                       # => True
