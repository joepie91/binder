
import unittest

from binder.api import *

from bindertest.testdbconfig import connect
from bindertest.tabledefs import Foo, Bar


foo1 = Foo.new(foo_id=1, i1=101, s1="alpha")
foo2 = Foo.new(foo_id=2, i1=101, s1="beta")


class ConnGetTest(unittest.TestCase):

    def setUp(self):
        conn = connect()
        try:
            conn.drop_table(Foo)
        except conn.DbError, e:
            self.assertEquals("no such table: foo", str(e))
        conn = connect()
        conn.create_table(Foo)
        conn.commit()
        conn = connect()
        conn.insert(Foo, foo1)
        conn.insert(Foo, foo2)
        conn.commit()

    def test_get(self):
        conn = connect()
        self.assertEquals(foo1, conn.get(Foo, 1))
        self.assertEquals(foo2, conn.get(Foo, 2))
        self.assertEquals(None, conn.get(Foo, 3))

    def test_get_more_than_one_row(self):
        conn = connect()
        Foo2 = Table("foo", AutoIdCol("i1"), IntCol("foo_id"))
        try:
            conn.get(Foo2, 101)
        except AssertionError, e:
            msg, info = e.args
            self.assertEquals("select_one(): more than 1 row", msg)
            table_name, sqlcond = info
            #table_name, sqlcond, rc = info
            self.assertEquals("foo", table_name)
            self.assertEquals('"i1 = 101"', repr(sqlcond))
            #self.assertEquals(2, rc)
        else:
            self.fail()

    def test_no_auto_id_col(self):
        conn = connect()
        try:
            conn.get(Bar, 12)
        except AssertionError, e:
            self.assertEquals("get(): table 'bar' does not have AutoIdCol", str(e))
        else:
            self.fail()

    def test_auto_id(self):
        conn = connect()
        try:
            conn.get(Foo, None)
        except AssertionError, e:
            self.assertEquals("get(): cannot use None for AutoIdCol", str(e))
        else:
            self.fail()

    def test_bad_values(self):
        conn = connect()
        try:
            conn.get(Foo, '4')
        except TypeError, e:
            self.assertEquals("AutoIdCol 'foo_id': int expected, got str", str(e))
        else:
            self.fail()




if __name__ == '__main__':
    unittest.main()
