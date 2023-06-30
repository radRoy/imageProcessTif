string = "abc,def,ghi";
print(startsWith(string, "bc"));
print(startsWith(string, "abc"));

files = newArray("id04-img_Ch561nm.tif", "id05-img_Ch488nm.tif", "id05-img_Ch561nm.tif", "id06-img_Ch561nm.tif");

for (i = 0; i < files.length; i++)
{
	if (! startsWith(files[i], "id05-img_Ch561nm")) {print("continuing"); continue;}
	print(files[i]);
}