#set.seed(230509)
#set.seed(230626)
#set.seed(240111)  # dataset04.b-c
#set.seed(240120)  # dataset10.a class balancing
set.seed(240123)  # dataset10.b train/val/test division

## dataset04.b-c
#n_files <- 7
#print(numbers_blind <- sample.int(n_files, replace = FALSE))

### dataset10.a class balancing
## id01
#n_majority <- 10
#n_minority <- 8
#id01 <- sample(n_majority, n_minority, replace = FALSE)
## id02
#n_majority <- 13
#n_minority <- 6
#id02 <- sample(n_majority, n_minority, replace = FALSE)
## id03
#n_majority <- 11
#n_minority <- 8
#id03 <- sample(n_majority, n_minority, replace = FALSE)
## id04
#n_majority <- 15
#n_minority <- 6
#id04 <- sample(n_majority, n_minority, replace = FALSE)
## id05
#n_majority <- 11
#n_minority <- 7
#id05 <- sample(n_majority, n_minority, replace = FALSE)
## id06
#n_majority <- 12
#n_minority <- 6
#id06 <- sample(n_majority, n_minority, replace = FALSE)
## id07
#n_majority <- 20
#n_minority <- 3
#id07 <- sample(n_majority, n_minority, replace = FALSE)
#
#print(sort(id01))  #[1]  1  2  3  4  6  7  9 10
#print(sort(id02))  #[1]  1  3  4  6 12 13
#print(sort(id03))  #[1]  3  5  6  7  8  9 10 11
#print(sort(id04))  #[1]  7 10 11 12 14 15
#print(sort(id05))  #[1]  2 4 5 6 7 8 9
#print(sort(id06))  #[1]  2  3  4  5  7 11
#print(sort(id07))  #[1]  5 18 20


### dataset10.a train val division
#n_files <- 7
#print(numbers_blind <- sample.int(n_files, replace = FALSE))  # [1] 3 4 2 7 6 1 5

## dataset10.b train val division
n_files <- 7
print(numbers_blind <- sample.int(n_files, replace = FALSE))  # [1] 2 3 5 7 6 4 1
# => train=id02,03,05,07,06, val=id04, test=id01 in dataset10.b.0 (aka dataset10.b)
# => train=id02,03,05,04,01, val=id07, test=id06 in dataset10.b.1
# => train=id02,07,06,04,01, val=id03, test=id05 in dataset10.b.2