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
n_minority <- 9
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

print(id01)
print(id02)
print(id03)
print(id04)
print(id05)
print(id06)
print(id07)
#> print(id01)
#[1]  2 10  4  9  3  7  1  6
#
#> print(id02)
#[1]  6  4  3 13 12  1  7 11  5
#
#> print(id03)
#[1]  9  8  3 11  7  4  6  2
#
#> print(id04)
#[1] 11  7 14 12  8  6
#
#> print(id05)
#[1]  2  4  8  5  9 10 11
#
#> print(id06)
#[1]  5  2  3  7 11 12
#
#> print(id07)
#[1] 18  8 15