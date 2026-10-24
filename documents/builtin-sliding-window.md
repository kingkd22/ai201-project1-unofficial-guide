Title: Sliding Window Algorithm Explained | Built In
Source: https://builtin.com/data-science/sliding-window-algorithm

---

Image: Shutterstock / Built In

UPDATED BY

Brennan Whitfield | Jun 18, 2025

Summary:

The sliding window algorithm is a technique that reduces nested loops into a single loop, optimizing time complexity from O(n²) to O(n). It’s used on arrays, lists or strings to find subarrays or substrings that meet conditions like maximum sum or target values.
more

The sliding window algorithm is a technique that reduces nested loops into a single loop, optimizing time complexity from O(n²) to O(n). It’s used on arrays, lists or strings to find subarrays or substrings that meet conditions like maximum sum or target values.

The sliding window algorithm is a problem-solving technique that’s designed to transform two nested loops into a single loop. It applies to arrays, lists or strings. Such problems are often approached with brute-force solutions that run in O(n²) or O(n³), but these are inefficient for large inputs However, the sliding window technique can reduce the time complexity of an algorithm to O(n).

Sliding window is commonly described as a technique rather than a distinct algorithm, since it can be applied to many different algorithmic problems.

## Sliding Window Algorithm Definition

Sliding window algorithm is a problem solving technique that transforms two nested loops into one loop. It can reduce the time complexity of an algorithm to O(n).

A tutorial on how the sliding window algorithm works. | Video: Ryan Schachte

## What Is the Sliding Window Algorithm?

The basic idea behind the sliding window technique is to transform two nested loops into a single loop. Below are some fundamental clues to identify sliding window algorithm problems:

- The problem will be based on an array, list or string type of data structure.

- It will ask to find subranges in that array to give the longest, shortest or target values of a string.

- Its concept is mainly based on ideas like the longest sequence or shortest sequence of something that satisfies a given condition perfectly.

Let’s say that if you have an array like below:

A sliding window of size three would run over it like below:

More on Data ScienceBubble Sort Time Complexity and Algorithm Explained

## How to Solve a Problem With the Sliding Window Algorithm

Below is the basic steps to solve problems related to the sliding window technique:

- Use a HashMap or dictionary to count a specific array input and increase the window toward the right using an outer loop or advance window.

- Use an inner loop (or pointer) to shrink the window from the left when certain conditions are met.

- Store the maximum (or minimum) value found in any valid window during iteration, depending on the problem's goal.

Example of sliding to find the largest sum of five consecutive elements.

```
[ 5, 7, 1, 4, 3, 6, 2, 9, 2 ]
```

More on Data ScienceNlogn and Other Big O Notation Explained

## Sliding Window Algorithm Examples With Solutions

There are many problem statements of sliding window techniques. Sliding windows can be fixed-size (e.g., subarray of length k) or variable-size (e.g., longest substring meeting certain criteria), so we’ll explore both of these types in the examples below:

### 1. Maximum Sum Subarray of Size K

Given an array of positive integers and a positive number k, find the maximum sum of any contiguous subarray of size k.

```
Input: [3, 5, 2, 1, 7], k=2
Output: 8
```

The subarray [1, 7] is the sum of the maximum sum.

#### Solution

```
def getMaxSum(arr, k):
    maxSum = 0
    windowSum = 0
    start = 0
    
    for i in range(len(arr)):
        windowSum += arr[i]
        
        if ((i - start + 1) == k):
            maxSum = max(maxSum, windowSum)
            windowSum -= arr[start]
            start += 1
    
    return maxSum
```

### 2. Count Occurrences of Anagram

Given a word and a text, return the count of occurrences of the anagrams of the word in the text.

```
Input: text = gotxxotgxdogt, word = got
Output : 3
```

Words “got,” “otg” and “ogt” are anagrams of “got.”

#### Solution 1

```
from collections import Counter

def isAnagram(s, word):
    return Counter(s) == Counter(word)

def countAnagram(text, word):
    w = len(word)
    count = 0
    d = {}

    if len(text) < w:
        return 0

    for i in range(len(text) - w + 1):
        ana = text[i:i + w]
        if ana not in d and isAnagram(ana, word):
            count += 1
            d[ana] = True

    return count
```

