import pytest

from .._conf import (
    SnapConfig,
    UnknownConfig,
)


@pytest.mark.usefixtures('snap_apply_environ')
class TestSnapConfig:

    def test_load(self, snap_config, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        config.load()
        assert config._config == snap_config

    def test_as_dict(self, snap_config, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        config.load()
        config.as_dict() == snap_config

    def test_as_dict_not_loaded(self, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        config.as_dict() == {}

    @pytest.mark.parametrize(
        'key,value', [
            ('foo', 123), ('baz.aaa', 'nested'),
            ('baz.bbb.ccc', 'more nested'), ('blah', [1, 2, 3])
        ])
    def test_getitem(self, key, value, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        config.load()
        assert config[key] == value

    @pytest.mark.parametrize('key', ['unknown', 'baz.unknown'])
    def test_getitem_notfound(self, key, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        config.load()
        with pytest.raises(UnknownConfig):
            config[key]

    def test_getitem_not_loaded(self, snapctl):
        config = SnapConfig(['foo', 'bar'], snapctl=snapctl)
        with pytest.raises(UnknownConfig):
            config['foo']
