Title: N-Base modified Binary Search algorithm - GeeksforGeeks
Source: https://www.geeksforgeeks.org/dsa/n-base-modified-binary-search-algorithm/

---

N-Base modified Binary Search is an algorithm based on number bases that can be used to find an element in a sorted array arr[]. This algorithm is an extension of Bitwise binary search and has a similar running time.

Examples:

Input: arr[] = {1, 4, 5, 8, 11, 15, 21, 45, 70, 100}, target = 45
Output: 7
Explanation: The value 45 is present at index 7

Input: arr[] = {1, 6, 8, 10}, target = 9
Output: -1
Explanation: The value 9 is not present in the given array.

Intuition: All numbers of a number system can be expressed in another number systems having any number (e.g. 2, 3, 7) as base of that number system. For example, 7 of decimal number system can be expressed as (21)3 in a number system having base as 3. Therefore the concept of bitwise binary search can be implemented using any number N as base of a number system.

Approach: The index for the target element is searched by adding powers of base (any positive integer starting from 2) to a sum (initially 0). When such a power is found, calculation is made to count the number of times it can be used to find the target index, and that value is added with the sum. The part of counting how many times a power can be used is similar to the "Bitwise binary search" from the binary search article.

- Define a base number, and a power of two greater or equal to the base (the power of two will help in counting how many times a power of base can be added to final index, efficiently)
- Compute the first power of the base (N) that is greater than the array size. ( Nk where k is an integer greater or equal to one and Xk is the first power of base greater or equal to the array size).
- Initialize an index (finId) as 0 which will store the final position where the target element should be at the end of all the iterations.
- Loop while computed power is greater than 0 and each time divide it by base value.

- Check how many times this power can be used and add that value to the finId.
- To check this, use the conditions mentioned below:

- finId + power of base < array size(M)
- value at finId + power of base ≤ target

While iteration is complete check if the value at final index is same as target or not. If it is not, then the value is not present in the array.

Illustration: See the illustration below for better understanding.

Illustration: arr[] = {1, 4, 5, 8, 11, 15, 21, 45, 70, 100}, array size(M) = 10, target = 45, base(N) = 3

Steps:

- Compute first power(power) of 3 (Base) greater than 10 (M), power = 27 in this case.
- Initialize a final index(finId) as 0 (position in arr[] where target value should be at the end).
- Now iterate through the powers of 3 (Base) that are less or equal to 27 and add them to the index as fallowing:

- 1st iteration : finId = 0. power is 27 and can't be used because finId + power > M. So, finId = 0.
- 2nd iteration : finId = 0. power is 9 and can't be used because element at finId + power > target
i.e. arr[finId + power] > target. So finId = 0.
- 3rd iteration : finId = 0. power is 3, this time power can be used because arr[finId + power] < target. Now count how many times 3 can be added to finId. In this case 3 can sum two times. finId after 3rd iteration will be 6 (finId += 3 + 3). 3 can't be added more than 2 times because finId will pass the index where target value is. So finId = 0 + 3 + 3 = 6.
- 4th iteration : finId = 6. power is 1, power can be used because arr[finId + power] ≤ target(45). Again count how many times 1 can be used. In this case 1 can be used only once. So add 1 only once with finId. So, finId = 6+1 = 7.

- after 4th iteration power is 0 so exit the loop.
- arr[7] = target. So the value is found at index 7.

Notes:

- At each iteration power can be used maximum (Base - 1) times
- Base can be any positive integer starting from 2
- Array needs to be sorted to perform this search algorithm

Below is the implementation of the above approach (in comparison with a classic binary search algorithm):

C++

```
// C++ code to implement the above approach
#include<bits/stdc++.h>
using namespace std;

#define N 3
#define PowerOf2 4

int Numeric_Base_Search(int arr[], int M, 
                        int target){
    unsigned long long i, step1, 
    step2 = PowerOf2, times;

    // Find the first power of N 
    // greater than the array size
    for (step1 = 1; step1 < M; step1 *= N);
    
    for (i = 0; step1; step1 /= N)

        // Each time a power can be used
        // count how many times 
        // it can be used
        if (i + step1 < M && arr[i + step1] 
            <= target){
            for (times = 1; step2; 
                 step2 >>= 1)
                if (i + 
                    (step1 * (times + step2)) 
                    < M && 
                    arr[i + 
                      (step1 * (times + step2))] 
                    <= target)
                    times += step2;

            step2 = PowerOf2;

            // Add to final result 
            // how many times 
            // can the power be used
            i += times * step1;
        }

    // Return the index 
    // if the element is present in array
    // else return -1
    return arr[i] == target ? i : -1;
}

// Driver code
int main(){
    int arr[10] = 
    {1, 4, 5, 8, 11, 15, 21, 45, 70, 100};
    int target = 45, M = 10;
    int answer  = Numeric_Base_Search(arr, M, target);
    cout<<answer;
    return 0;
}
```

Java

