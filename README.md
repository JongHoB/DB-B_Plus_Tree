# Project : B+Tree

## Goal
Implement a B+Tree with Python


## Problem Specification

- The framework provides an environment to simulate B+tree. Your task is to implement the key components of the B+tree, which is `class B_PLUS_TREE`.
- The framework uses `txt` files to command and show the result. As you can see, `test_bp.txt` is for command and `result.txt` is for the result of the command. The basic case is in `test_bp.txt` and the result should be like `gold.txt`.
- The framework accepts five main commands, which are `INIT`, `EXIT`, `INSERT`, `DELETE`,`ROOT`, `PRINT`, `FIND`, and `RANGE`.

### 1. INIT (Already implemented)
- `INIT K`
- Initialize K-degree b+tree
- Assume that K is odd for convenience.

### 2. EXIT (Already implemented)
- `EXIT`
- Quit the program

### 3. INSERT
- `INSERT A`
- Insert A into B+-tree
- Input: integer A
- Tree rebalancing: Split

### 4. DELETE
- `DELETE A`
- Delete A from B+-tree
- Input: integer A
- Tree rebalancing: Merge

### 5. ROOT
- `ROOT`
- Print root of the tree

### 6. PRINT
- `PRINT`
- Print the tree (print nodes level by level from the root)

### 7. FIND
- `FIND K`
- Find the key from the tree
- Input: integer K
- Output: paths or NONE (if K does not exist)

### 8. RANGE
- `RANGE K(from) K(to)`
- Print all nodes in the range K(from) K(to)

 ## Tips 
- In this Project, every operation is based on this site. https://www.cs.usfca.edu/~galles/visualization/BPlusTree.html
- command example `python bptree_202212345.py < test_bp.txt > result_202212345.txt`
- There could be an error.