#### Solution 2

```
def getCountOccurances(text, word):
    wHeap = [0] * 26
    textHeap = [0] * 26
    start = 0
    count = 0
    
    for c in word:
        wHeap[ord(c) - ord('a')] += 1
    
    for i in range(len(text)):
        textHeap[ord(text[i]) - ord('a')] += 1
        if (i - start + 1) == len(word):
            if textHeap == wHeap:
                count += 1
            
            textHeap[ord(text[start]) - ord('a')] -= 1
            start += 1
        
    return count
```

### 3. Difference Between the Maximum and Minimum Average of all K-Length Continuous Subarrays

```
Input: arr[ ] = {3, 8, 9, 15}, K = 2
Output: 6.5
```

All subarrays of length 2 are {3, 8}, {8, 9}, {9, 15} and their averages are (3+8)/2 = 5.5, (8+9)/2 = 8.5, and (9+15)/2 = 12.0 respectively.

Therefore, the difference between the maximum(=12.0) and minimum(=5.5) is 12.0 -5.5 = 6.5.

#### Solution

```
def getMinMaxDiff(arr, k):
    n = len(arr)
    
    if k > n:
        return -1
    
    min_avg = float('inf')
    max_avg = float('-inf')
    
    window_sum = sum(arr[:k])
    
    for i in range(k, n):
        current_avg = window_sum / k
        min_avg = min(min_avg, current_avg)
        max_avg = max(max_avg, current_avg)
        window_sum -= arr[i - k]
        window_sum += arr[i]
    
    last_avg = window_sum / k
    min_avg = min(min_avg, last_avg)
    max_avg = max(max_avg, last_avg)
    
    difference = max_avg - min_avg
    
    return difference

# Test case
arr = [3, 8, 9, 15]
k = 2
result = getMinMaxDiff(arr, k)
print(result)  # Output: 6.5
```

### 4. Find the Longest Substring of a String Containing ‘K’ Distinct Characters

```
Input: s = 'abcbdbdbbdcdabd'
k = 2
Output: bdbdbbd
```

#### Solution

```
def getLongest(s, k):
    high = 0
    windows = set()
    freq = [0] * 128
    low = 0
    end = 0
    start = 0
    
    while high < len(s):
        windows.add(s[high])
        freq[ord(s[high])] += 1
        
        while len(windows) > k:
            freq[ord(s[low])] -= 1
            if freq[ord(s[low])] == 0:
                windows.remove(s[low])
            
            low += 1
            
        if end - start < high - low:
            end = high
            start = low
        
        high += 1
        
    return s[start:end + 1]
```

### 5. Find Duplicates Within a Range ‘K’ in an Array

```
Input: nums = [5, 6, 8, 2, 4, 6, 9]
k = 2
Output: False
```

#### Solution

```
def getDuplicates(nums, k):
    d = {}
    count = 0
    for i in range(len(nums)):
        if nums[i] in d and i - d[nums[i]] <= k:
            return True
        else:
            d[nums[i]] = i
    
    return False
```

### 6. Find Minimum Sum SubArray of Size K

```
Input: arr = [10, 4, 2, 5, 6, 3, 8, 1]
k = 3
Output: 11
```

#### Solution

```
def getMinSum(arr, k):
    currSum = 0
    minSum = float("inf")
    start = 0
    
    for i in range(len(arr)):
        currSum += arr[i]
        
        if (i - start + 1 == k):
            minSum = min(minSum, currSum)
            currSum -= arr[start]
            start += 1
    
    return minSum
```

### 7. Length of the Longest Substring That Doesn’t Contain Any Vowels

```
Input: s = "codeforintelligents"
Output: 3
Explanation: 'nts' is the longest substring that doesn't contain any vowels.
```

#### Solution

```
def getLongestSubstring(s):
    vowels = ['a', 'e', 'i', 'o', 'u']
    result = ""
    maxResult = ""
    for i in range(len(s)):
        if s[i] not in vowels:
            result += s[i]
            print(result)
            if len(result) > len(maxResult):
                maxResult = result
        else:
            result = ""
    
    return len(maxResult)
```

