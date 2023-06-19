print("");  // prints an empty line incl. newline, for easy reading of output
size = 10
stringList = newArray(size);

for (i = 0; i < size; i++) {
	//stringList[i] = String.append(str);"der";  // fancy, not required
	stringList[i] = "derr" + i;
}

for (i = 0; i < size; i++) {
	print(stringList[i]);
}
