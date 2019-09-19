import time

import pytest

from httparrot import responses, make_app


@pytest.fixture
def app():
    responses.clear()
    return make_app()


@pytest.fixture
def fetch(http_client, base_url):
    async def do_fetch(url, *args, **kwargs):
        return await http_client.fetch(
            base_url + url,
            *args,
            raise_error=False,
            allow_nonstandard_methods=True,
            **kwargs,
        )
    return do_fetch


@pytest.mark.gen_test
@pytest.mark.parametrize("uri", ["/", "/asdf", "/some/path"])
@pytest.mark.parametrize("status", [200, 301, 400, 524])
@pytest.mark.parametrize("body", [b"1234", b"aphabetical", b"\1\2", None])
async def test_can_get_stored_response(fetch, uri, body, status):
    await fetch(f"{uri}?status={status}", method="POST", body=body)
    response = await fetch(uri)
    if body is None:
        body = b""
    assert response.body == body
    assert response.code == status


@pytest.mark.gen_test
@pytest.mark.parametrize("status", [105])
async def test_returns_400_on_bad_post(fetch, status):
    response = await fetch(f"/asdf?status={status}", method="POST")
    assert response.code == 400


@pytest.mark.gen_test
async def test_can_delay_response(fetch):
    await fetch("/asdf?delay=0.2", method="POST", body=b"123")
    t0 = time.time()
    await fetch("/asdf")
    time_taken = time.time() - t0
    assert time_taken >= 0.2
    assert time_taken < 0.25
