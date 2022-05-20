import unittest


def is_multi_match(s, p):
    """
    multi stars
    :param s:
    :param p:
    :return:
    """
    def all_stars(p, j):
        for c in set(p[j:]):
            if c != '*':
                return False
        return True

    def dfs(s, p, i, j):
        if i == len(s):
            return all_stars(p, j)

        if j == len(p):  # i != len(s)
            return False

        # cur level
        if p[j] == '*':
            # use * to cover 1 char in s or 0 char
            is_match = dfs(s, p, i + 1, j) or dfs(s, p, i, j + 1)
        else:
            is_match = (s[i] == p[j] and dfs(s, p, i + 1, j + 1))

        return is_match

    return dfs(s, p, i=0, j=0)


class MyTestCase(unittest.TestCase):
    def test_is_multi_match(self):
        s = "abbbbbbcccccsd"
        p = "ab*bbc*sd"
        self.assertEqual(is_multi_match(s, p), True)

