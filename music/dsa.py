#Node is a BST node that stores a song ID and has left and right children. 
# BST is a binary search tree that stores song IDs in order of their titles. It has methods to insert, search, delete, and traverse the tree in order. 
# The merge_sort function sorts a list of song IDs by their durations using the merge sort algorithm. 
# The binary_search_duration function performs a binary search on a sorted list of song IDs to find all songs with a given duration.
class Node:
    def __init__(self, song_id):
        self.song_id = song_id
        self.left = None
        self.right = None

class BST:
    def __init__(self, title_for_id):
        self.root = None
        self.title_for_id = title_for_id

    def insert(self, song_id):
        def add(node, song_id):
            if node is None:
                return Node(song_id)
            key = self.title_for_id(song_id).lower()
            current = self.title_for_id(node.song_id).lower()
            if key < current:
                node.left = add(node.left, song_id)
            elif key > current:
                node.right = add(node.right, song_id)
            else:
                raise ValueError('Song title already exists')
            return node
        self.root = add(self.root, song_id)

    def search(self, title):
        node = self.root
        comparisons = 0
        key = title.lower()
        while node is not None:
            comparisons += 1
            current = self.title_for_id(node.song_id).lower()
            if key == current:
                return node.song_id, comparisons
            node = node.left if key < current else node.right
        return None, comparisons

    def delete(self, title):
        def remove(node, key):
            if node is None:
                return None
            current = self.title_for_id(node.song_id).lower()
            if key < current:
                node.left = remove(node.left, key)
            elif key > current:
                node.right = remove(node.right, key)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.song_id = successor.song_id
                node.right = remove(
                    node.right,
                    self.title_for_id(successor.song_id).lower(),
                )
            return node
        self.root = remove(self.root, title.lower())

    def inorder(self):
        output = []
        def visit(node):
            if node:
                visit(node.left)
                output.append(node.song_id)
                visit(node.right)
        visit(self.root)
        return output


def merge_sort(song_ids, duration_for_id):
    """Returns song IDs ordered by duration and the number of comparisons."""
    if len(song_ids) <= 1:
        return song_ids[:], 0
    mid = len(song_ids) // 2
    left, a = merge_sort(song_ids[:mid], duration_for_id)
    right, b = merge_sort(song_ids[mid:], duration_for_id)
    result = []
    i = j = comparisons = 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if duration_for_id(left[i]) <= duration_for_id(right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:], a + b + comparisons


def binary_search_duration(sorted_song_ids, duration, duration_for_id):
    """Binary-search duration-sorted song IDs and return all equal matches."""
    lo, hi = 0, len(sorted_song_ids) - 1
    comparisons = 0
    found = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        value = duration_for_id(sorted_song_ids[mid])
        if value == duration:
            found = mid
            break
        if value < duration:
            lo = mid + 1
        else:
            hi = mid - 1
    if found == -1:
        return [], comparisons
    first = last = found
    while first > 0 and duration_for_id(sorted_song_ids[first - 1]) == duration:
        first -= 1
    while (
        last + 1 < len(sorted_song_ids)
        and duration_for_id(sorted_song_ids[last + 1]) == duration
    ):
        last += 1
    return sorted_song_ids[first:last + 1], comparisons
