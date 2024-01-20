#set.seed(230509)
#set.seed(230626)
#set.seed(240111)  # dataset04.b-c
set.seed(240120)  # dataset10.a class balancing

## dataset04.b-c
#n_files <- 7
#print(numbers_blind <- sample.int(n_files, replace = FALSE))

## dataset10.a class balancing
# id01
n_majority <- 10
n_minority <- 8
id01 <- sample(n_majority, n_minority, replace = FALSE)
# id02
n_majority <- 13
n_minority <- 6
id02 <- sample(n_majority, n_minority, replace = FALSE)
# id03
n_majority <- 11
n_minority <- 8
id03 <- sample(n_majority, n_minority, replace = FALSE)
# id04
n_majority <- 15
n_minority <- 6
id04 <- sample(n_majority, n_minority, replace = FALSE)
# id05
n_majority <- 11
n_minority <- 7
id05 <- sample(n_majority, n_minority, replace = FALSE)
# id06
n_majority <- 12
n_minority <- 6
id06 <- sample(n_majority, n_minority, replace = FALSE)
# id07
n_majority <- 20
n_minority <- 3
id07 <- sample(n_majority, n_minority, replace = FALSE)

print(sort(id01))
print(sort(id02))
print(sort(id03))
print(sort(id04))
print(sort(id05))
print(sort(id06))
print(sort(id07))
#> print(sort(id01))
#[1]  1  2  3  4  6  7  9 10
#
#> print(sort(id02))
#[1]  1  3  4  6 12 13
#
#> print(sort(id03))
#[1]  3  5  6  7  8  9 10 11
#
#> print(sort(id04))
#[1]  7 10 11 12 14 15
#
#> print(sort(id05))
#[1] 2 4 5 6 7 8 9
#
#> print(sort(id06))
#[1]  2  3  4  5  7 11
#
#> print(sort(id07))
#[1]  5 18 20