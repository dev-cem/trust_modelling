import unittest
import sub_logic

opinion1 = sub_logic.SubLog(True, {'a': 0.5, 'b': 0.2, 'd': 0.3, 'u': 0.5})
opinion2 = sub_logic.SubLog(False, {'a': 0.2, 's': 1, 'r': 3})


class MyTestCase(unittest.TestCase):
    def test_opinion1(self):
        self.assertEqual(opinion1.a, 0.5)
        self.assertEqual(opinion1.b, 0.2)
        self.assertEqual(opinion1.d, 0.3)
        self.assertEqual(opinion1.u, 0.5)
        self.assertEqual(opinion1.s, 1.2)
        self.assertEqual(opinion1.r, 0.8)

    def test_opinion2(self):
        self.assertEqual(opinion2.a, 0.2)
        self.assertEqual(opinion2.b, 0.5)
        self.assertEqual(opinion2.d, 0.16666666666666666)
        self.assertEqual(opinion2.u, 0.33333333333333333)
        self.assertEqual(opinion2.s, 1)
        self.assertEqual(opinion2.r, 3)

    def test_trust(self):
        self.assertEqual(opinion1.trust(), 0.45)

    def test_trust(self):
        self.assertEqual(opinion2.trust(), 0.566667)

    def test_transitivity(self):
        self.assertEqual(opinion1.transitivity(opinion2).a, 0.5)
        self.assertEqual(opinion1.transitivity(opinion2).b, 0.1)
        self.assertEqual(opinion1.transitivity(opinion2).d, 0.03333333333333333)
        self.assertEqual(opinion1.transitivity(opinion2).u, 0.8666666666666667)

    def test_cumulative_fusion(self):
        self.assertEqual(sub_logic.cumulative_fusion(opinion1, opinion2).a, 0.5)
        self.assertEqual(sub_logic.cumulative_fusion(opinion1, opinion2).b, 0.475)
        self.assertEqual(sub_logic.cumulative_fusion(opinion1, opinion2).d, 0.275)
        self.assertEqual(sub_logic.cumulative_fusion(opinion1, opinion2).u, 0.25)


if __name__ == '__main__':
    unittest.main()
