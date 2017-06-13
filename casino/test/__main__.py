import doctest
import unittest

from .. import roulette
from . import test_roulette

suite = unittest.TestSuite()

# Mix unittests and doctests into the same suite
suite.addTest(doctest.DocTestSuite(roulette))
suite.addTest(unittest.defaultTestLoader.loadTestsFromModule(test_roulette))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
