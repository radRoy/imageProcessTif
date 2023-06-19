size = 6;
test = newArray(size);
for (i = 0; i < size; i++) {
	test[i] = i;
}
for (i = 0; i < lengthOf(test); i++) {
	print(test[i]);
}
print(lengthOf(test));