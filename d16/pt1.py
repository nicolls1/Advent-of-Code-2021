SOURCE_FILE = 'numbers.txt'


def literal_operator(input_string):
  offset = 0
  found_last = False
  literal_string = ''
  while not found_last:
    found_last |= input_string[offset] == '0'
    literal_string += input_string[offset + 1: offset + 5]
    offset += 5

  return int(literal_string, 2), offset


def packet_operator(input_string):
  offset = 0
  sub_packets = []
  if input_string[0] == '0':
    # next 15 bits is length of body
    length = int(input_string[1:16], 2)
    bits_read = 0
    offset += 16
    while bits_read < length:
      packet = parse_packet(input_string[offset + bits_read:])
      sub_packets.append(packet)
      bits_read += packet['length']
    assert bits_read == length
    offset += bits_read
  else:
    # next 11 bits is length packets
    packets = int(input_string[1:12], 2)
    offset += 12
    while len(sub_packets) < packets:
      packet = parse_packet(input_string[offset:])
      sub_packets.append(packet)
      offset += packet['length']

  return sub_packets, offset


TYPE_OPERATIONS = {
  0: packet_operator,
  1: packet_operator,
  2: packet_operator,
  3: packet_operator,
  4: literal_operator,
  5: packet_operator,
  6: packet_operator,
  7: packet_operator,
}


def parse_packet(input_string):
  packet = {
    'version': int(input_string[:3], 2),
    'type': int(input_string[3:6], 2),
  }
  remaining_input_string = input_string[6:]
  value, bits_read = TYPE_OPERATIONS[packet['type']](remaining_input_string)
  return packet | {
    'value': value,
    'length': bits_read + 6,
  }


def sum_versions(packet):
  current_sum = packet['version']
  if isinstance(packet['value'], list):
    current_sum += sum([sum_versions(sub_packet) for sub_packet in packet['value']])
  return current_sum


def run():
  with open(SOURCE_FILE, 'r') as f:
    line = f.readline().strip()
  input_string = str(bin(int(line, 16)))[2:].zfill(4 * len(line))

  packet = parse_packet(input_string)
  print(sum_versions(packet))


if __name__ == '__main__':
  run()
