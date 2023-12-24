from MIDI import MIDIFile

def parse(file):
    c=MIDIFile(file)
    c.parse()
    print(str(c))
    for idx, track in enumerate(c):
        track.parse()
        print(f'Track {idx}:')
        
        for line in track:
            print('\t'+str(line))
            print('\t\t'+str(line.time)+'\t'+str(line.header)+'\t'+str(line.data) )
            print('\t\t\t'+str(line.message))
            try:
                print('\t\t\t'+str(line.message.note)+"  "+str(line.message.onOff))
            except:
                pass

def generate_sound_list(file):
    c=MIDIFile(file)
    c.parse()
    print(str(c))
    
    song_list = []
    bpm = 130
    ticks = 128
    seg_per_ticks = 60/(bpm*ticks)
    
    
    
    for idx, track in enumerate(c):
        track.parse()
        print(f'Track {idx}:')
        prev_time = 0
        prev_note = 0
        for line in track:
            
            try:
                if line.message.onOff == "ON":
                    print(f"delta: {line.time - prev_time}")
                    delta = line.time - prev_time
                    
                    if delta > 0 and prev_note >= 21 and prev_note <= 108:
                        song_list.append((prev_note, round(delta*seg_per_ticks,2)))
                    
                    prev_time = line.time
                    prev_note = int(line.data[0])
                    
                    
                    
                    print(int(line.data[0]))
                    print(int(line.data[1]))
                    print(f"{line.message.onOff} {line.message.note}")
                    print()
            
            except:
                print(str(line))
                prev_time = line.time
    
    print(song_list)
            
           


# parse("test2.mid")
generate_sound_list("basic.mid")
