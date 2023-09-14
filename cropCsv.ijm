// script for cropping: getting the relevant information from desired files and writing them to a .csv


filePaths = newArray("specimen01.tif", "specimen02.tif", "specimen03.tif");
headers = newArray("filename", "x_size", "y_size", "z_size", );
delim = ",";
csvString = "";

for (i = 0; i < filePaths.length; i++)
{
	row = newArray();
	for (j = 0; j < headers.length; j++)
	{
		if (headers[j] == "filename")
		{
			row[j] = filePaths[i];
			continue;
		}
		row[j] = headers[j];
	}
	rowString = String.join(row, delim);
	print("rowString: " + rowString);
	csvString = csvString + rowString + "\n";
}

print("  csvString:\n", csvString);
