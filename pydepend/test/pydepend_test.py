#!/usr/bin/env python
from pydepend import Dependency, CyclicDependencyError

import inspect
try:
    import unittest2 as unittest
except ImportError:
    import unittest


class DependencyTest(unittest.TestCase):
    def test_ordered_deps(self):
        a = Dependency('a')
        b = Dependency('b')
        c_obj = object()
        c = Dependency(c_obj)
        d = Dependency('d')
        e = Dependency('e')

        a.depends_on(b)
        b.depends_on(d)
        c.depends_on(d)
        a.depends_on(c)
        e.depends_on(d)

        self.assertEquals(a.ordered_deps, (d, b, c))
        self.assertEquals(e.ordered_deps, (d,))

    def test_ordered_deps_with_no_dependencies(self):
        a = Dependency('a')
        self.assertEquals(a.ordered_deps, tuple())

    def test_ordered_deps_cache_invalidation(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on(b)
        self.assertEquals(a.ordered_deps, (b,))

        a.depends_on(c)
        self.assertEquals(a.ordered_deps, (b, c))

    def test_direct_deps(self):
        a = Dependency('a')
        b = Dependency('b')
        c_obj = object()
        c = Dependency(c_obj)
        d = Dependency('d')

        a.depends_on(b)
        b.depends_on(d)
        c.depends_on(d)
        a.depends_on(c)

        self.assertEquals(a.direct_deps, (b, c))
        self.assertEquals(b.direct_deps, (d,))

    def test_direct_deps_with_no_dependencies(self):
        a = Dependency('a')
        self.assertEquals(a.direct_deps, tuple())

    def test__lt__indicates_dependency_order(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on(b)
        b.depends_on(c)

        self.assertTrue(a < b)
        self.assertTrue(a < c)
        self.assertFalse(c < a)
        self.assertFalse(a < a)

    def test__gt__indicates_dependency_order(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on(b)
        b.depends_on(c)

        self.assertFalse(a > b)
        self.assertFalse(a > c)
        self.assertTrue(c > a)
        self.assertFalse(a > a)

    def test__eq__(self):
        a = Dependency('a')
        b = Dependency('b')

        self.assertEqual(a, a)
        self.assertNotEqual(a, b)

        class SomeClass(object):
            pass

        obj1 = SomeClass()
        obj2 = SomeClass()
        x = Dependency(obj1)
        y = Dependency(obj1)
        z = Dependency(obj2)

        self.assertEqual(x, y)
        self.assertNotEqual(x, z)

    def test__iter__generates_ordered_deps(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on([b, c])

        iterator = a.__iter__()
        self.assertTrue(inspect.isgenerator(iterator))
        self.assertIs(iterator.next(), b)
        self.assertIs(iterator.next(), c)

    def test__contains__tests_ordered_deps(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on([b, c])

        a.depends_on([b, c])
        self.assertIn(b, a)
        self.assertIn(c, a)
        self.assertNotIn(a, a)

    def test__len__measures_ordered_deps(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on([b, c])

        self.assertEquals(len(a), 2)

    def test_raises_on_cyclic_dependencies(self):
        a = Dependency('a')
        b = Dependency('b')
        c = Dependency('c')

        a.depends_on(b)
        b.depends_on(c)
        c.depends_on(a)

        self.assertRaises(CyclicDependencyError, lambda: a.ordered_deps)
