# test_Classifier.py

import os
import shutil
import arrow
import classifier.classifier as clf
import pytest

__location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__), '.unittest'))

__tmp_files = [u'test_file', u'test_file_中文']
__tmp_dirs = [u'test_dir', u'test_dir_中文']


def setup_module():
    if not os.path.exists(__location):
        os.mkdir(__location)
    os.chdir(__location)
    for file_ in __tmp_files:
        open(file_, 'w').close()
    for dir_ in __tmp_dirs:
        if not os.path.exists(dir_):
            os.mkdir(dir_)


def teardown_module():
    shutil.rmtree(__location)


def test_moveto():
    target_dir = os.path.abspath(os.path.join(__location, 'moveto'))
    for file_ in __tmp_files:
        clf.moveto(file_, __location, target_dir)

    for file_ in __tmp_files:
        final_file_path = os.path.join(target_dir, file_)
        assert os.path.exists(final_file_path)


def test_classify_bydate():
    date_format = 'YYYY-MM-DD'
    target_files = []
    for file_ in __tmp_files:
        target_dir = arrow.get(os.path.getctime(file_)).format(date_format)
        final_file_path = os.path.join(target_dir, file_)
        target_files.append(final_file_path)
    clf.classify_by_date(date_format, __location)
    for file_ in target_files:
        assert os.path.exists(file_)
    for dir_ in __tmp_dirs:
        assert os.path.exists(dir_)

if __name__ == '__main__':
    pytest.main()
