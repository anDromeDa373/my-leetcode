#!/usr/bin/env python3
"""Scaffold NeetCode 150 problem directories under src/."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"

NEETCODE_150 = [
    {
        "title": "Contains Duplicate",
        "url": "https://leetcode.com/problems/contains-duplicate/",
        "category": "Arrays & Hashing",
        "difficulty": "Easy"
    },
    {
        "title": "Valid Anagram",
        "url": "https://leetcode.com/problems/valid-anagram/",
        "category": "Arrays & Hashing",
        "difficulty": "Easy"
    },
    {
        "title": "Two Sum",
        "url": "https://leetcode.com/problems/two-sum/",
        "category": "Arrays & Hashing",
        "difficulty": "Easy"
    },
    {
        "title": "Group Anagrams",
        "url": "https://leetcode.com/problems/group-anagrams/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Top K Frequent Elements",
        "url": "https://leetcode.com/problems/top-k-frequent-elements/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Encode and Decode Strings",
        "url": "https://leetcode.com/problems/encode-and-decode-strings/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Product of Array Except Self",
        "url": "https://leetcode.com/problems/product-of-array-except-self/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Valid Sudoku",
        "url": "https://leetcode.com/problems/valid-sudoku/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Consecutive Sequence",
        "url": "https://leetcode.com/problems/longest-consecutive-sequence/",
        "category": "Arrays & Hashing",
        "difficulty": "Medium"
    },
    {
        "title": "Valid Palindrome",
        "url": "https://leetcode.com/problems/valid-palindrome/",
        "category": "Two Pointers",
        "difficulty": "Easy"
    },
    {
        "title": "Two Sum II Input Array Is Sorted",
        "url": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/",
        "category": "Two Pointers",
        "difficulty": "Medium"
    },
    {
        "title": "3Sum",
        "url": "https://leetcode.com/problems/3sum/",
        "category": "Two Pointers",
        "difficulty": "Medium"
    },
    {
        "title": "Container With Most Water",
        "url": "https://leetcode.com/problems/container-with-most-water/",
        "category": "Two Pointers",
        "difficulty": "Medium"
    },
    {
        "title": "Trapping Rain Water",
        "url": "https://leetcode.com/problems/trapping-rain-water/",
        "category": "Two Pointers",
        "difficulty": "Hard"
    },
    {
        "title": "Best Time to Buy And Sell Stock",
        "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/",
        "category": "Sliding Window",
        "difficulty": "Easy"
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/",
        "category": "Sliding Window",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Repeating Character Replacement",
        "url": "https://leetcode.com/problems/longest-repeating-character-replacement/",
        "category": "Sliding Window",
        "difficulty": "Medium"
    },
    {
        "title": "Permutation In String",
        "url": "https://leetcode.com/problems/permutation-in-string/",
        "category": "Sliding Window",
        "difficulty": "Medium"
    },
    {
        "title": "Minimum Window Substring",
        "url": "https://leetcode.com/problems/minimum-window-substring/",
        "category": "Sliding Window",
        "difficulty": "Hard"
    },
    {
        "title": "Sliding Window Maximum",
        "url": "https://leetcode.com/problems/sliding-window-maximum/",
        "category": "Sliding Window",
        "difficulty": "Hard"
    },
    {
        "title": "Valid Parentheses",
        "url": "https://leetcode.com/problems/valid-parentheses/",
        "category": "Stack",
        "difficulty": "Easy"
    },
    {
        "title": "Min Stack",
        "url": "https://leetcode.com/problems/min-stack/",
        "category": "Stack",
        "difficulty": "Medium"
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "url": "https://leetcode.com/problems/evaluate-reverse-polish-notation/",
        "category": "Stack",
        "difficulty": "Medium"
    },
    {
        "title": "Daily Temperatures",
        "url": "https://leetcode.com/problems/daily-temperatures/",
        "category": "Stack",
        "difficulty": "Medium"
    },
    {
        "title": "Car Fleet",
        "url": "https://leetcode.com/problems/car-fleet/",
        "category": "Stack",
        "difficulty": "Medium"
    },
    {
        "title": "Largest Rectangle In Histogram",
        "url": "https://leetcode.com/problems/largest-rectangle-in-histogram/",
        "category": "Stack",
        "difficulty": "Hard"
    },
    {
        "title": "Binary Search",
        "url": "https://leetcode.com/problems/binary-search/",
        "category": "Binary Search",
        "difficulty": "Easy"
    },
    {
        "title": "Search a 2D Matrix",
        "url": "https://leetcode.com/problems/search-a-2d-matrix/",
        "category": "Binary Search",
        "difficulty": "Medium"
    },
    {
        "title": "Koko Eating Bananas",
        "url": "https://leetcode.com/problems/koko-eating-bananas/",
        "category": "Binary Search",
        "difficulty": "Medium"
    },
    {
        "title": "Find Minimum In Rotated Sorted Array",
        "url": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/",
        "category": "Binary Search",
        "difficulty": "Medium"
    },
    {
        "title": "Search In Rotated Sorted Array",
        "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/",
        "category": "Binary Search",
        "difficulty": "Medium"
    },
    {
        "title": "Time Based Key Value Store",
        "url": "https://leetcode.com/problems/time-based-key-value-store/",
        "category": "Binary Search",
        "difficulty": "Medium"
    },
    {
        "title": "Median of Two Sorted Arrays",
        "url": "https://leetcode.com/problems/median-of-two-sorted-arrays/",
        "category": "Binary Search",
        "difficulty": "Hard"
    },
    {
        "title": "Reverse Linked List",
        "url": "https://leetcode.com/problems/reverse-linked-list/",
        "category": "Linked List",
        "difficulty": "Easy"
    },
    {
        "title": "Merge Two Sorted Lists",
        "url": "https://leetcode.com/problems/merge-two-sorted-lists/",
        "category": "Linked List",
        "difficulty": "Easy"
    },
    {
        "title": "Linked List Cycle",
        "url": "https://leetcode.com/problems/linked-list-cycle/",
        "category": "Linked List",
        "difficulty": "Easy"
    },
    {
        "title": "Reorder List",
        "url": "https://leetcode.com/problems/reorder-list/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "Remove Nth Node From End of List",
        "url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "Copy List With Random Pointer",
        "url": "https://leetcode.com/problems/copy-list-with-random-pointer/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "Add Two Numbers",
        "url": "https://leetcode.com/problems/add-two-numbers/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "Find The Duplicate Number",
        "url": "https://leetcode.com/problems/find-the-duplicate-number/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "LRU Cache",
        "url": "https://leetcode.com/problems/lru-cache/",
        "category": "Linked List",
        "difficulty": "Medium"
    },
    {
        "title": "Merge K Sorted Lists",
        "url": "https://leetcode.com/problems/merge-k-sorted-lists/",
        "category": "Linked List",
        "difficulty": "Hard"
    },
    {
        "title": "Reverse Nodes In K Group",
        "url": "https://leetcode.com/problems/reverse-nodes-in-k-group/",
        "category": "Linked List",
        "difficulty": "Hard"
    },
    {
        "title": "Invert Binary Tree",
        "url": "https://leetcode.com/problems/invert-binary-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Maximum Depth of Binary Tree",
        "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Diameter of Binary Tree",
        "url": "https://leetcode.com/problems/diameter-of-binary-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Balanced Binary Tree",
        "url": "https://leetcode.com/problems/balanced-binary-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Same Tree",
        "url": "https://leetcode.com/problems/same-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Subtree of Another Tree",
        "url": "https://leetcode.com/problems/subtree-of-another-tree/",
        "category": "Trees",
        "difficulty": "Easy"
    },
    {
        "title": "Lowest Common Ancestor of a Binary Search Tree",
        "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Binary Tree Right Side View",
        "url": "https://leetcode.com/problems/binary-tree-right-side-view/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Count Good Nodes In Binary Tree",
        "url": "https://leetcode.com/problems/count-good-nodes-in-binary-tree/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Validate Binary Search Tree",
        "url": "https://leetcode.com/problems/validate-binary-search-tree/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Kth Smallest Element In a Bst",
        "url": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Construct Binary Tree From Preorder And Inorder Traversal",
        "url": "https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/",
        "category": "Trees",
        "difficulty": "Medium"
    },
    {
        "title": "Binary Tree Maximum Path Sum",
        "url": "https://leetcode.com/problems/binary-tree-maximum-path-sum/",
        "category": "Trees",
        "difficulty": "Hard"
    },
    {
        "title": "Serialize And Deserialize Binary Tree",
        "url": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/",
        "category": "Trees",
        "difficulty": "Hard"
    },
    {
        "title": "Kth Largest Element In a Stream",
        "url": "https://leetcode.com/problems/kth-largest-element-in-a-stream/",
        "category": "Heap / Priority Queue",
        "difficulty": "Easy"
    },
    {
        "title": "Last Stone Weight",
        "url": "https://leetcode.com/problems/last-stone-weight/",
        "category": "Heap / Priority Queue",
        "difficulty": "Easy"
    },
    {
        "title": "K Closest Points to Origin",
        "url": "https://leetcode.com/problems/k-closest-points-to-origin/",
        "category": "Heap / Priority Queue",
        "difficulty": "Medium"
    },
    {
        "title": "Kth Largest Element In An Array",
        "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/",
        "category": "Heap / Priority Queue",
        "difficulty": "Medium"
    },
    {
        "title": "Task Scheduler",
        "url": "https://leetcode.com/problems/task-scheduler/",
        "category": "Heap / Priority Queue",
        "difficulty": "Medium"
    },
    {
        "title": "Design Twitter",
        "url": "https://leetcode.com/problems/design-twitter/",
        "category": "Heap / Priority Queue",
        "difficulty": "Medium"
    },
    {
        "title": "Find Median From Data Stream",
        "url": "https://leetcode.com/problems/find-median-from-data-stream/",
        "category": "Heap / Priority Queue",
        "difficulty": "Hard"
    },
    {
        "title": "Subsets",
        "url": "https://leetcode.com/problems/subsets/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Combination Sum",
        "url": "https://leetcode.com/problems/combination-sum/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Combination Sum II",
        "url": "https://leetcode.com/problems/combination-sum-ii/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Permutations",
        "url": "https://leetcode.com/problems/permutations/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Subsets II",
        "url": "https://leetcode.com/problems/subsets-ii/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Generate Parentheses",
        "url": "https://leetcode.com/problems/generate-parentheses/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Word Search",
        "url": "https://leetcode.com/problems/word-search/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Palindrome Partitioning",
        "url": "https://leetcode.com/problems/palindrome-partitioning/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "url": "https://leetcode.com/problems/letter-combinations-of-a-phone-number/",
        "category": "Backtracking",
        "difficulty": "Medium"
    },
    {
        "title": "N Queens",
        "url": "https://leetcode.com/problems/n-queens/",
        "category": "Backtracking",
        "difficulty": "Hard"
    },
    {
        "title": "Implement Trie Prefix Tree",
        "url": "https://leetcode.com/problems/implement-trie-prefix-tree/",
        "category": "Tries",
        "difficulty": "Medium"
    },
    {
        "title": "Design Add And Search Words Data Structure",
        "url": "https://leetcode.com/problems/design-add-and-search-words-data-structure/",
        "category": "Tries",
        "difficulty": "Medium"
    },
    {
        "title": "Word Search II",
        "url": "https://leetcode.com/problems/word-search-ii/",
        "category": "Tries",
        "difficulty": "Hard"
    },
    {
        "title": "Number of Islands",
        "url": "https://leetcode.com/problems/number-of-islands/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Max Area of Island",
        "url": "https://leetcode.com/problems/max-area-of-island/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Clone Graph",
        "url": "https://leetcode.com/problems/clone-graph/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Walls And Gates",
        "url": "https://leetcode.com/problems/walls-and-gates/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Rotting Oranges",
        "url": "https://leetcode.com/problems/rotting-oranges/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Pacific Atlantic Water Flow",
        "url": "https://leetcode.com/problems/pacific-atlantic-water-flow/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Surrounded Regions",
        "url": "https://leetcode.com/problems/surrounded-regions/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Course Schedule",
        "url": "https://leetcode.com/problems/course-schedule/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Course Schedule II",
        "url": "https://leetcode.com/problems/course-schedule-ii/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Graph Valid Tree",
        "url": "https://leetcode.com/problems/graph-valid-tree/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Number of Connected Components In An Undirected Graph",
        "url": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Redundant Connection",
        "url": "https://leetcode.com/problems/redundant-connection/",
        "category": "Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Word Ladder",
        "url": "https://leetcode.com/problems/word-ladder/",
        "category": "Graphs",
        "difficulty": "Hard"
    },
    {
        "title": "Network Delay Time",
        "url": "https://leetcode.com/problems/network-delay-time/",
        "category": "Advanced Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Reconstruct Itinerary",
        "url": "https://leetcode.com/problems/reconstruct-itinerary/",
        "category": "Advanced Graphs",
        "difficulty": "Hard"
    },
    {
        "title": "Min Cost to Connect All Points",
        "url": "https://leetcode.com/problems/min-cost-to-connect-all-points/",
        "category": "Advanced Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Swim In Rising Water",
        "url": "https://leetcode.com/problems/swim-in-rising-water/",
        "category": "Advanced Graphs",
        "difficulty": "Hard"
    },
    {
        "title": "Alien Dictionary",
        "url": "https://leetcode.com/problems/alien-dictionary/",
        "category": "Advanced Graphs",
        "difficulty": "Hard"
    },
    {
        "title": "Cheapest Flights Within K Stops",
        "url": "https://leetcode.com/problems/cheapest-flights-within-k-stops/",
        "category": "Advanced Graphs",
        "difficulty": "Medium"
    },
    {
        "title": "Climbing Stairs",
        "url": "https://leetcode.com/problems/climbing-stairs/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Easy"
    },
    {
        "title": "Min Cost Climbing Stairs",
        "url": "https://leetcode.com/problems/min-cost-climbing-stairs/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Easy"
    },
    {
        "title": "House Robber",
        "url": "https://leetcode.com/problems/house-robber/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "House Robber II",
        "url": "https://leetcode.com/problems/house-robber-ii/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Palindromic Substring",
        "url": "https://leetcode.com/problems/longest-palindromic-substring/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Palindromic Substrings",
        "url": "https://leetcode.com/problems/palindromic-substrings/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Decode Ways",
        "url": "https://leetcode.com/problems/decode-ways/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Coin Change",
        "url": "https://leetcode.com/problems/coin-change/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Maximum Product Subarray",
        "url": "https://leetcode.com/problems/maximum-product-subarray/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Word Break",
        "url": "https://leetcode.com/problems/word-break/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Increasing Subsequence",
        "url": "https://leetcode.com/problems/longest-increasing-subsequence/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Partition Equal Subset Sum",
        "url": "https://leetcode.com/problems/partition-equal-subset-sum/",
        "category": "1-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Unique Paths",
        "url": "https://leetcode.com/problems/unique-paths/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Common Subsequence",
        "url": "https://leetcode.com/problems/longest-common-subsequence/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Best Time to Buy And Sell Stock With Cooldown",
        "url": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Coin Change II",
        "url": "https://leetcode.com/problems/coin-change-ii/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Target Sum",
        "url": "https://leetcode.com/problems/target-sum/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Interleaving String",
        "url": "https://leetcode.com/problems/interleaving-string/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Longest Increasing Path In a Matrix",
        "url": "https://leetcode.com/problems/longest-increasing-path-in-a-matrix/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Hard"
    },
    {
        "title": "Distinct Subsequences",
        "url": "https://leetcode.com/problems/distinct-subsequences/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Hard"
    },
    {
        "title": "Edit Distance",
        "url": "https://leetcode.com/problems/edit-distance/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Medium"
    },
    {
        "title": "Burst Balloons",
        "url": "https://leetcode.com/problems/burst-balloons/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Hard"
    },
    {
        "title": "Regular Expression Matching",
        "url": "https://leetcode.com/problems/regular-expression-matching/",
        "category": "2-D Dynamic Programming",
        "difficulty": "Hard"
    },
    {
        "title": "Maximum Subarray",
        "url": "https://leetcode.com/problems/maximum-subarray/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Jump Game",
        "url": "https://leetcode.com/problems/jump-game/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Jump Game II",
        "url": "https://leetcode.com/problems/jump-game-ii/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Gas Station",
        "url": "https://leetcode.com/problems/gas-station/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Hand of Straights",
        "url": "https://leetcode.com/problems/hand-of-straights/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Merge Triplets to Form Target Triplet",
        "url": "https://leetcode.com/problems/merge-triplets-to-form-target-triplet/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Partition Labels",
        "url": "https://leetcode.com/problems/partition-labels/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Valid Parenthesis String",
        "url": "https://leetcode.com/problems/valid-parenthesis-string/",
        "category": "Greedy",
        "difficulty": "Medium"
    },
    {
        "title": "Insert Interval",
        "url": "https://leetcode.com/problems/insert-interval/",
        "category": "Intervals",
        "difficulty": "Medium"
    },
    {
        "title": "Merge Intervals",
        "url": "https://leetcode.com/problems/merge-intervals/",
        "category": "Intervals",
        "difficulty": "Medium"
    },
    {
        "title": "Non Overlapping Intervals",
        "url": "https://leetcode.com/problems/non-overlapping-intervals/",
        "category": "Intervals",
        "difficulty": "Medium"
    },
    {
        "title": "Meeting Rooms",
        "url": "https://leetcode.com/problems/meeting-rooms/",
        "category": "Intervals",
        "difficulty": "Easy"
    },
    {
        "title": "Meeting Rooms II",
        "url": "https://leetcode.com/problems/meeting-rooms-ii/",
        "category": "Intervals",
        "difficulty": "Medium"
    },
    {
        "title": "Minimum Interval to Include Each Query",
        "url": "https://leetcode.com/problems/minimum-interval-to-include-each-query/",
        "category": "Intervals",
        "difficulty": "Hard"
    },
    {
        "title": "Rotate Image",
        "url": "https://leetcode.com/problems/rotate-image/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Spiral Matrix",
        "url": "https://leetcode.com/problems/spiral-matrix/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Set Matrix Zeroes",
        "url": "https://leetcode.com/problems/set-matrix-zeroes/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Happy Number",
        "url": "https://leetcode.com/problems/happy-number/",
        "category": "Math & Geometry",
        "difficulty": "Easy"
    },
    {
        "title": "Plus One",
        "url": "https://leetcode.com/problems/plus-one/",
        "category": "Math & Geometry",
        "difficulty": "Easy"
    },
    {
        "title": "Pow(x, n)",
        "url": "https://leetcode.com/problems/powx-n/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Multiply Strings",
        "url": "https://leetcode.com/problems/multiply-strings/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Detect Squares",
        "url": "https://leetcode.com/problems/detect-squares/",
        "category": "Math & Geometry",
        "difficulty": "Medium"
    },
    {
        "title": "Single Number",
        "url": "https://leetcode.com/problems/single-number/",
        "category": "Bit Manipulation",
        "difficulty": "Easy"
    },
    {
        "title": "Number of 1 Bits",
        "url": "https://leetcode.com/problems/number-of-1-bits/",
        "category": "Bit Manipulation",
        "difficulty": "Easy"
    },
    {
        "title": "Counting Bits",
        "url": "https://leetcode.com/problems/counting-bits/",
        "category": "Bit Manipulation",
        "difficulty": "Easy"
    },
    {
        "title": "Reverse Bits",
        "url": "https://leetcode.com/problems/reverse-bits/",
        "category": "Bit Manipulation",
        "difficulty": "Easy"
    },
    {
        "title": "Missing Number",
        "url": "https://leetcode.com/problems/missing-number/",
        "category": "Bit Manipulation",
        "difficulty": "Easy"
    },
    {
        "title": "Sum of Two Integers",
        "url": "https://leetcode.com/problems/sum-of-two-integers/",
        "category": "Bit Manipulation",
        "difficulty": "Medium"
    },
    {
        "title": "Reverse Integer",
        "url": "https://leetcode.com/problems/reverse-integer/",
        "category": "Bit Manipulation",
        "difficulty": "Medium"
    }
]


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def folder_name(index: int, url: str) -> str:
    slug = slug_from_url(url).replace("-", "_")
    return f"nc{index:03d}_{slug}"


def build_status(problem_id: str, title: str, url: str) -> dict:
    return {
        "id": problem_id,
        "title": title,
        "url": url,
        "points": 0,
        "last_attempt": None,
        "history": [],
    }


def build_notes(problem_id: str, title: str, url: str, category: str, difficulty: str) -> str:
    return f"""# {problem_id} — {title}

