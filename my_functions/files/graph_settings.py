#!/usr/bin/env python3

"""Provides all reusable parameters for seaborn graphing."""

import sys
import os
import re
from dataclasses import dataclass

import pandas as pd

@dataclass
class ColorWheel:
    """A dataclass used to store information about hex codes for graphs. 
    Has a name (str) and colors (dictionary)."""
    name: str
    colors: dict[any, str]

def dict_printer(my_dictionary: dict):
    """Prints and formats the contents of a provided dictionary."""
    for key, value in my_dictionary.items():
        print(f"{key}: {value}")

def get_default_colors() -> ColorWheel:
    """Returns the default colors for the Pantone Spring Summer 2025 color scheme."""
    default_colors = ["#A66E4A",
                      "#93B7D5",
                      "#C67FAE",
                      "#A6BE47",
                      "#D7E8BC",
                      "#F3EAC3",
                      "#98DDDF",
                      "#009499",
                      "#F7EF70",
                      "#2E5283",
                      "#F6745F",
                      "#6F8D6A",
                      "#AC6C29",
                      "#E3BD33",
                      "#DE3848",
                      "#E2552D",
                      "#6D5698",
                      "#582B36"]
    return default_colors

def get_white_wheel(dataset: pd.DataFrame, 
                    pop_value: str = "") -> dict:
    """Generates a white color wheel based on the values in the provided DataFrame. 
    A 'pop' value may be provided to remove extra data columns before processing."""
    
    treat_type = dataset.copy()
    treat_type = treat_type.pop(pop_value)
    white_wheel = ColorWheel("white_wheel", {})
    
    for treat in treat_type: 
        white_wheel.colors.setdefault(treat, '#FFFFFF')
    return white_wheel.colors

def get_default_wheel() -> dict:
    """Generates a ColorWheel object with the name "default" 
    and the original color wheel provided by Sidd."""

    def_color_wheel = ColorWheel("default", dict([
    ("Cut_nod", '#cc4273'),
    ("Cut_SS", '#f1c4c8'),
    ("Acral", '#4b81bf'),
    ("Subungual", '#F6C163'),
    ("Muc_ano", '#29636C'),
    ("Muc_nasal", '#BCDBE8'),
    ("Muc_vul", '#7C4480'),
    ("Unknown", '#BA412E'),
    ("Other", '#A36E37'),
    ("Unde", '#3ca858'),
    (10, '#215996'),
    (11, '#c1db3c'),
    (12, '#C1AFCD'),
    (13, '#BCDBE8'),
    (14, '#B54062'),
    (15,'#BCDBE8'),
    (16,'#f1c4c8')
    ]))
    return def_color_wheel.colors
    
def get_data_path(filename: str) -> str:
    """Gets the file path of the current directory and appends 
    /datasets/ to allow for file organization."""
    full_path = os.getcwd() + "/datasets/" + filename
    return full_path

def get_file_from_cmd(position: int=1):
    """Opens a specified file from a command line argument. 
    The position parameter defines which argument the filename is passed in."""
    filename = get_data_path(sys.argv[position])
    try:
        return open((filename), "r", encoding="utf-8")
    except FileNotFoundError as n:
        print("File not found. Double check spelling and/or directory path.")
        print(n)
        return sys.exit(1)

def my_output_file(filename: str, 
                   plot_type: str ="Plot", 
                   extension: str="svg") -> str:
    """Creates a regex to rename the output file based on the original 
    .csv file. The plot type adds the name of the plot to the filename, 
    and the extension specifies what file format to save (svg, png, jpeg,
    or pdf)."""
    try:
        if extension in ["svg", "png", "pdf","jpeg","jpg"]:
            just_name = filename.split("/")
            new_name = re.sub(".csv$",
                              "_Image" + plot_type + "." + extension,
                              just_name[::-1][0],
                              1)
            return os.getcwd() + "/generated_images/" + new_name
    except ValueError as e:
        print(e)
        return sys.exit(1)

