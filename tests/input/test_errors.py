import pytest

from yadism.input import errors


def test_domain_error():
    with pytest.raises(errors.DomainError):
        raise errors.DomainError(
            name="test",
            description="test_description",
            type=type(3),
            known_as="ciao",
            value=3,
        )
