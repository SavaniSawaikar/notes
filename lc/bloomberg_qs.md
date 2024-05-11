GREEDY: pick locally optimum at each step to get a globally optimum soln

# Q1. 1029. Two City Scheduling
A company is planning to interview 2n people. Given the array costs where costs[i] = [aCosti, bCosti], the cost of flying the ith person to city a is aCosti, and the cost of flying the ith person to city b is bCosti.
Return the minimum cost to fly every person to a city such that exactly n people arrive in each city.
- Used a greedy solution which looks at the difference between flying to cities and sorts them, first n go to one city, second n go to the other
- Time complexity is O(N logN) because log N for sorting and N for loop
 