### 8. Count Negative Elements Present in Every K-Length Subarray

```
Input: arr = [-1, 2, -2, 3, 5, -7, -5], K = 3
Output: 2, 1, 1, 1, 2
```

#### Solution

```
def getCountNegatives(arr, k):
    lst = []
    start = 0
    count = 0
    
    for i in range(len(arr)):
        if arr[i] < 0:
            count += 1
        
        if (i - start + 1 == k):
            lst.append(count)
            if arr[start] < 0:
                count -= 1
                
            start += 1
    
    return lst
```

### 9. Minimum Size Subarray Sum

```
Input: target = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: The subarray [4,3] has the minimal length under the problem constraint
```

#### Solution

```
def minSubArrayLen(target, nums):
    currSum = 0
    start = 0
    count = 0
    minCount = float("inf")
    
    for i in range(len(nums)):
        currSum += nums[i]
        
        while currSum >= target:
            minCount = min(minCount, i - start + 1)
            currSum -= nums[start]
            start += 1
        
        if minCount == float("inf"):
            return 0
        
    return minCount
```

### 10. Longest Repeating Character Replacement

You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

```
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
```

#### Solution

```
def characterReplacement(self, s, k):
        freq = {}
        maxRepeatLetterCount = 0
        windowStart = 0
        maxLength = 0
        
        for i in range(len(s)):
            if s[i] not in freq:
                freq[s[i]]= 0
            
            freq[s[i]] += 1
            maxRepeatLetterCount = max(maxRepeatLetterCount, freq[s[i]])
            if (i - windowStart + 1 - maxRepeatLetterCount) > k:
                freq[s[windowStart]] -= 1
                windowStart += 1
            
        maxLength = max(maxLength, i-windowStart + 1)
        
        return maxLength
```

### 11. Count Distinct Absolute Values in a Sorted Array

```
Input:  { -1, -1, 0, 1, 1, 1 }
Output: The total number of distinct absolute values is 2 (0 and 1)
```

#### Solution

```
def getCountDistinct(arr):
    count = 0
    d = {}
    for item in arr:
        if abs(item) not in d:
            d[abs(item)] = 1
            count += 1

    return count
```

### 12. Permutation in String

Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.

In other words, return true if one of s1’s permutations is the substring of s2.

```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
Explanation: s2 contains one permutation of s1 ("ba").
```

#### Solution

```
def checkInclusion(self, s1, s2):
    numbers = [0]*26
    numbers2 = [0]*26
    
    for c in s1:
        numbers[ord(c) - ord('a')] += 1
        
    for index in range(0, len(s2)):
        numbers2[ord(s2[index]) - ord('a')] += 1
        
        if index >= len(s1) - 1:
            if numbers == numbers2:
                return True
                
            numbers2[ord(s2[index - len(s1) + 1]) - ord('a')] -= 1
                
    return False
```

### 13. Find All Anagrams in a String

```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".
```

#### Solution

```
def findAnagrams(s, p):
    target = [0] *  26
    result = []
    count = [0] * 26
    start = 0
    
    for c in p:
        target[ord(c) - ord('a')] += 1
   
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        if i - start == len(p):
            count[ord(s[start]) - ord('a')] -= 1
            start += 1
        
        if count == target:
            result.append(start)
    return result
```

### 14. Maximum Average Subarray I

You are given an integer array of nums consisting of n elements and an integer k.

Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10–5 will be accepted.

```
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
```

#### Solution

```
def findMaxAverage(self, nums, k):
    st = 0
    max_sum = float('-inf')
    win_sum = 0.0
    
    for i in range(len(nums)):
        win_sum += nums[i]
        if i >= k-1:
            max_sum = max(win_sum, max_sum)
            win_sum -= nums[st]
            st += 1
        
    return max_sum/k
```

### 15. K Radius Subarray Averages

Build and return an array avgs of length n where avgs[i] is the k-radius average for the subarray centered at index i.

```
Input: nums = [7,4,3,9,1,8,5,2,6], k = 3
Output: [-1,-1,-1,5,4,4,-1,-1,-1]
```

#### Solution

