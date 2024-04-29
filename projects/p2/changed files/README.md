# Project 2: Loan Analysis

## Corrections/Clarifications

* none yet

## Overview

Sadly, there is a long history of lending discrimination based on race
in the United States.  Lenders have literally drawn red
lines on a map around certain neighborhoods where they would not
offer loans, based on the racial demographics of those neighborhoods
(read more about redlining here: https://en.wikipedia.org/wiki/Redlining).
In 1975, congress passed the Home Mortgage Disclosure Act (HDMA) to
bring more transparency to this injustice
(https://en.wikipedia.org/wiki/Home_Mortgage_Disclosure_Act).  The
idea is that banks must report details about loan applications and
which loans they decide to approve.

The public HDMA dataset spans all the states and many years, and is documented here:
* https://www.ffiec.gov/hmda/pdf/2020guide.pdf
* https://cfpb.github.io/hmda-platform/#hmda-api-documentation

In this project, we'll analyze every loan application made in Wisconsin in
2020.

Things you'll practice:
* classes
* large datasets
* trees
* testing
* writing modules

There's a lot of new stuff here, and students have often reported back
that P2 is the hardest of the semester, so we encourage you to start
early.

## Testing

Run `python3 tester.py mp2.ipynb` often and work on fixing any issues.

## Submission

As last time, your notebook should have a comment like this:

```python
# project: p2
# submitter: ????
# partner: none
# hours: ????
```

You'll hand in 4 files:
* mp2.ipynb
* loans.py (first module developed in lab)
* module_tester.py
* search.py (second module developed in lab)

Combine these into a zip by running the following in the `p2` directory:

```
zip ../mp2.zip mp2.ipynb loans.py search.py module_tester.py
```

Hand in the resulting mp2.zip file.  Don't zip a different way (our
tests won't run if you have an extra directory inside your zip, for
example).

# Group Part (75%)

For this portion of the project, you may collaborate with your group
members in any way (even looking at working code).  You may also seek
help from 320 staff (mentors, TAs, instructor).  You <b>may not</b>
seek help from other 320 students (outside your group) or
anybody outside the course.

## Part 1: Loan Classes

Finish the `Applicant` and `Loan` classes from [Lab 3](Lab3/loans) (if you haven't already done so).  

We'll now add a `Bank` class to `loans.py`.  A `Bank` can be created like this (create a class with the necessary constructor for this to work):

```python
uwcu = loans.Bank("University of Wisconsin Credit Union")
```

### banks.json

The `__init__` constructor of your `Bank` class should check that the given name appears in the `banks.json` file. If the name does not exist, raise a ValueError exception. The constructor should also lookup the `lei` ("Legal Entity Identifier") corresponding to the name and store that in an `lei` attribute as a string.  In other words, `uwcu.lei` should give the LEI for UWCU, in this case "254900CN1DD55MJDFH69".

### wi.zip

Add a new method to your Bank class called `load_from_zip` that takes in an argument `path`. If your zip file is located in the current directory, you should be able to call your method like this:
```python
uwcu.load_from_zip("./wi.zip")
```

The `load_from_zip` 'path' argument points to the file location (a.k.a. the path) of the `wi.zip` file. When the `load_from_zip` method is called, your program should read and process the CSV file inside `wi.zip`. You already learned how to read text from a zip file in lab using `TextIOWrapper` and the `zipfile` module.

When your `load_from_zip` method loops over the loan `dict`s, it should skip any that don't match the bank's `lei`.  The loan dicts that match should get converted to `Loan` objects and appended to a list, stored as an attribute in the `Bank` object.

Read the documentation and example for how to read CSV files with `DictReader` [here](https://docs.python.org/3/library/csv.html#csv.DictReader).  You can combine this with what you learned about zipfiles.  When you create a `DictReader`, just pass in a `TextIOWrapper` object instead of a regular file object.



### Special Methods

We don't tell you what to call the attribute storing the loans, but you should be able to print the last loan like this:

```python
print(uwcu.SOME_ATTRIBUTE_NAME[-1])
```

Where 'SOME_ATTRIBUTE_NAME' is your chosen attribute name. We can check how many loans there are with this command:

```python
print(len(uwcu.SOME_ATTRIBUTE_NAME))
```

For convenience, we want to be able to directly use brackets and `len` directly on `Bank` objects, like this:
* `uwcu[-1]`
* `len(uwcu)`

Add the special methods to `Bank` necessary to make this work.

### Testing

Running `python3 tester.py mp2.ipynb` does two things:

1. compute a score based on whether answers in your `mp2.ipynb` are correct
2. get a second score by running `module_tester.py`, which exercises various classes/methods in `loan.py` (already done) and `search.py` (the next part)

Your total score is an average of these two components.

Try running `module_tester.py` now.  You should see the following (assuming you haven't worked ahead on `search.py`):

```
{'score': 40.0, 'errors': ['could not find search module']}
```

It should actually be possible to get 50.0 from `module_tester.py`
after just completing `loans.py`, but we left some tests undone so you
can get some practice writing tests for yourself.

Open `module_tester.py` and take a look at the `loans_test`.  The
function tries different things (e.g., creating different `Loan` and
`Applicant` objects and calling various methods).

Whenever something works, a global variable `loans_points` is
increased.  There are also asserts, and if any fail, the test stops
giving points.  For example, here's a bit that tests the `lower_age`
method:

```python
    # lower_age
    assert loans.Applicant("<25", []).lower_age() == 25
    assert loans.Applicant("20-30", []).lower_age() == 20
    assert loans.Applicant(">75", []).lower_age() == 75
    loans_points += 1
```

You should add some additional test code of your choosing (based on
where you think bugs are most likely to occur).  When the additional
code shows that `loans.py` works correctly, it should add 4 points to
`loan_points`.  You could do this in one step (`loans_points += 4`),
or better, divide the points over the testing of a few different
aspects.

## Part 2: Binary Search Tree

Finish the `Node` and `BST` classes from [lab 4](Lab4/) (if you haven't already done so). 

**Note:** if we haven't gotten to BSTs in lecture and lab yet, you can still work on some of the questions in parts 3 and 4, but you should wait to work on the ones related to trees.

**Before you move on to Part 3 ...** 

Add a special method to `BST` so that if `t` is a `BST` object, it is possible to lookup items in `t` with `t["some key"]` instead of `t.root.lookup("some key")`. Check out the __getitem__ documentation [here](https://docs.python.org/3/reference/datamodel.html#object.__getitem__).

## Part 3: "Charles Schwab Bank, SSB" Analysis

For the following questions, create a `Bank` object for the bank named "Charles Schwab Bank, SSB".

### Q1: what is the average interest rate for the bank?

In the Bank class, create an `average_interest_rate()` method that returns the average interest rate. Include the missing loans where the interest rate is not specified in your calculation. What is the average interest rate for the "Charles Schwab Bank, SSB"?

### Q2: how many applicants are there per loan, on average?

In the bank class, create a `num_applicants()` method that returns the number of applicants (the method should not return the average). A loan with an applicant and a co-applicant is considered a loan with two applicants. On `average`, how many loan applicants are there for the "Charles Schwab Bank, SSB"? Use your new method and find a way to count the number of loans to compute the average.

### Q3: what is the distribution of ages for loan recipients?

Create an `ages_dict()` method that returns a dictionary with the keys as the SORTED, from lowest start value to highest start value, age range with values that correspond to the counts of different age ranges. Make sure to filter any instances that have unrealistic ages, such as `8888` or `9999`. For example (the values here are examples, and do not reflect the actual data):

```
{'<25': 2, '25-34': 31, '35-44': 28, ...}
```
Your answer to Q3 should be your dictionary object.

### Tree of Loans for Q4 and Q5

For the following questions, create a `BST` tree.  Loop over every loan in the bank, adding each to the tree.  The `key` passed to the `add` call should be the `.interest_rate` of the `Loan` object, and the `val` passed to `add` should be the `Loan` object itself.

### Q4: how many interest rate values are missing?

Don't loop over every loan to answer.  Use your tree to get and count loans with missing rates (that is, `-1`).

### Q5: how tall is the tree?

The height is the number of edges in the path from the root to the deepest node.  Write a recursive method or function called `get_height(...)` that returns the height of the tree as the answer.

# Individual Part (25%)

You have to do the remainder of this project on your own.  Do not
discuss with anybody except 320 staff (mentors, TAs, instructor).

## Part 4: University of Wisconsin Credit Union Analysis

Build a new `Bank` and corresponding `BST` object as before, but now for "University of Wisconsin Credit Union".

### Q6: how long does it take to add the loans to the tree?

Answer with a plot, where the x-axis is how many loans have been added so far, and the y-axis is the total time that has passed so far.  You'll need to measure how much time has elapsed (since the beginning) after each `.add` call using the difference (-) between the time recorded before the call and the time recorded after the call. The `time.time()` documentation [here](https://docs.python.org/3/library/time.html) will be useful.

**Note:** performance and the amount of noise will vary from one virtual machine to another, so your plot probably won't be identical (this applies to the other performance plots too).

<img src="q6.png">

### Q7: how fast are tree lookups?

Create a bar plot with two bars:
1. time to find missing `interest_rate` values (`-1`) by looping over every loan and keeping a counter
2. time to compute `len(NAME_OF_YOUR_BST_OBJECT[-1])`

<img src="q7.png">

### Q8: How many applicants indicate multiple racial identities?

Answer with a bar graph, where the y axis should represent the number of applicants with the corresponding x-axis representing the number of race selections. Be sure to label your axes.

**Note:** The x-axis should be the number of race identities selected by the applicants, not the individual races. Please keep all number of race selections (Do NOT exclude bars that have less than or equal to one race selection).

### Q9: How many leaf nodes are in the tree?

Write a recursive function or method `num_nonleaf_nodes(...)` to count the number of non-leaf nodes present in the given BST. Use this method to calculate the number of leaf nodes by subtracting the result of running `num_nonleaf_nodes(...)` from the total number of nodes. The answer you should return for Q9 is the number of leaf nodes.

### Q10: What is the fourth largest interest rate in the Bank BST?

Write a **recursive** function or method that can return the top 4 (or N) keys for any subtree.

