# This calculated a rounded version of the notes in midi. 
# Take into account that this starts in 21 but the arraw starts from 0
# you have to substract 21 to the notes you get from the code, to match
# this!, be careful.
# http://newt.phys.unsw.edu.au/jw/notes.html


n = 87
note_list = [None] * n


m = 21
for i in range(0,n):
    # print(  (m - 69))
    # print(  (m - 69)/12.0 )
    # print(  2**( (m - 69)/12.0) )
    # print(  ( 2**( (m - 69)/12.0) ) * (440) )
    note_list[i] = round(( 2**( (m - 69)/12.0) ) * (440))
    
    m = m + 1

# Print the rounded notes
print(note_list)