class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self, head) -> None:
        self.head = head
        self.cur = None

    # Define Iterator
    def __iter__(self):
        self.cur = self.head
        return self

    # Iterate
    def __next__(self):
        if self.cur:
            # Get value of current pointer
            val = self.cur.val
            # Shift the current pointer
            self.cur = self.cur.next
            return val
        else:
            raise StopIteration


head = ListNode(1)

head.next = ListNode(2)

head.next.next = ListNode(3)
myList = LinkedList(head)

for n in myList:
    print(n)
