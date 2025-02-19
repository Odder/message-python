## Pre-requisites
Python (tested using 3.13)

## Usage

`python main.py`

This will spin up each individual service and attach it to the same main process such that the they all write to the 
same stdout. If you want you can also spin up each service individually, but this will require you to manually send 
messages about files to read or not.

When the orchestration is running, you will be prompted with:
```
Enter commands in the format: <input_file> <output_file>
Enter command: 
```

this will read the file from the path `file_reader/<input_file>` and output to the path `file_writer/<output_file>`.

I've added some basic error handling regarding connections and such and I am using `EOF` as an end of file marker, which
of course leads to some edge-case issues if you put EOF and the end of a line in your file.

