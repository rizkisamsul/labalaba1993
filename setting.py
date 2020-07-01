import os, json, time, re
from flask import Flask, request, abort
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import json
import hashlib
import datetime

# filename = "data/setting.json"
# with open(filename, 'r') as f:
# 	datastore = json.load(f)


# def login_agent():
# 	return datastore["login_profile"]["user_agent"]