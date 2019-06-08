import pytest
import tasks
from tasks import Task


def test_add_raises():
    """
    add() should raise an exception
    :return: None
    """
    with pytest.raises(TypeError):
        tasks.add(task='not a task object')


def test_start_tasks_db_raises():
    with pytest.raises(ValueError) as excinfo:
        tasks.start_tasks_db('whatever/path/', 'not_supported_db')
        exception_msg = excinfo.value.args[0]
        assert exception_msg ==  "db_type must be a 'tiny' or 'mongo'"


@pytest.mark.smoke
def test_list_tasks_raises():
    with pytest.raises(TypeError):
        tasks.list_tasks(owner=123)


@pytest.mark.get
@pytest.mark.smoke
def test_get_raises():
    with pytest.raises(TypeError):
        tasks.get('123')


def test_add_returns_valid_id():
    new_task = Task('do something')
    task_id = tasks.add(new_task)
    assert isinstance(task_id, int)


@pytest.mark.smoke
def test_added_task_has_id_set():
    new_task = Task('sit in chair', owner='me', done=True)
    task_id = tasks.add(new_task)
    task_from_db = tasks.get(task_id)
    assert task_from_db.id == task_id


@pytest.fixture(autouse=True)
def initialized_tasks_db(tmpdir):
    tasks.start_tasks_db(str(tmpdir), 'tiny')
    yield

    # teardown = stop db
    tasks.stop_tasks_db()


@pytest.mark.skipif(tasks.__version__ < '0.2.0',
                    reason='not implented until version 0.2.0')
def test_unique_id_1():
    id_1 = tasks.unique_id()
    id_2 = tasks.unique_id()
    assert id_1 != id_2


def test_unique_id_2():
    ids = []
    ids.append(tasks.add(Task('one')))
    ids.append(tasks.add(Task('two')))
    ids.append(tasks.add(Task('three')))
    uid = tasks.unique_id()
    assert uid not in ids


@pytest.mark.xfail(reason='Demonstrate pytest.mark.xfail')
def test_unique_id_is_a_duck():
    uid = tasks.unique_id()
    assert uid == 'a duck'


@pytest.mark.xfail(reason='This actually will not fail')
def test_unique_id_is_not_a_duck():
    uid = tasks.unique_id()
    assert uid != 'a duck'


def test_add_1():
    t = Task('breathe', 'Brian', True)
    t_id = tasks.add(t)
    t_from_db = tasks.get(t_id)
    assert equivalent(t, t_from_db)


@pytest.mark.parametrize('task',[
    Task('sleep', done=True),
    Task('wake', 'Brian'),
    Task('breathe', 'BrIaN', True),
    Task('exercise', 'Brian', False)
])
def test_add_2(task):
    t = Task('breathe', 'Brian', True)
    t_id = tasks.add(t)
    t_from_db = tasks.get(t_id)
    assert equivalent(t, t_from_db)


@pytest.mark.parametrize('summary, owner, done', [
    ('sleep', 'Brian', True),
    ('wake', 'Brian', False),
    ('breathe', 'BrIaN', True),
    ('exercise', 'Brian', False)
])
def test_add_3(summary, owner, done):
    t = Task(summary, owner, done)
    t_id = tasks.add(t)
    t_from_db = tasks.get(t_id)
    assert equivalent(t, t_from_db)


def equivalent(t1, t2):
    """
    Tasks are equivalent if all their attributes match but id
    :param t1: Task
    :param t2: Task
    :return: Bool
    """
    return t1.summary == t2.summary and \
        t1.owner == t2.owner and \
        t1.done == t2.done