```
def getAverages(self, nums, k):
    if k == 0:
        return nums
        
    n = len(nums)
    ans = [-1] * n
    prefSum = [0] * n
        
    for i in range(0, n):
        if i == 0:
            prefSum[0] = nums[i]
        else:
            prefSum[i] = prefSum[i-1] + nums[i]
                
    for i in range(k, n-k):
        if i-k-1 < 0:
            ans[i] = (prefSum[i + k])//(2*k + 1)
        else:
            ans[i] = (prefSum[i + k] - prefSum[i - k - 1])//(2*k + 1)
                
    return ans
```

### 16. Substrings of Size Three With Distinct Characters

A string is good if there are no repeated characters.

Given a string s, return the number of good substrings of length three in s.

If there are multiple occurrences of the same substring, every occurrence should be counted.

A substring is a contiguous sequence of characters in a string.

```
Input: s = "xyzzaz"
Output: 1
Explanation: There are 4 substrings of size 3: "xyz", "yzz", "zza", and "zaz".
The only good substring of length 3 is "xyz".
```

#### Solution

```
class Solution(object):
    def countGoodSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """
        k = 3
        
        if k > len(s):
            return 0
        
        freq = {}
        count = 0
        start = 0
        
        for i in range(len(s)):
            if s[i] not in freq:
                freq[s[i]] = 0
            freq[s[i]] += 1
            
            if i >= k - 1:
                if len(freq) == k:
                    count += 1
                
                freq[s[start]] -= 1
                if freq[s[start]] == 0:
                    del freq[s[start]]
                
                start += 1
                
        return count
```

### 17. Frequency of the Most Frequent Element

The frequency of an element is the number of times it occurs in an array.

You are given an integer array nums and an integer k. In one operation, you can choose an index of nums and increment the element at that index by 1.

Return the maximum possible frequency of an element after performing at most k operations.

```
Input: nums = [1,2,4], k = 5
Output: 3
Explanation: Increment the first element three times and the second element two times to make nums = [4,4,4].
4 has a frequency of 3.
```

#### Solution

```
class Solution(object):
    def maxFrequency(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        len_nums = len(nums)
        nums.sort()
        max_freq = 1
        freq = 1
        left = 0
        ops = k
        
        for right in range(1, len_nums):
            ops -= (nums[right] - nums[right - 1]) * freq
            freq += 1
            if ops >= 0:
                max_freq = max(max_freq, freq)
            else:
                while ops < 0:
                    ops += nums[right] - nums[left]
                    left += 1
                    freq -= 1
                    
        return max_freq
```

### 18. Maximum Erasure Value

You are given an array of positive integers nums and want to erase a subarray containing unique elements. The score you get by erasing the subarray is equal to the sum of its elements.

Return the maximum score you can get by erasing exactly one subarray.

An array b is called to be a subarray if it forms a contiguous subsequence of a that is if it is equal to a[l], a[l+1],…, a[r] for some (l,r).

```
Input: nums = [4,2,4,5,6]
Output: 17
Explanation: The optimal subarray here is [2,4,5,6].
```

#### Solution

```
class Solution(object):
    def maximumUniqueSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        m = {}
        final = 0
        summ = 0
        l = 0
        
        for i in range(len(nums)):
            if nums[i] in m:
                index = m[nums[i]]
                while l <= index:
                    del m[nums[l]]
                    summ -= nums[l]
                    l += 1
            
            m[nums[i]] = i
            summ += nums[i]
            final = max(final, summ)
        
        return final
```

### 19. Maximum Number of Occurrences of a Substring

Given a string s, return the maximum number of occurrences of any substring under the following rules:

- The number of unique characters in the substring must be less than or equal to maxLetters.

- The substring size must be between minSize and maxSize inclusive.

```
Input: s = "aababcaab", maxLetters = 2, minSize = 3, maxSize = 4
Output: 2
Explanation: Substring "aab" has 2 ocurrences in the original string.
It satisfies the conditions, 2 unique letters and size 3 (between minSize and maxSize).
```

#### Solution

