def bubble_sort(list):
    length = len(list)
    for i in range(length):
        for i in range(length - 1):
            if list[i] > list[i + 1]:
                list[i], list[i + 1] = list[i + 1], list[i]
    return list


def select_sort(list):
    length = len(list)
    for i in range(length):
        min = i
        for j in range(i + 1, length):
            if list[j] < list[min]:
                min = j
        list[min], list[i] = list[i], list[min]
    return list


def insert_sort(list):
    length = len(list)
    for i in range(1, length):
        j = i
        while j > 0 and list[j] < list[j - 1]:
            list[j], list[j - 1] = list[j - 1], list[j]
            j -= 1
    return list


def qsort(list):
    if len(list) <= 1:
        return list
    else:
        init = list[0]
        return qsort([x for x in list[1:] if x < init]) + \
            [init] + qsort([x for x in list[1:] if x >= init])


def merge(left, right):
    result = []
    while len(left) > 0 and len(right) > 0:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    if len(left):
        result += left
    elif len(right):
        result += right
    return result


def merge_sort(lists):
    if len(lists) <= 1:
        return lists
    middles = len(lists) / 2
    left = merge_sort(lists[:middles])
    right = merge_sort(lists[middles:])
    return merge(left, right)


# print(merge_sort([5,6,4,3,2,1]))


# tree
class Node(object):
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


tree = Node(1, Node(3, Node(7, Node(0)), Node(6)), Node(2, Node(5), Node(4)))

#        1
#    3       2
#  7   6    5  4
# 0


def lookup(tree):
    row = [tree]
    while row:
        print([o.data for o in row])
        row = [kid for item in row for kid in (item.left, item.right) if kid]


def deep(tree):
    if not tree:
        return
    print(tree.data)
    deep(tree.left)
    deep(tree.right)


def mid(tree):
    if tree.left:
        mid(tree.left)
    print(tree.data)
    if tree.right:
        mid(tree.right)


def mid2(tree):
    re = []
    stack = []
    while tree or stack:
        while tree:
            stack.append(tree)
            tree = tree.left
        if stack:
            t = stack.pop()
            re.append(t.data)
            tree = t.right
    return re


def pre(tree):
    print(tree.data)
    if tree.left:
        pre(tree.left)
    if tree.right:
        pre(tree.right)


def pre2(tree):
    re = []
    stack = [tree]
    while stack:
        node = stack.pop()
        re.append(node.data)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return re


def pre3(tree):
    re = []
    stack = []
    while tree or stack:
        while tree:
            re.append(tree.data)
            stack.append(tree)
            tree = tree.left
        if stack:
            t = stack.pop()
            tree = t.right
    return re


def aft(tree):
    if tree.left:
        aft(tree.left)
    if tree.right:
        aft(tree.right)
    print(tree.data)



def max_deep(tree):
    if not tree:
        return 0
    return max(max_deep(tree.left), max_deep(tree.right)) + 1


# print(lookup(tree))


#link
class Node(object):
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

link = Node(1, Node(2, Node(3, Node(4, Node(5, Node(6, Node(7, Node(8, Node(9)))))))))

def rev(link):
    pre = link
    cur = link.next
    pre.next = None
    while cur:
        tmp = cur.next
        cur.next = pre
        pre = cur
        cur = tmp
    return pre


