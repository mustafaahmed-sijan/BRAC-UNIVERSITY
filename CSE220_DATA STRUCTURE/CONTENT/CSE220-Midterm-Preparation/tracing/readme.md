# CSE220 Midterm Preparation

A comprehensive study repository for **CSE220 (Data Structures)** midterm preparation.

This repository contains questions collected from previous midterm papers, additional MCQ practice, Java programming solutions, and theory explanations. The primary goal is to understand the underlying concepts and problem-solving techniques rather than simply memorize solutions.

Most programming solutions include beginner-friendly Java code with comments, Bangla logic explanations, and independent driver methods for testing.

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Source Papers](#source-papers)
3. [Repository Structure](#repository-structure)
4. [MCQ Question Bank](#mcq-question-bank)
5. [Coding Problems and Solutions](#coding-problems-and-solutions)
6. [Theory and Tracing](#theory-and-tracing)
7. [How to Run the Java Programs](#how-to-run-the-java-programs)
8. [Learning Approach](#learning-approach)
9. [Limitations](#limitations)

---

## Repository Overview

| Section | Contents |
|---|---|
| MCQ Question Bank | Original MCQs and additional practice questions |
| Coding Problems | Independent Java solutions for past-paper problems |
| Theory and Tracing | Data structure concepts, complexity and manual tracing |
| Source Appendix | Extracted text from uploaded past papers |

### Main Features

- Original questions from previous CSE220 midterms.
- Additional conceptual and analytical MCQs.
- Java solutions with English code comments.
- Bangla explanations of programming logic.
- Individual folders for individual coding problems.
- Independent `Main.java` files with driver methods.
- Time and space complexity discussions.

## Source Papers

The repository is based on the following uploaded question papers:

| Semester | Source Paper |
|---|---|
| Fall 2023 | FA23 |
| Spring 2024 | SP24 |
| Summer 2024 | SU24 |
| Fall 2024 | FA24 |
| Summer 2025 | SU25 |
| Fall 2025 | FA25 |
| Spring 2026 | SP26 |

The two Fall 2025 PDFs were identified as duplicate versions of the same paper.

## Repository Structure

```text
CSE220-Midterm-Preparation/
│
├── README.md
│
├── 01_MCQ_Question_Bank/
│   │
│   ├── Original_MCQs.md
│   ├── Additional_Practice_MCQs.md
│
├── 02_Coding_Problems/
│   │
│   ├── Fall_2023/
│   │   ├── Q1_Compress_Matrix/
│   │   │   ├── Main.java
│   │   │   └── README.md
│   │   ├── Q2_Pairwise_Equal/
│   │   │   ├── Main.java
│   │   │   └── README.md
│   │   └── Q3_Conditional_Reverse/
│   │       ├── Main.java
│   │       └── README.md
│   │
│   ├── Spring_2024/
│   │   ├── Q1_Sum_Diff/
│   │   ├── Q2_Is_Sum_Possible/
│   │   └── Q3_Dance_Pair/
│   │
│   ├── Summer_2024/
│   │   ├── Q1_Rotate_Outer_Ring/
│   │   ├── Q2_Remove_Duplicates/
│   │   └── Q3_Adjacent_Stack_Swap/
│   │
│   ├── Fall_2024/
│   │   ├── Q1_Zigzag_Traversal/
│   │   ├── Q2_Reverse_And_Swap/
│   │   └── Q3_Merge_Overlapping_Tasks/
│   │
│   ├── Summer_2025/
│   │   ├── Q1_Local_Minima/
│   │   ├── Q2_Sorted_Hash_Insert/
│   │   └── Q3_Deposit_Sum/
│   │
│   ├── Fall_2025/
│   │   ├── Q1_Block_Energy_Sum/
│   │   ├── Q2_Range_Reverse/
│   │   └── Q3_Merge_Stacks/
│   │
│   └── Spring_2026/
│       ├── Q1_Decode_2x2_Traversal/
│       ├── Q2_Send_Pulse/
│       └── Q3_Queue_Group_Reverse/
│
└── 03_Theory_and_Tracing/
    ├── README.md
    └── Original_Paper_Text_Appendix.md
```

Each coding problem folder contains its own `Main.java` and problem-specific `README.md`.

## MCQ Question Bank

Location: `01_MCQ_Question_Bank/`

### Original_MCQs.md

Contains readable original MCQs extracted from the uploaded question papers, including:

- Complete questions and answer options.
- Correct answers.
- Bangla explanations.
- Relevant theoretical concepts.
- Calculation and code-tracing explanations where available.

### Additional_Practice_MCQs.md

Contains 50 additional practice questions across five topics:

1. Arrays and Matrices
2. Linked Lists
3. Stacks and Queues
4. Hash Tables
5. Time and Space Complexity

Questions cover conceptual understanding, analytical thinking, code output, and common exam traps.

## Coding Problems and Solutions

Location: `02_Coding_Problems/`

Currently organized into 21 individual Java programming problem folders.

### Explanation Format

Each problem is organized around the following learning structure:

1. **Problem Explanation:** Understand what the question asks.
2. **Logic Breakdown:** Understand the solution approach in Bangla.
3. **Dry Run:** Trace the important operations.
4. **Java Implementation:** Beginner-friendly code with comments.
5. **Driver Code:** Run the solution independently.
6. **Complexity Analysis:** Time and space complexity.
7. **Exam Variations:** Possible modifications and common mistakes.

### Topics Covered

- Array and Matrix Operations
- Matrix Compression and Traversal
- Linked List Manipulation
- Dummy Headed Linked Lists
- Doubly Linked Lists
- Stack Operations
- Queue Operations
- Hash Table and Separate Chaining
- Sorting and Merging
- Pointer Manipulation

## Theory and Tracing

Location: `03_Theory_and_Tracing/`

This section covers theoretical questions and manual execution exercises, including:

- Row-major array indexing.
- Multidimensional array conversion.
- Stack push and pop sequences.
- Circular queue operations.
- Linked-list pointer tracing.
- Dummy-headed linked lists.
- Doubly circular linked lists.
- Hash functions and collision handling.
- Time and space complexity.

`Original_Paper_Text_Appendix.md` contains extracted text from the uploaded source papers.

## How to Run the Java Programs

Each problem is independent and can be executed separately.

**Requirements:**
- Java JDK installed.
- Visual Studio Code.
- Java Extension Pack (recommended).

**Steps:**

1. Open the desired problem folder in VS Code.
2. Open `Main.java`.
3. Open the VS Code terminal.
4. Compile the program:

```bash
javac Main.java
```

5. Execute:

```bash
java Main
```

Each solution has its own `main()` method, so no additional project configuration is required.

## Learning Approach

This repository is designed for understanding rather than memorization.

Recommended study sequence:

1. Read the relevant theory.
2. Attempt the original MCQs.
3. Understand the Bangla explanation.
4. Try solving the programming problem independently.
5. Compare your approach with the Java implementation.
6. Perform a dry run.
7. Practise variations of the same problem.

## Limitations

This is an evolving study resource.

- Some original paper diagrams require manual verification.
- Some image-based questions may not be fully represented in extracted text.
- Certain programming explanations and dry runs require further expansion.
- Always compare diagram-dependent solutions with the original question paper before relying on them.

**The objective is to build a stronger understanding of Data Structures, Java programming, and CSE220 problem-solving techniques.**

---

*Created for academic learning and CSE220 midterm preparation.*
