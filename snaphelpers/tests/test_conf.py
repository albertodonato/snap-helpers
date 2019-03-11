import pytest

from .._conf import (
    InvalidKey,
    SnapConfig,
    SnapConfigOptions,
    UnknownConfigKey,
)


class TestSnapConfigOptions:

    def test_fetch(self, snap_config, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        options.fetch()
        assert options._config == {
            'foo': 123,
            'baz': {
                'aaa': 'nested',
                'bbb': {
                    'ccc': 'more nested'
                }
            }
        }

    def test_as_dict(self, snap_config, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        options.fetch()
        options.as_dict() == snap_config

    def test_as_dict_not_fetched(self, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        options.as_dict() == {}

    @pytest.mark.parametrize(
        'key,value', [
            ('foo', 123), ('baz.aaa', 'nested'),
            ('baz.bbb.ccc', 'more nested'), ('blah', [1, 2, 3])
        ])
    def test_getitem(self, key, value, fake_snapctl):
        options = SnapConfigOptions(
            ['foo', 'baz', 'blah'], snapctl=fake_snapctl)
        options.fetch()
        assert options[key] == value

    @pytest.mark.parametrize('key', ['unknown', 'baz.unknown'])
    def test_getitem_notfound(self, key, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        options.fetch()
        with pytest.raises(UnknownConfigKey) as e:
            options[key]
        assert e.value.key == key

    def test_getitem_not_fetched(self, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        with pytest.raises(UnknownConfigKey):
            options['foo']

    @pytest.mark.parametrize(
        'key,contained', [
            ('foo', True), ('nope', False), ('baz.bbb', True),
            ('baz.nope', False), ('baz.bbb.ccc', True),
            ('baz.bbb.nope', False)
        ])
    def test_in(self, key, contained, fake_snapctl):
        options = SnapConfigOptions(['foo', 'baz'], snapctl=fake_snapctl)
        options.fetch()
        assert (key in options) == contained

    @pytest.mark.parametrize(
        'key,value', [
            ('foo', 123), ('baz.aaa', 'nested'),
            ('baz.bbb.ccc', 'more nested'), ('blah', [1, 2, 3])
        ])
    def test_get(self, key, value, fake_snapctl):
        options = SnapConfigOptions(
            ['foo', 'baz', 'blah'], snapctl=fake_snapctl)
        options.fetch()
        assert options.get(key, None) == value

    def test_get_default(self, fake_snapctl):
        options = SnapConfigOptions(
            ['foo', 'baz', 'blah'], snapctl=fake_snapctl)
        options.fetch()
        assert options.get('something.else', 'this') == 'this'


class TestSnapConfig:

    @pytest.mark.parametrize(
        'key,value', [
            ('foo', 123), ('baz.aaa', 'nested'),
            ('baz.bbb.ccc', 'more nested'), ('blah', [1, 2, 3])
        ])
    def test_config_get(self, key, value, fake_snapctl):
        config = SnapConfig(snapctl=fake_snapctl)
        assert config.get(key) == value

    @pytest.mark.parametrize(
        'key', ['not-here', 'foo.not-here', 'baz.aaa.not-here'])
    def test_config_get_not_found(self, key, fake_snapctl):
        config = SnapConfig(snapctl=fake_snapctl)
        with pytest.raises(UnknownConfigKey):
            config.get(key)

    @pytest.mark.parametrize(
        'key,value', [
            ('foo', 123), ('baz.aaa', 'nested'),
            ('baz.bbb.ccc', 'more nested'), ('blah', [1, 2, 3])
        ])
    def test_get_options(self, key, value, fake_snapctl):
        config = SnapConfig(snapctl=fake_snapctl)
        options = config.get_options('foo', 'baz', 'blah')
        assert options[key] == value

    def test_get_options_only_top_level(self, fake_snapctl):
        config = SnapConfig(snapctl=fake_snapctl)
        with pytest.raises(InvalidKey) as e:
            config.get_options('foo', 'baz.bar')
        assert e.value.key == 'baz.bar'

    def test_set(self, fake_snapctl):
        config = SnapConfig(snapctl=fake_snapctl)
        config.set({'one': 1, 'two': {'three': 3}})
        assert fake_snapctl._configs['one'] == 1
        assert fake_snapctl._configs['two'] == {'three': 3}
        options = config.get_options('one', 'two')
        assert options.as_dict() == {'one': 1, 'two': {'three': 3}}
