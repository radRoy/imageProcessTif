function doSomething(input) {
	/* function description*/
	print("input is: " + input);
	return input + input;
}

input = "qwer";
input = 3;  // both input argument types work in above function.
output = doSomething(input);
print("output is: " + output);