#!/usr/bin/env python3

"""A sandbox script for learning argparse functions."""

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is a test of the " \
    "argparse library for my own understanding")
    parser.add_argument('-name',default=None,dest='user_name',type=str,help='CSV')
    