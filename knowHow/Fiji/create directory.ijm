/*
 * author: Daniel Walther
 * creation date: 7.8.2023
 * file purpose: testing the creation of directories.
 * - find a function. does it work?
 * - what does it do if dir exists already? (function's desired behaviour: do nothing)
 */


//path = "C:\Users\popsicle_cell\Documents\testdir";
path = "C:/testdir";
File.makeDirectory(path);
	// function requires slashes as directory delimiter