from rq import rqSet

__author__ = 'sander'

def test_rq_parser():
    rq_set = rqSet()
    rq_set.parse(b'!ABCv001;')
    assert len(rq_set.nodes) == 1
    assert rq_set.nodes[0].address == b'ABC'

def test_json():
    rq_set = rqSet()
    rq_set.parse(b'!ABCv001;')
    rq_set.save_json()
    assert len(rq_set.nodes) == 1

def test_get_version():
    rq_set = rqSet()
    rq_set.parse(b'!ABCv001;')
    ver = rq_set.nodes[0].get_version()
    assert ver == b'!ABCv?;'
