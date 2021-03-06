import time

from cvbase.progress import ProgressBar, track_progress, track_parallel_progress


class TestProgressBar(object):

    def test_start(self, capsys):
        # without total task num
        prog_bar = ProgressBar()
        out, _ = capsys.readouterr()
        assert out == 'completed: 0, elapsed: 0s'
        prog_bar = ProgressBar(start=False)
        out, _ = capsys.readouterr()
        assert out == ''
        prog_bar.start()
        out, _ = capsys.readouterr()
        assert out == 'completed: 0, elapsed: 0s'
        # with total task num
        prog_bar = ProgressBar(10)
        out, _ = capsys.readouterr()
        assert out == '[{}] 0/10, elapsed: 0s, ETA:'.format(' ' * 50)
        prog_bar = ProgressBar(10, start=False)
        out, _ = capsys.readouterr()
        assert out == ''
        prog_bar.start()
        out, _ = capsys.readouterr()
        assert out == '[{}] 0/10, elapsed: 0s, ETA:'.format(' ' * 50)

    def test_update(self, capsys):
        # without total task num
        prog_bar = ProgressBar()
        capsys.readouterr()
        time.sleep(1)
        prog_bar.update()
        out, _ = capsys.readouterr()
        assert out == 'completed: 1, elapsed: 1s, 1.0 tasks/s'
        # with total task num
        prog_bar = ProgressBar(10)
        capsys.readouterr()
        time.sleep(1)
        prog_bar.update()
        out, _ = capsys.readouterr()
        assert out == ('\r[{}] 1/10, 1.0 task/s, elapsed: 1s, ETA:     9s'.
                       format('>' * 5 + ' ' * 45))


def sleep_1s(num):
    time.sleep(1)
    return num


def test_track_progress_list(capsys):

    ret = track_progress(sleep_1s, [1, 2, 3], bar_width=3)
    out, _ = capsys.readouterr()
    assert out == ('[   ] 0/3, elapsed: 0s, ETA:'
                   '\r[>  ] 1/3, 1.0 task/s, elapsed: 1s, ETA:     2s'
                   '\r[>> ] 2/3, 1.0 task/s, elapsed: 2s, ETA:     1s'
                   '\r[>>>] 3/3, 1.0 task/s, elapsed: 3s, ETA:     0s\n')
    assert ret == [1, 2, 3]


def test_track_progress_iterator(capsys):

    ret = track_progress(sleep_1s, ((i for i in [1, 2, 3]), 3), bar_width=3)
    out, _ = capsys.readouterr()
    assert out == ('[   ] 0/3, elapsed: 0s, ETA:'
                   '\r[>  ] 1/3, 1.0 task/s, elapsed: 1s, ETA:     2s'
                   '\r[>> ] 2/3, 1.0 task/s, elapsed: 2s, ETA:     1s'
                   '\r[>>>] 3/3, 1.0 task/s, elapsed: 3s, ETA:     0s\n')
    assert ret == [1, 2, 3]


def test_track_parallel_progress_list(capsys):

    results = track_parallel_progress(sleep_1s, [1, 2, 3, 4], 2, bar_width=4)
    out, _ = capsys.readouterr()
    assert out == ('[    ] 0/4, elapsed: 0s, ETA:'
                   '\r[>   ] 1/4, 1.0 task/s, elapsed: 1s, ETA:     3s'
                   '\r[>>  ] 2/4, 2.0 task/s, elapsed: 1s, ETA:     1s'
                   '\r[>>> ] 3/4, 1.5 task/s, elapsed: 2s, ETA:     1s'
                   '\r[>>>>] 4/4, 2.0 task/s, elapsed: 2s, ETA:     0s\n')
    assert results == [1, 2, 3, 4]


def test_track_parallel_progress_iterator(capsys):

    results = track_parallel_progress(
        sleep_1s, ((i for i in [1, 2, 3, 4]), 4), 2, bar_width=4)
    out, _ = capsys.readouterr()
    assert out == ('[    ] 0/4, elapsed: 0s, ETA:'
                   '\r[>   ] 1/4, 1.0 task/s, elapsed: 1s, ETA:     3s'
                   '\r[>>  ] 2/4, 2.0 task/s, elapsed: 1s, ETA:     1s'
                   '\r[>>> ] 3/4, 1.5 task/s, elapsed: 2s, ETA:     1s'
                   '\r[>>>>] 4/4, 2.0 task/s, elapsed: 2s, ETA:     0s\n')
    assert results == [1, 2, 3, 4]
