
def base36decode(input):

  c = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  rv = pos = 0
  charlist = list(input)
  charlist.reverse()
  
  for char in charlist:
    rv += c.find(char) * 36**pos
    pos += 1
  return rv

def base36encode(input):
  c = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  rv = ""
  while input != 0:
    rv = c[ input % 36 ] + rv
    input /= 36
  return rv

