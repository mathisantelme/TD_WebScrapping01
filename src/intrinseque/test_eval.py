from cleaneval_tool import *
import re, sys

test_file = sys.argv[1]
clean_file = sys.argv[2]
print(evaluate_file(test_file, clean_file))
