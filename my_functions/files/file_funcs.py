#!/usr/bin/env python3
"""All reused functions across the viralogue-repo."""

def tab_separator(my_file: str, 
                  delimiter: str="\t",
                  header: bool=False) -> list[str]:
    """Separates a delimited file into a list object. The delimiter can be specified, 
    but tab is the default."""
    return_list = []
    with open(my_file,"r",encoding="utf-8") as f:
        for idx, line in enumerate(f.readlines()):
            if (header) and (idx == 0):
                pass
            else:
                return_list.append(line.strip().split(delimiter))
    f.close()
    return return_list

def write_dict_to_file(my_filename: str, my_dict: dict, delimiter: str="\t", 
                       keep_flags: bool=False):
    """Outputs the contents of a dictionary to a specified file.\n
    my_filename: the desired filename (if no path specified, it will output to the 
    current directory)\n my_dict: the dictionary to print out\n
    delimiter (default tab): the delimiter to space between keys and values\n
    keep_flags (default False): adds 'key' and 'value' to each column for troubleshooting."""
    with open(my_filename, "w") as f:
        if not keep_flags:
            for key,value in my_dict.items():
                f.write(key + delimiter + str(value) + "\n")
        else:
            for key,value in my_dict.items():
                print("key: " + key + delimiter + "value" + str(value) + "\n")
                
                           
