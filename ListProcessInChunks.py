### Process large lists from API calls into chunks to write to database


### pass in list name (e.g. seq) and chunk size
def chunker(seq, size):
 return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def process(order_items:list) -> None:
### Process using chunker function
    for group in chunker(order_items,10):
        print(group)
        for item in group:
            print('{} in group'.format(item))
            pass
        

### Example
#process(order_items)

order_items = [*range(10,101,1)]
for pos in range(0,len(order_items),10):
    print(pos)
    print(order_items[pos:pos+10])
