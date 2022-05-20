import collections
import unittest


class SearchEngine:
    def __init__(self, docs):
        # word: doc_id
        self.inverted_index = collections.defaultdict(list)
        for doc_id, content in docs:
            words = content.split()
            for word in words:
                self.inverted_index[word].append(doc_id)

    def search_word(self, word):
        if word not in self.inverted_index:
            raise Exception("word not exist")
        return self.inverted_index[word]

    def search_phrase(self, phrase):
        doc_lists = []
        for word in phrase.split():
            doc_ids = self.search_word(word)
            doc_lists.append(doc_ids)
        # doc ids are sorted
        return self.intersect_sorted_lists(doc_lists)

    def intersect_sorted_lists(self, lists):
        def intersect_two_lists(l1, l2):
            i, j = 0, 0
            res = []
            while i < len(l1) and j < len(l2):
                if l1[i] == l2[j]:
                    res.append(l1[i])
                    i += 1
                    j += 1
                elif l1[i] < l2[j]:
                    i += 1
                else:
                    j += 1
            return res

        res = lists[0]
        for l in lists[1:]:
            res = intersect_two_lists(res, l)

        return res

    def intersect_sorted_lists_optimized(self, lists):
        def intersect_two_sorted_lists_in_place(l1, l1_len, l2):
            i, j = 0, 0
            k = 0
            while i < l1_len and j < len(l2):
                if l1[i] == l2[j]:
                    l1[k] = l1[i]
                    i += 1
                    j += 1
                    k += 1
                elif l1[i] < l2[j]:
                    i += 1
                else:
                    j += 1
            return k

        def find_shortest_list(lists):
            min_len = len(lists[0])
            shortest_list = lists[0]
            shortest_list_idx = -1

            for i, list in enumerate(lists):
                if len(list) < min_len:
                    min_len = len(list)
                    shortest_list = list
                    shortest_list_idx = i

            return shortest_list, shortest_list_idx

        shortest, shortest_idx = find_shortest_list(lists)

        # O(1) delete shortest list
        lists[shortest_idx], lists[-1] = lists[-1], lists[shortest_idx]
        lists.pop()

        res = shortest
        res_len = len(shortest)

        for l in lists:
            # res_len limit the space
            # 规定了intersect的最大区间
            res_len = intersect_two_sorted_lists_in_place(res, res_len, l)

        return res[:res_len]


class MyTestCase(unittest.TestCase):
    def test_search_phrase(self):
        se = SearchEngine([
            [1, "cloud search"],
            [2, "cloud computing is awesome"],
            [3, "computing cloud is great as well"]
        ])

        self.assertEqual(se.search_word("cloud"), [1, 2, 3])
        self.assertEqual(se.search_phrase("cloud computing is"), [2, 3])




