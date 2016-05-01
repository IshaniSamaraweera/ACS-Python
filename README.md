# ACS-Python
Python program to implement Average Common Substring (ACS) Algorithm

Average Common Substring (ACS) Algorithm
Let A and B be two strings (genomes) of length n and m respectively. For any position i in A, we identify the length of the longest substring L(i) of A, that exactly matches a substring in string B starting at some position j. The longest common substring from B to each position of A computed and averaged to get the measure L(A,B).
L (A,B) = sum of i=1 to i=n of L(i)/n

Intuitively, a large value for L(A,B)represents that the string A and B more similar in nature. If the length of string B is significantly longer than string A, it will affect the L(A,B) value computed in the above equation. Hence, the L(A,B) value is normalized in accordance with the equation given below.  The normalized L(A,B) is also considered a similarity (S) measure between the two strings A and B.
S(A,B) = L(A,B)/log(m)

Using the above equation a distance measure (D) between the two strings A and B are computed as:
D(A,B)=log(m)/L(A,B) - log(n)/L(A,A)

However, the distance measure above is not a symmetric measure. Therefore, we need to compute D(B,A)  and average the value with D(A,B) to get the final ACS measure. 
ACS = {D(A,B)+D(B,A)}/2

The ACS measure requires the implementation of string matching algorithms to find the longest common substring. By this program compute the ACS measure using or adopting suitable string matching algorithm.