```
// Java code to implement the above approach
class GFG {

    static int N = 3;
    static int PowerOf2 = 4;

    static int Numeric_Base_Search(int[] arr, int M,
                                   int target)
    {
        int i, step1, step2 = PowerOf2, times;

        // Find the first power of N
        // greater than the array size
        for (step1 = 1; step1 < M; step1 *= N)
            ;

        for (i = 0; step1 > 0; step1 /= N) {

            // Each time a power can be used
            // count how many times
            // it can be used
            if (i + step1 < M && arr[i + step1] <= target) {
                for (times = 1; step2 > 0; step2 >>= 1)
                    if (i + (step1 * (times + step2)) < M
                        && arr[i
                               + (step1 * (times + step2))]
                               <= target)
                        times += step2;

                step2 = PowerOf2;

                // Add to final result
                // how many times
                // can the power be used
                i += times * step1;
            }
        }
      
        // Return the index
        // if the element is present in array
        // else return -1
        return arr[i] == target ? i : -1;
    }

    // Driver code
    public static void main(String args[])
    {
        int[] arr = { 1, 4, 5, 8, 11, 15, 21, 45, 70, 100 };
        int target = 45, M = 10;
        int answer = Numeric_Base_Search(arr, M, target);
        System.out.println(answer);
    }
}

// This code is contributed by Saurabh Jaiswal
```

Python3

```
# Python code for the above approach
N = 3
PowerOf2 = 4

def Numeric_Base_Search(arr, M, target):
    i = None
    step1 = None
    step2 = PowerOf2
    times = None

    # Find the first power of N
    # greater than the array size
    step1 = 1
    while(step1 < M):
        step1 *= N

    i = 0
    while(step1):
        step1 = step1 // N

        # Each time a power can be used
        # count how many times
        # it can be used
        if (i + step1 < M and arr[i + step1] <= target):
            times=1
            while(step2):
                step2 >>= 1
                if (i + (step1 * (times + step2)) < M and arr[i + (step1 * (times + step2))] <= target):
                    times += step2;

            step2 = PowerOf2;

            # Add to final result
            # how many times
            # can the power be used
            i += times * step1

    # Return the index
    # if the element is present in array
    # else return -1
    return i if arr[i] == target else -1

   # Driver code
arr = [1, 4, 5, 8, 11, 15, 21, 45, 70, 100]
target = 45
M = 10
answer = Numeric_Base_Search(arr, M, target)
print(answer)

  # This code is contributed by Saurabh Jaiswal
```

C#

```
// C# code to implement the above approach
using System;
class GFG {

    static int N = 3;
    static int PowerOf2 = 4;

    static int Numeric_Base_Search(int[] arr, int M,
                                   int target)
    {
        int i, step1, step2 = PowerOf2, times;

        // Find the first power of N
        // greater than the array size
        for (step1 = 1; step1 < M; step1 *= N)
            ;

        for (i = 0; step1 > 0; step1 /= N) {

            // Each time a power can be used
            // count how many times
            // it can be used
            if (i + step1 < M && arr[i + step1] <= target) {
                for (times = 1; step2 > 0; step2 >>= 1)
                    if (i + (step1 * (times + step2)) < M
                        && arr[i
                               + (step1 * (times + step2))]
                               <= target)
                        times += step2;

                step2 = PowerOf2;

                // Add to final result
                // how many times
                // can the power be used
                i += times * step1;
            }
        }
        // Return the index
        // if the element is present in array
        // else return -1
        return arr[i] == target ? i : -1;
    }

    // Driver code
    public static void Main()
    {
        int[] arr = { 1, 4, 5, 8, 11, 15, 21, 45, 70, 100 };
        int target = 45, M = 10;
        int answer = Numeric_Base_Search(arr, M, target);
        Console.WriteLine(answer);
    }
}

// This code is contributed by ukasp.
```

JavaScript

```
<script>
    // JavaScript code for the above approach
    let N = 3
    let PowerOf2 = 4

    function Numeric_Base_Search(arr, M,
      target) {
      let i, step1,
        step2 = PowerOf2, times;

      // Find the first power of N 
      // greater than the array size
      for (step1 = 1; step1 < M; step1 *= N);

      for (i = 0; step1; step1 /= N)

        // Each time a power can be used
        // count how many times 
        // it can be used
        if (i + step1 < M && arr[i + step1]
          <= target) {
          for (times = 1; step2;
            step2 >>= 1)
            if (i +
              (step1 * (times + step2))
              < M &&
              arr[i +
              (step1 * (times + step2))]
              <= target)
              times += step2;

          step2 = PowerOf2;

          // Add to final result 
          // how many times 
          // can the power be used
          i += times * step1;
        }

      // Return the index 
      // if the element is present in array
      // else return -1
      return arr[i] == target ? i : -1;
    }

    // Driver code
    let arr =
      [1, 4, 5, 8, 11, 15, 21, 45, 70, 100];
    let target = 45, M = 10;
    let answer = Numeric_Base_Search(arr, M, target);
    document.write(answer);

  // This code is contributed by Potta Lokesh
  </script>
```

Output

```
7
```

Time Complexity: O(log N M * log 2 N)
Auxiliary Space: O(1)
