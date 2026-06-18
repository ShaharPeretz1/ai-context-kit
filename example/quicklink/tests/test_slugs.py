from app.slugs import generate_slug


def test_slug_is_seven_base62_chars():
    s = generate_slug()
    assert len(s) == 7
    assert all(c.isalnum() for c in s)


def test_slugs_are_unique_enough():
    # Not a real collision test, just a smoke check that we're not constant.
    assert len({generate_slug() for _ in range(1000)}) > 990
