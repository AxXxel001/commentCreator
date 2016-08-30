#! /usr/bin/python
#coding: utf-8

import pystache

print pystache.render("Hello, {{planet}}!", {"planet": "World"})