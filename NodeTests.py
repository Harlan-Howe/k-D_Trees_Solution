import unittest

from PointNodeFile import PointNode
from SplitterNodeFile import SplitterNode, NUM_POINTS_FOR_MEDIAN


class MyTestCase(unittest.TestCase):

    def setUp(self):

        self.node_0 = SplitterNode(0)
        self.node_1 = SplitterNode(1)
        self.node_3 = SplitterNode(3)
        self.val_set_A = {(29.0, 27.0), (70.0, 74.0), (16.0, 93.0), (30.0, 61.0), (47.0, 0.0), (38.0, 2.0), (84.0, 54.0),
                     (1.0, 96.0), (27.0, 25.0)}

        self.val_set_B = {(0.03, 0.76, 0.91, 0.96, 0.57), (0.93, 0.78, 0.02, 0.94, 0.56), (0.12, 0.88, 0.03, 0.98, 0.89),
                     (0.94, 0.21, 0.0, 0.27, 0.11), (0.57, 0.5, 0.39, 0.01, 0.7), (0.23, 0.01, 0.4, 0.56, 0.67),
                     (0.97, 0.26, 0.7, 0.45, 0.18), (0.34, 0.62, 0.86, 0.62, 0.83), (0.36, 0.85, 0.08, 0.0, 0.86),
                     (0.72, 0.62, 0.22, 0.7, 0.25), (0.44, 0.73, 0.8, 0.46, 0.82), (0.69, 0.1, 0.88, 0.05, 0.34),
                     (0.64, 0.26, 0.76, 0.64, 0.27), (0.96, 0.42, 0.35, 0.63, 0.16), (0.26, 0.72, 0.84, 0.64, 0.46),
                     (0.19, 0.08, 0.54, 0.18, 0.7), (0.21, 0.39, 0.37, 0.33, 0.08), (0.65, 0.24, 0.41, 0.86, 0.89)}

        self.assertLess(18, NUM_POINTS_FOR_MEDIAN, "Because of the randomness of the sampling, this test will only "
                                                   "work if SplitterNode's NUM_POINTS_FOR_MEDIAN is greater "
                                                   "than 18. This doesn't mean your code is broken... just increase "
                                                   "the constant.")

    def test_find_median(self):

        self.assertEqual(30.0, self.node_0.get_median_value(self.val_set_A))
        self.assertEqual(0.57, self.node_0.get_median_value(self.val_set_B))
        self.assertEqual(54.0, self.node_1.get_median_value(self.val_set_A))
        self.assertEqual(0.50, self.node_1.get_median_value(self.val_set_B))
        self.assertEqual(0.62, self.node_3.get_median_value(self.val_set_B))

    def test_split_dataset_A(self):
        threshold, left_set, right_set = self.node_0.split_data(self.val_set_A)
        self.assertEqual(30.0, threshold)
        # because the median value might get thrown into the left or right set, there are two correct cases.
        self.assertTrue(({(1.0, 96.0), (29.0, 27.0), (16.0, 93.0), (27.0, 25.0)} == left_set and
                         {(70.0, 74.0), (30.0, 61.0), (47.0, 0.0), (38.0, 2.0), (84.0, 54.0)} == right_set)
                        or
                        ({(29.0, 27.0), (16.0, 93.0), (30.0, 61.0), (1.0, 96.0), (27.0, 25.0)} == left_set and
                         {(47.0, 0.0), (38.0, 2.0), (84.0, 54.0), (70.0, 74.0)} == right_set))

    def test_split_dataset_B(self):

        threshold, left_set, right_set = self.node_1.split_data(self.val_set_A)
        self.assertEqual(54.0, threshold)
        # because the median value might get thrown into the left or right set, there are two correct cases.
        self.assertTrue(({(29.0, 27.0), (47.0, 0.0), (38.0, 2.0), (84.0, 54.0), (27.0, 25.0)} == left_set and
                         {(1.0, 96.0), (16.0, 93.0), (30.0, 61.0), (70.0, 74.0)} == right_set)
                        or
                        ({(47.0, 0.0), (27.0, 25.0), (29.0, 27.0), (38.0, 2.0)} == left_set and
                        {(70.0, 74.0), (16.0, 93.0), (30.0, 61.0), (84.0, 54.0), (1.0, 96.0)} == right_set))

    def test_split_dataset_C(self):
        threshold, left_set, right_set = self.node_3.split_data(self.val_set_B)
        print(f"{threshold=}\n{left_set=}\n{right_set=}")
        self.assertEqual(0.62, threshold)
        # because the median value might get thrown into the left or right set, there are two correct cases.
        self.assertTrue(({(0.57, 0.5, 0.39, 0.01, 0.7), (0.23, 0.01, 0.4, 0.56, 0.67), (0.97, 0.26, 0.7, 0.45, 0.18),
                          (0.34, 0.62, 0.86, 0.62, 0.83), (0.36, 0.85, 0.08, 0.0, 0.86), (0.44, 0.73, 0.8, 0.46, 0.82),
                          (0.69, 0.1, 0.88, 0.05, 0.34), (0.19, 0.08, 0.54, 0.18, 0.7), (0.21, 0.39, 0.37, 0.33, 0.08),
                          (0.94, 0.21, 0.0, 0.27, 0.11)} == left_set and
                         {(0.03, 0.76, 0.91, 0.96, 0.57), (0.93, 0.78, 0.02, 0.94, 0.56),
                          (0.65, 0.24, 0.41, 0.86, 0.89), (0.72, 0.62, 0.22, 0.7, 0.25),
                          (0.64, 0.26, 0.76, 0.64, 0.27), (0.96, 0.42, 0.35, 0.63, 0.16),
                          (0.12, 0.88, 0.03, 0.98, 0.89), (0.26, 0.72, 0.84, 0.64, 0.46)} == right_set)
                        or
                        ({(0.57, 0.5, 0.39, 0.01, 0.7), (0.23, 0.01, 0.4, 0.56, 0.67), (0.97, 0.26, 0.7, 0.45, 0.18),
                          (0.36, 0.85, 0.08, 0.0, 0.86), (0.44, 0.73, 0.8, 0.46, 0.82), (0.69, 0.1, 0.88, 0.05, 0.34),
                          (0.19, 0.08, 0.54, 0.18, 0.7), (0.21, 0.39, 0.37, 0.33, 0.08),
                          (0.94, 0.21, 0.0, 0.27, 0.11)} == left_set and
                         {(0.93, 0.78, 0.02, 0.94, 0.56), (0.03, 0.76, 0.91, 0.96, 0.57),
                          (0.65, 0.24, 0.41, 0.86, 0.89), (0.34, 0.62, 0.86, 0.62, 0.83),
                          (0.72, 0.62, 0.22, 0.7, 0.25), (0.64, 0.26, 0.76, 0.64, 0.27),
                          (0.96, 0.42, 0.35, 0.63, 0.16), (0.12, 0.88, 0.03, 0.98, 0.89),
                          (0.26, 0.72, 0.84, 0.64, 0.46)} == right_set))

    def test_PointNode_find_nearest_A(self):
        ptn_0 = PointNode((45.0, 83.0))
        target_1 = (44.0, 66.0)
        target_2 = (18.0, 51.0)

        val, dist = ptn_0.find_nearest(target_1, None, float('inf'))
        self.assertEqual((45.0, 83.0), val)
        self.assertAlmostEqual(17.03, dist, places=2)

        val, dist = ptn_0.find_nearest(target_2, None, float('inf'))
        self.assertEqual((45.0, 83.0), val)
        self.assertAlmostEqual(41.87, dist, places=2)

        val, dist = ptn_0.find_nearest(target_1, target_2, 41.87)
        self.assertEqual((45.0, 83.0), val)
        self.assertAlmostEqual(17.03, dist, places=2)

        val, dist = ptn_0.find_nearest(target_2, target_1, 17.03)
        self.assertIsNone(val)
        self.assertIsNone(dist)

    def test_PointNode_find_nearest_B(self):
        ptn_0 = PointNode((45.0, 83.0, 18.0, 23.0))
        target_1 = (44.0, 66.0, 22.0, 34.0)
        target_2 = (18.0, 51.0, 25.0, 23.0)

        val, dist = ptn_0.find_nearest(target_1, None, float('inf'))
        self.assertEqual((45.0, 83.0, 18.0, 23.0), val)
        self.assertAlmostEqual(20.66, dist, places=2)

        val, dist = ptn_0.find_nearest(target_2, None, float('inf'))
        self.assertEqual((45.0, 83.0, 18.0, 23.0), val)
        self.assertAlmostEqual(42.45, dist, places=2)

        val, dist = ptn_0.find_nearest(target_1, target_2, 42.45)
        self.assertEqual((45.0, 83.0, 18.0, 23.0), val)
        self.assertAlmostEqual(20.66, dist, places=2)

        val, dist = ptn_0.find_nearest(target_2, target_1, 20.66)
        self.assertIsNone(val)
        self.assertIsNone(dist)

        print(f"{val=}\t{dist=}")

if __name__ == '__main__':
    unittest.main()
