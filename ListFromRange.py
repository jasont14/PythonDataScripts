###Creates a range
ml_r = range(10,20,1)
print(ml_r)

### asterisk '*' unpacks the range into a list. Otherwise it is stored as a range
ml = [*range(10,20,1)]
print(ml)

### use extend to unpack range
ml_extend = []
  
# Value to begin and end with
start, end = 10, 20
  
# Check if start value is smaller than end value
if start < end:
    # unpack the result
    ml_extend.extend(range(start, end))
    # Append the last value
    ml_extend.append(end)
  
# Print the list
print(ml_extend)
