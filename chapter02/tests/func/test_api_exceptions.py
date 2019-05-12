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
