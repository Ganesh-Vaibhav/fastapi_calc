from app.security import hash_password, verify_password


def test_hash_and_verify_password():
    raw_password = "supersecret123"
    password_hash = hash_password(raw_password)

    assert password_hash != raw_password
    assert verify_password(raw_password, password_hash)
    assert not verify_password("wrongpassword", password_hash)