```
class Solution(object):
    def maxFreq(self, s, maxLetters, minSize, maxSize):
        """
        :type s: str
        :type maxLetters: int
        :type minSize: int
        :type maxSize: int
        :rtype: int
        """
        cnt = {}
        res= 0
        
        for i in range(0,len(s)-minSize+1):
            sub = s[i:i + minSize]
            
            if len(set(sub)) <= maxLetters:
                if sub not in cnt:
                    cnt[sub] = 0
                
                cnt[sub] += 1
                res = max(res, cnt[sub])
                
        return res
```

### 20. Number of Subarrays of Size K and Average Greater than or Equal to Threshold

Given an array of integers arr and two integers k and threshold.

Return the number of subarrays of size k and average greater than or equal to a threshold.

```
Input: arr = [2,2,2,2,5,5,5,8], k = 3, threshold = 4
Output: 3
Explanation: Sub-arrays [2,5,5],[5,5,5] and [5,5,8] have averages 4, 5 and 6 respectively. All other sub-arrays of size 3 have averages less than 4 (the threshold).
```

#### Solution

```
class Solution(object):
    def numOfSubarrays(self, arr, k, threshold):
        """
        :type arr: List[int]
        :type k: int
        :type threshold: int
        :rtype: int
        """
        start = 0
        windowSum = 0
        count = 0
        
        for windowEnd in range(len(arr)):
            windowSum += arr[windowEnd] 
            if windowEnd >= k - 1:
                if (windowSum/k) >= threshold:
                    count+=1
                windowSum -=arr[start]
                start += 1
                
        return count
```

### 21. Number of Substrings Containing All Three Characters

Given a string s consisting only of characters a, b and c.

Return the number of substrings containing at least one occurrence of all these characters a, b and c.

```
Input: s = "abcabc"
Output: 10
Explanation: The substrings containing at least one occurrence of the characters a, b and c are "abc", "abca", "abcab", "abcabc", "bca", "bcab", "bcabc", "cab", "cabc" and "abc" (again)
```

#### Solution

```
class Solution(object):
    def numberOfSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """
        count, left = 0, 0
        map = {x:0 for x in "abc"}
        
        for right in range(0,len(s)):
            map[s[right]] += 1
            
            while map["a"] and map["b"] and map["c"]:
                map[s[left]] -= 1
                left += 1
            
            count += left
            
        return count
```

### 22. Maximum Points You Can Obtain from Cards

There are several cards arranged in a row, and each card has an associated number of points. The points are given in the integer array cardPoints.

In one step, you can take one card from the beginning or from the end of the row. You have to take exactly k cards.

Your score is the sum of the points of the cards you have taken.

Given the integer array cardPoints and the integer k, return the maximum score you can obtain.

```
Input: cardPoints = [1,2,3,4,5,6,1], k = 3
Output: 12
Explanation: After the first step, your score will always be 1. However, choosing the rightmost card first will maximize your total score. The optimal strategy is to take the three cards on the right, giving a final score of 1 + 6 + 5 = 12.
```

#### Solution

```
class Solution(object):
    def maxScore(self, cardPoints, k):
        """
        :type cardPoints: List[int]
        :type k: int
        :rtype: int
        """
        best = score = sum(cardPoints[:k])
        
        for i in range(1, k+1):
            score = score - cardPoints[k-i] + cardPoints[-i]
            best = score if score > best else best
            
        return best
```

### 23. Longest Continuous Subarray With Absolute Diff Less Than or Equal to

Given an array of integers nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to the limit.

```
Input: nums = [8,2,4,7], limit = 4
Output: 2
Explanation: All subarrays are:
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4.
Therefore, the size of the longest subarray is 2.
```

#### Solution

```
from collections import deque

def longestSubarray(nums, limit):
    maxDeque = deque()
    minDeque = deque()
    left = 0
    result = 0

    for right in range(len(nums)):
        # Maintain decreasing max deque
        while maxDeque and nums[right] > maxDeque[-1]:
            maxDeque.pop()
        maxDeque.append(nums[right])

        # Maintain increasing min deque
        while minDeque and nums[right] < minDeque[-1]:
            minDeque.pop()
        minDeque.append(nums[right])

        # Shrink window if limit exceeded
        while maxDeque[0] - minDeque[0] > limit:
            if nums[left] == maxDeque[0]:
                maxDeque.popleft()
            if nums[left] == minDeque[0]:
                minDeque.popleft()
            left += 1

        result = max(result, right - left + 1)

    return result
```

