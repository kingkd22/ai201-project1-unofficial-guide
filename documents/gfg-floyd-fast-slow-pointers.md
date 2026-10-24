Title: How does Floyd's slow and fast pointers approach work? - GeeksforGeeks
Source: https://www.geeksforgeeks.org/dsa/how-does-floyds-slow-and-fast-pointers-approach-work/

---

We have discussed Floyd's fast and slow pointer algorithms in Detect loop in a linked list. The algorithm is to start two pointers slow and fast from the head of the linked list. We move slow one node at a time and fast two nodes at a time. If there is a loop, then they will definitely meet.

This approach works because of the following facts :

- When slow pointer enters the loop, the fast pointer must be inside the loop.
- if we consider movements of slow and fast pointers, we can notice that distance between them (from slow to fast) increase by one after every iteration.

After each iteration where the slow pointer moves one step forward and the fast pointer moves two steps forward, the distance between the two pointers increases. Initially, if the slow pointer is at a distance k from a certain point in the cycle, then after one iteration, the distance between the slow and fast pointers becomes k+1. After two iterations, this distance becomes k+2 and so on. As they continue to move within the cycle, this distance will eventually equal the cycle length n. At this point, since the distance wraps around the cycle and both pointers are moving within the same cycle, they will meet.

Let slow and fast meet at some point after Floyd's Cycle finding algorithm. The below diagram shows the situation when the cycle is found.

We can conclude below from the above diagram:

Distance travelled by fast pointer = 2 * (Distance travelled by slow pointer)

- (m + n*x + k) = 2*(m + n*y + k) , Note that before the meeting point shown above, fast was moving at twice speed.

- x = Number of complete cyclic rounds made by fast pointer before they meet first time.
- y = Number of complete cyclic rounds made by slow pointer before they meet first time.

From the above equation, we can conclude below :

- m + k = (x - 2y)*n, which means m + k is a multiple of n. Thus we can write, m + k = i*n or m = i*n - k where i : number of times the fast pointer has completed a full cycle before meeting the slow pointer.

When the slow pointer and the fast pointer meet, the fast pointer has traveled a distance that is a multiple of the cycle length plus some extra distance. Specifically, the distance covered by the fast pointer is i * n - k, where:

- (i * n) represents the distance covered by the fast pointer in completing i full cycles.
- (- k) represents the extra distance it has traveled within the cycle before meeting the slow pointer.

The slow pointer, on the other hand, has traveled a distance m where m is exactly k plus one complete cycle if i is greater than 1. When the fast pointer completes i-1 full cycles, it travels (i-1) * n distance. To cover the remaining distance in the cycle, the fast pointer needs to travel an additional n - k to meet the slow pointer.

Therefore ,The total distance covered by the slow pointer can be expressed as:

- m = (i-1)*n + (n-k), Here (i-1) * n covers the complete cycles before the final partial cycle, and n - k covers the remaining distance to the meeting point.

Finding the Start of the Cycle

Once the slow and fast pointers meet within the loop, the next step is to identify the start of the cycle. To do this, we reset one of the pointers - let’s say the slow pointer to the head of the linked list. The other pointer, the fast pointer, remains at the point where the two pointers initially met. Both pointers are then moved one node at a time. As they traverse the list, the pointer that was reset to the head will cover the distance m to the start of the loop. Since the total distance m + k covered by the slow pointer is a multiple of the cycle length n, both pointers will eventually converge at the start of the cycle. This simultaneous movement ensures that the pointer starting from the head meets the pointer at the start of the cycle, there by successfully identifying the beginning of the loop.

Floyd’s Cycle-Finding Algorithm is efficient in detecting loops in a linked list with a time complexity O(n) and space complexity of O(1).

Please refer to Find Starting node of cycle for more details.