## 問題

- **カテゴリ**: {category}
- **難易度**: {difficulty}
- **URL**: {url}

## 計算量

| | |
|---|---|
| **時間** | |
| **空間** | |

## つまずいたポイント

-

## 解法メモ

-

"""


def scaffold_problem(index: int, problem: dict, *, force: bool = False) -> str:
    problem_id = f"nc{index:03d}"
    dir_name = folder_name(index, problem["url"])
    problem_dir = SRC_DIR / dir_name

    if problem_dir.exists() and not force:
        return "skip"

    problem_dir.mkdir(parents=True, exist_ok=True)

    status_path = problem_dir / "status.json"
    notes_path = problem_dir / "NOTES.md"

    status_path.write_text(
        json.dumps(
            build_status(problem_id, problem["title"], problem["url"]),
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    notes_path.write_text(
        build_notes(
            problem_id,
            problem["title"],
            problem["url"],
            problem["category"],
            problem["difficulty"],
        ),
        encoding="utf-8",
    )
    return "create"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate NeetCode 150 problem folders under src/",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=len(NEETCODE_150),
        help="Number of problems to scaffold (default: all 150)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing problem directories",
    )
    args = parser.parse_args()

    if args.limit < 1 or args.limit > len(NEETCODE_150):
        print(f"error: --limit must be between 1 and {len(NEETCODE_150)}", file=sys.stderr)
        return 1

    SRC_DIR.mkdir(parents=True, exist_ok=True)

    created = skipped = 0
    targets = NEETCODE_150[: args.limit]

    for index, problem in enumerate(targets, start=1):
        result = scaffold_problem(index, problem, force=args.force)
        if result == "create":
            created += 1
            print(f"[create] {folder_name(index, problem['url'])}")
        else:
            skipped += 1
            print(f"[skip]   {folder_name(index, problem['url'])}")

    print(f"\nDone: {created} created, {skipped} skipped (limit={args.limit})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
