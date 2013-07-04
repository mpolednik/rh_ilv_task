#!/usr/bin/env python
# encoding: utf-8

# test cases
tests = []
# 1: simple ilv string with obsolete byte at the end
tests.append('010321DB3FCC')
# 2: simple ilv without obsolete byte (off-by-one checking)
tests.append('0201AC')
# 3: ilv with multiple bytes with obsolete byte at the end
import random
value = ''
for i in range(0, 456*2):
    value += random.choice('0123456789ABCDEF')
tests.append('038201C8'+value+'CC')
print 'Ending byte in test 3: {}'.format(value[-2:])
# 4: ilv with multiple bytes without obsolete byte at the end
import random
value = ''
for i in range(0, 456*2):
    value += random.choice('0123456789ABCDEF')
tests.append('048201C8'+value)
print 'Ending byte in test 4: {}'.format(value[-2:])


def printFormatted(data):

    full_byte = ''
    current_state = 0

    for char in data:
        full_byte += char
        if (len(full_byte) == 2):
            # we've read the whole byte

            if (current_state == 0):
                # setting up, reading id
                value = ''
                length = ''
                id = full_byte
                current_state = 1
            elif (current_state == 1):
                # reading length
                fake_length = int(full_byte, 10) # used to determine whether more bytes should be read
                if (fake_length > 80):
                    ctr = fake_length - 80
                    current_state = 2
                else:
                    length = int(str(fake_length), 16)
                    current_state = 3
            elif (current_state == 2):
                # !!unsure of exact values!!
                if (ctr > 0):
                    length += full_byte
                    ctr -= 1
                    if (ctr == 0):
                        length = int(length, 16)
                        current_state = 3
            elif (current_state == 3):
                # reading value
                value += full_byte
                if (len(value)/2 == length):
                    # outputting, setting state back to 0 (setup)
                    print 'ID: {}\nLENGTH: {}\nVALUE: {}\n'.format(id, length, value)
                    current_state = 0

            # ready to read next byte, clean current one
            full_byte = ''

for test in tests:
    printFormatted(test)
