#!/usr/bin/python
# add symbolic names to read_msr / write_msr in trace
# decode_msr msr-index.h < trace
import sys
import re

msrs = {}

with open(sys.argv[1] if len(sys.argv) > 1 else "msr-index.h", "r") as f:
	for j in f:
		if m := re.match(r'#define (MSR_\w+)\s+(0x[0-9a-fA-F]+)', j):
			msrs[int(m[2], 16)] = m[1]

extra_ranges = (
	( "MSR_LASTBRANCH_%d_FROM_IP", 0x680, 0x69F ),
	( "MSR_LASTBRANCH_%d_TO_IP", 0x6C0, 0x6DF ),
	( "LBR_INFO_%d", 0xdc0, 0xddf ),
)

for j in sys.stdin:
	if m := re.search(r'(read|write)_msr:\s+([0-9a-f]+)', j):
		r = None
		num = int(m[2], 16)
		if num in msrs:
			r = msrs[num]
		else:
			for er in extra_ranges:
				if er[1] <= num <= er[2]:
					r = er[0] % (num - er[1],)
					break
		if r:
			j = j.replace(" " + m[2], f" {r}(" + m[2] + ")")
	m = re.search(r'(read|write)_msr:\s+([0-9a-f]+)', j)