### 24. Maximum Number of Vowels in a Substring of Given Length

Given a string s and an integer k.

Return the maximum number of vowel letters in any substring of s with length k.

Vowel letters in English are (a, e, i, o, u).

```
Input: s = "abciiidef", k = 3
Output: 3
Explanation: The substring "iii" contains 3 vowel letters.
```

#### Solution

```
class Solution(object):
    def maxVowels(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        vowels = ['a','e','i','o','u']
        ans = 0
        win = ''
        v = 0
        
        for char in range(k):
            win += s[char]
            
            if s[char] in vowels:
                v+=1
                
        ans = max(ans,v)
        
        for char in range(len(s)-k):
            win += s[char+k]
            if s[char] in vowels:
                v-=1
            if s[char+k] in vowels:
                v+=1
            ans=max(ans,v)
        return ans
```

### 25. Find Two Non-Overlapping Subarrays Each With Target Sum

Given an array of integers arr and an integer target.

You have to find two non-overlapping subarrays of arr each with a sum equal target. There can be multiple answers so you have to find an answer where the sum of the lengths of the two subarrays is minimum.

Return the minimum sum of the lengths of the two required subarrays, or return -1 if you cannot find such two subarrays.

```
Input: arr = [3,2,2,4,3], target = 3
Output: 2
Explanation: Only two sub-arrays have sum = 3 ([3] and [3]). The sum of their lengths is 2
```

#### Solution

```
class Solution(object):
    def minSumOfLengths(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """
        INF = len(arr) + 1
        best_at_i = [INF]*len(arr) 
        best = INF 
        curr_sum = 0 
        
        left = 0
        for right in range(len(arr)):
            curr_sum += arr[right]
            
            while curr_sum > target and left <= right:
                curr_sum -= arr[left]
                left += 1
                
            if curr_sum == target:
                best = min(best, best_at_i[left-1] + right - left + 1)
                best_at_i[right] = min(best_at_i[right-1], right - left + 1)
            else:
                best_at_i[right] = best_at_i[right-1]
        
        if best == INF:
            return -1
        return best
```

### 26. Longest Subarray of 1’s After Deleting One Element

Given binary array nums, you should delete one element from it.

Return the size of the longest non-empty subarray containing only 1’s in the resulting array. Return 0 if there is no such subarray.

```
Input: nums = [1,1,0,1]
Output: 3
Explanation: After deleting the number in position 2, [1,1,1] contains 3 numbers with value of 1's.
```

#### Solution

```
class Solution(object):
    def longestSubarray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        windowStart = 0
        hashmap = {x: 0 for x in nums}
        max_length = 0
        
        if 0 not in hashmap.keys():
            return len(nums) - 1
        
        for windowEnd in range(len(nums)):
            hashmap[nums[windowEnd]] += 1
            
            if hashmap[0] > 1:
                hashmap[nums[windowStart]] -= 1
                windowStart += 1
            
            max_length = max(max_length, windowEnd - windowStart)
        return (max_length)
```

### 27. Minimum Operations to Reduce X to Zero

You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.

Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.

```
Input: nums = [1,1,4,2,3], x = 5
Output: 2
Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
```

#### Solution

```
class Solution(object):
    def minOperations(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """
        S = sum(nums)
        left = right = curr = 0
        ans = -1
        
        while right<len(nums):
            curr += nums[right]
            right+=1
            while left<len(nums) and curr>S-x:
                curr-=nums[left]
                left+=1
            if curr == S-x:
                ans = max(ans,right-left)
                
        return len(nums) - ans if ans!=-1 else ans
```

### 28. Get Equal Substrings Within Budget

You are also given an integer maxCost.

Return the maximum length of a substring of s that can be changed to be the same as the corresponding substring of t with a cost less than or equal to maxCost.

If there is no substring from s that can be changed to its corresponding substring from t, return 0.

