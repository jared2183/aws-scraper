#
# Client-side python app for our CS 310 Final Project, which is a web
# scraping application. It calls a set of lambda functions in AWS through
# API Gateway. The overall goal of the app is to provide data about a
# link provided by the client. This data can either be one of the following:
#   1) Get all outgoing links
#   2) Get the total word count
#   3) Get the number of occurences of a target word
#
# Authors:
#   Adam Chen, Andres Rojas, Jared Yang, and Timothy Sinaga
#   Northwestern University
#   CS 310 Final Project
#
#   Note: based off of Joe Hummel's client for Project 3
#

import requests
import json

import uuid
import pathlib
import logging
import sys
import os
import base64

from configparser import ConfigParser


############################################################
#
# prompt
#
def prompt():
  """
  Prompts the user and returns the command number

  Parameters
  ----------
  None

  Returns
  -------
  Command number entered by user (0, 1, 2, or 4)
  """
  print()
  print(">> Enter a command:")
  print("   0 => End")
  print("   1 => Outgoing Links")
  print("   2 => Total Word Count")
  print("   3 => Single Word Count")

  cmd = input()

  if cmd == "":
    cmd = -1
  elif not cmd.isnumeric():
    cmd = -1
  else:
    cmd = int(cmd)

  return cmd


############################################################
#
# Outgoing Links
#
def outgoing_links(baseurl):
  """
  Prompts the user for a URL and prints all outgoing links from it

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # prompt the user for a URL:
    #
    print("Enter URL>")
    client_url = input()

    input_data = json.dumps({"url": client_url})

    #
    # call the web service:
    #
    api = '/links'
    url = baseurl + api

    res = requests.get(url, data=input_data)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # deserialize and extract links:
    #
    body = res.json()

    print("Here are the outgoing links:")
    link_count = 1
    for link in body:
      print(f"{link_count}) {link}")
      link_count += 1

    return

  except Exception as e:
    logging.error("outgoing_links() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


############################################################
#
# Total Word Count
#
def total_word_count(baseurl):
  """
  Prompts the user for a URL and prints a total count of all words on the
  page

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # prompt the user for a URL
    #
    print("Enter URL>")
    client_url = input()

    #
    # call the web service:
    #
    api = '/word_count' #TODO: UPDATE THIS IF THE API IS NOT THIS
    url = baseurl + api

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # deserialize and extract word count:
    #
    body = res.json()

    # TODO: May need to adjust this
    print(f"Total word count: {body}")

    return

  except Exception as e:
    logging.error("total_word_count() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

############################################################
#
# Single Word Count
#
def single_word_count(baseurl):
  """
  Prompts the user for a URL and a word of their choice. Prints the amount that
  it appeared on the page

  Parameters
  ----------
  baseurl: baseurl for web service

  Returns
  -------
  nothing
  """

  try:
    #
    # prompt the user for a URL
    #
    print("Enter URL>")
    input_url = input()

    #
    # prompt the user for a word
    #
    print("Enter any word>")
    input_word = input()

    #
    # call the web service:
    #
    api = '/word_occurences' #TODO: UPDATE THIS IF THE API IS NOT THIS
    url = baseurl + api | "/" + input_word

    res = requests.get(url)

    #
    # let's look at what we got back:
    #
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:
        # we'll have an error message
        body = res.json()
        print("Error message:", body)
      #
      return

    #
    # deserialize and extract word coun for inputted wordt:
    #
    body = res.json()

    # TODO: Will need to adjust
    print(f"Total word count for {input_word}: {body}")

    return

  except Exception as e:
    logging.error("single_word_count() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return

############################################################
# main
#
try:
  print('** Welcome to our web scraper app! **')
  print()

  # eliminate traceback so we just get error message:
  sys.tracebacklimit = 0

  #
  # what config file should we use for this session?
  #
  config_file = 'scraperapp-client-config.ini'

  print("Which config file do you wish to use for this session?")
  print("Press ENTER to use default, or")
  print("enter config file name>")
  s = input()

  if s == "":  # use default
    pass  # already set
  else:
    config_file = s

  #
  # does config file exist?
  #
  if not pathlib.Path(config_file).is_file():
    print("**ERROR: config file '", config_file, "' does not exist, exiting")
    sys.exit(0)

  #
  # setup base URL to web service:
  #
  configur = ConfigParser()
  configur.read(config_file)
  baseurl = configur.get('client', 'webservice')

  #
  # make sure baseurl does not end with /, if so remove:
  #
  if len(baseurl) < 16:
    print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
    sys.exit(0)

  if baseurl == "https://YOUR_GATEWAY_API.amazonaws.com":
    print("**ERROR: update config.ini file with your gateway endpoint")
    sys.exit(0)

  lastchar = baseurl[len(baseurl) - 1]
  if lastchar == "/":
    baseurl = baseurl[:-1]

  #
  # main processing loop:
  #
  cmd = prompt()

  while cmd != 0:
    #
    if cmd == 1:
      outgoing_links(baseurl)
    elif cmd == 2:
      total_word_count(baseurl)
    elif cmd == 3:
      single_word_count(baseurl)
    else:
      print("** Unknown command. Please try again.")
    #
    cmd = prompt()

  #
  # done
  #
  print()
  print('** Done **')
  sys.exit(0)

except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)
