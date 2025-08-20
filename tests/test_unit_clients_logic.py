from tests.clients_logic import can_update_client, is_valid_email, is_unique_username


def test_can_update_client():
    admin = type("User", (), {"id": 1, "role_id": 1})()  # Simuler un user admin
    user1 = type("User", (), {"id": 2, "role_id": 3})()
    user2 = type("User", (), {"id": 3, "role_id": 3})()

    assert can_update_client(admin, user1) is True  # Admin peut modifier
    assert can_update_client(user1, user1) is True  # User peut modifier lui-même
    assert can_update_client(user1, user2) is False # User ne peut pas modifier un autre user



def test_is_valid_email():
    assert is_valid_email("test@example.com") is True
    assert is_valid_email("bademail") is False
    assert is_valid_email("nouser@domain") is False


def test_is_unique_username():
    users = [{"username": "alice"}, {"username": "bob"}]
    assert is_unique_username("charlie", users) is True
    assert is_unique_username("alice", users) is False