```
Input: s = "abcd", t = "bcdf", maxCost = 3
Output: 3
Explanation: "abc" of s can change to "bcd". That costs 3, so the maximum length is 3.
```

#### Solution

```
class Solution(object):
    def equalSubstring(self, s, t, maxCost):
        """
        :type s: str
        :type t: str
        :type maxCost: int
        :rtype: int
        """
        diff = [abs(ord(s[i]) - ord(t[i])) for i in range(len(s))]
        summ = 0
        low = length = 0
        
        for i in range(len(s)):
            summ += diff[i]
            
            while low < i and summ > maxCost:
                summ -= diff[low]
                low += 1
            if summ <= maxCost:
                length = max(length, i-low+1)
                
        return length
```

### 29. Grumpy Bookstore Owner

There is a bookstore owner that has a store open for n minutes. Every minute, some number of customers enter the store. You are given an integer array of customers of length n where customers[i] is the number of the customer that enters the store at the start of the ith minute and all those customers leave after the end of that minute.

For some minutes, the bookstore owner is grumpy. You are given a binary array grumpy where grumpy[i] is 1 if the bookstore owner is grumpy during the ith minute, and is 0 otherwise.

When the bookstore owner is grumpy, the customers during that minute aren’t satisfied, otherwise, they are satisfied.

The bookstore owner knows a secret technique to keep themselves not grumpy for consecutive minutes but can only use it once.

Return the maximum number of customers that can be satisfied throughout the day.

```
Input: customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3
Output: 16
Explanation: The bookstore owner keeps themselves not grumpy for the last 3 minutes. 
The maximum number of customers that can be satisfied = 1 + 1 + 1 + 1 + 7 + 5 = 16.
```

#### Solution

```
class Solution(object):
    def maxSatisfied(self, customers, grumpy, minutes):
        """
        :type customers: List[int]
        :type grumpy: List[int]
        :type minutes: int
        :rtype: int
        """
        n = len(customers)
        res = 0
        
        for i in range(n):
            if grumpy[i] == 0:
                res += customers[i]
        sum1 = 0        
        for i in range(minutes):
            if grumpy[i] == 1:
                sum1 += customers[i]
                
        result = sum1
        for r in range(minutes, n):
            if grumpy[r] == 1:
                sum1 += customers[r]
            if grumpy[r - minutes] == 1:
                sum1 -= customers[r - minutes]
            result = max(sum1, result)
        
        return res + result
```

### 30. Max Consecutive Ones III

Given binary array nums and an integer k, return the maximum number of consecutive 1’s in the array if you can flip at most k 0’s.

```
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
```

#### Solution

```
class Solution(object):
    def longestOnes(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        start, end, n, max_consecutive = 0, 0, len(nums), 0
        
        while end < n:
            if nums[end] == 0:
                if k > 0:
                    k -= 1
                else:                  
                    max_consecutive = max(max_consecutive, end - start)
                    if nums[start] == 0:
                        k += 1
                    start += 1
                    continue
            end += 1
```

### 31. Binary Subarrays With Sum

Given binary array nums and an integer goal, return the number of non-empty subarrays with a sum goal. A subarray is a contiguous part of the array.

```
Input: nums = [1,0,1,0,1], goal = 2
Output: 4
Explanation: The 4 subarrays are bolded and underlined below:
[1,0,1,0,1]
[1,0,1,0,1]
[1,0,1,0,1]
[1,0,1,0,1]
```

#### Solution

```
class Solution(object):
    def numSubarraysWithSum(self, nums, goal):
        """
        :type nums: List[int]
        :type goal: int
        :rtype: int
        """
        cumSum = 0
        result = 0
        
        hashMap = {0:1}
        
        for x in nums:
            cumSum += x
            
            val = cumSum - goal
            if (val) in hashMap:
                result += hashMap[val]
            
            hashMap[cumSum] = hashMap.get(cumSum, 0) + 1
        
        return result
```

### 32. Maximum Length of Repeated Subarray

Given two integer arrays nums1 and nums2, return the maximum length of a subarray that appears in both arrays.

```
Input: nums1 = [1,2,3,2,1], nums2 = [3,2,1,4,7]
Output: 3
Explanation: The repeated subarray with maximum length is [3,2,1].
```

