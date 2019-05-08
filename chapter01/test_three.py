from collections import namedtuple

Task = namedtuple('Task', ['summary', 'owner', 'done', 'id'])
Task.__new__.__defaults__ = (None, None, False, None)


def test_defaults():
    """
    Using no parameters should invoke defaults.
    :return: None
    """
    t1 = Task()
    t2 = Task(None, None, False, None)
    assert t1 == t2


def test_access_member():
    """
    Check field functionality.
    :return: None
    """
    t = Task("buy milk", "Brian")
    assert t.summary == "buy milk"
    assert t.owner == "Brian"
    assert (t.done, t.id) == (False, None)


def test_asdict():
    """
    _asdict() should return a dictionary.
    :return: None
    """
    t_task = Task('do something', 'okken', True, 21)
    t_dict = {
        'summary': 'do something',
        'owner': 'okken',
        'done': True,
        'id': 21
    }
    assert t_task._asdict() == t_dict


def test_replace():
    """
    replace() should change passed in fields.
    :return: None
    """
    t_before = Task('finish book', 'brian', False)
    t_after = t_before._replace(id=10, done=True)
    t_expected = Task('finish book', 'brian', True, 10)

    assert t_after == t_expected