#### Solution

```
class Solution(object):
    def findLength(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """
        nums2_str = ''.join([chr(x) for x in nums2])
        max_str = ''
        res = 0
        
        for num in nums1:
            max_str += chr(num)
            if max_str in nums2_str:
                res = max(res,len(max_str))
            else:
                max_str = max_str[1:]
                
        return res
```

### 33. Longest Turbulent Subarray

Given an integer array arr, return the length of a maximum size turbulent subarray of arr.

A subarray is turbulent if the comparison sign flips between each adjacent pair of elements in the subarray.

```
Input: arr = [9,4,2,10,7,8,8,1,9]
Output: 5
Explanation: arr[1] > arr[2] < arr[3] > arr[4] < arr[5]
```

#### Solution

```
class Solution(object):
    def maxTurbulenceSize(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """
        n = len(arr)
        ans = 1
        anchor = 0
        
        for i in range(1, n):
            c = cmp(arr[i-1], arr[i])
            if c == 0:
                anchor = i
            elif i == n - 1 or c * cmp(arr[i], arr[i+1]) != -1:
                ans = max(ans, i - anchor + 1)
                anchor = i
        
        return ans
```

### 34. Longest Substring Of All Vowels in Order

Given a string word consisting of English vowels, return the length of the longest beautiful substring of a word. If no such substring exists, return 0.

A substring is a contiguous sequence of characters in a string.

```
Input: word = "aeiaaioaaaaeiiiiouuuooaauuaeiu"
Output: 13
Explanation: The longest beautiful substring in word is "aaaaeiiiiouuu" of length 13.
```

#### Solution

```
class Solution(object):
    def longestBeautifulSubstring(self, word):
        """
        :type word: str
        :rtype: int
        """
        res = 0
        i = 0
        seen = set()
        
        for j in range(0,len(word)):
            if j > 0 and word[j] < word[j-1]:
                seen = set()
                i = j
            
            seen.add(word[j])
            if len(seen) == 5:
                res = max(res,j-i+1)
                
        return res
```

### 35. Fruit Into Baskets

You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.

You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:

- You only have two baskets, and each basket can only hold a single type of fruit. There is no limit on the amount of fruit each basket can hold.

- Starting from any tree of your choice, you must pick exactly one fruit from every tree (including the start tree) while moving to the right. The picked fruits must fit in one of your baskets.

- Once you reach a tree with fruit that cannot fit in your baskets, you must stop.

Given the integer array, return the maximum number of fruits you can pick.

```
Input: fruits = [1,2,1]
Output: 3
Explanation: We can pick from all 3 trees.
```

#### Solution

```
class Solution(object):
    def totalFruit(self, fruits):
        """
        :type fruits: List[int]
        :rtype: int
        """
        length = len(fruits)
        left, right, current = 0, length - 1, {}
        currentLength, longestLength = 0, 0
        
        for right in range(0, length):
            current[fruits[right]] = current.get(fruits[right], 0) + 1
            
            while len(current) > 2:
                current[fruits[left]] -= 1
                if current[fruits[left]] == 0:
                    del current[fruits[left]]
                left += 1   
                
            currentLength  = right - left + 1
            longestLength = max(longestLength, currentLength)     
            
        return longestLength
```

## Frequently Asked Questions

### What is the sliding window algorithm?

The sliding window algorithm is a technique used to efficiently find subarrays or substrings that meet specific conditions, such as maximum sum, fixed-length averages, or unique character constraints in arrays, lists or strings. It reduces the time complexity of problems that would normally require nested loops (O(n²) or O(n³)) to a single-pass solution in O(n), making it more scalable for large data sets.

### What is the sliding window technique formula?

The sliding window technique involves moving a window of size k across a data structure by adding the incoming element and removing the outgoing one as the window shifts. For example, to update a sum:

current_sum = current_sum - element_out + element_in.

This allows efficient computation over subarrays or substrings without reprocessing the entire window each time.

### How do you calculate sliding windows?

To calculate the sum of a subarray within a sliding window, subtract the element that exits the window and add the new element that enters it as the window moves forward. For example:

sum = sum - arr[left] + arr[right]
