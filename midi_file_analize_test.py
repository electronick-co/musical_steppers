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
    track_num = 0;
    
    
    for idx, track in enumerate(c):
        track.parse()
        print(f'Track {idx}:')
        prev_time = 0
        prev_note = 0
        song_list.append([])
        for line in track:
            
            try:
                if line.message.onOff: # == "ON":
                    print(f"delta: {line.time - prev_time}")
                    delta = line.time - prev_time
                    
                    if delta > 0 and prev_note >= 21 and prev_note <= 108:
                        #song_list[track_num].append((prev_note, round(delta,2)))
                        pass
                    
                    song_list[track_num].append([line.time, int(line.data[0]), line.message.onOff ])
                    
                    prev_time = line.time
                    prev_note = int(line.data[0])
                    
                    
                    
                    print(int(line.data[0]))
                    print(int(line.data[1]))
                    print(f"{line.message.onOff} {line.message.note}")
                    print()
            
            except:
                print(str(line))
                prev_time = line.time
        track_num = track_num + 1
    
    
    #Solve timeline on track#2
    base_timeline = song_list[1][0][0]
    for i in range(len(song_list[1])):
        song_list[1][i][0] =  song_list[1][i][0] - base_timeline 
            
    print(song_list[0])
    print(song_list[1])
    
    # We have to take the list, convert it into one
    
    mixed_song = []
    
    flag_process = True
    
    len_t1 = len(song_list[0])
    i_1 = 0
    len_t2 = len(song_list[1])
    i_2 = 0
    
    POS_TIMELINE = 0
    POS_NOTE = 1
    POS_ONOFF = 2
    
    # Structure of new list. [ Delay until new event, bool - change on channel 1, midi note 1, bool - change on channel 2, midi note 2]
    
    while flag_process:
        
        if (i_1 + 2) > len_t1 or (i_2 + 2) > len_t2: #TODO this should be review as it will cut it in the shorterst track lenght
            flag_process = False
            print("Take a break!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
            break
        else:
            print(f"i1 = {i_1}/{len_t1}, i2= {i_2}/{len_t2}")
        
        # Check if both have events in the same timeline
        if song_list[0][i_1][POS_TIMELINE] == song_list[1][i_2][POS_TIMELINE]:
            
            current_timeline = song_list[0][i_1][POS_TIMELINE]
            
            # Select the midi note of both (making sure if is on or off.) 
            midi_note_1 = 0
            midi_note_2 = 0
            if song_list[0][i_1][POS_ONOFF] == "ON":
                midi_note_1 = song_list[0][i_1][POS_NOTE]
            if song_list[1][i_2][POS_ONOFF] == "ON":
                midi_note_2 = song_list[1][i_2][POS_NOTE]
            
            # Review delta
            if song_list[0][i_1 + 1][POS_TIMELINE] >= song_list[1][i_2 + 1][POS_TIMELINE]:
                delta = song_list[0][i_1 + 1][POS_TIMELINE] - current_timeline
            else:
                delta = song_list[1][i_2 + 1][POS_TIMELINE] - current_timeline
            
            mixed_song.append(  [ round(delta*seg_per_ticks,2),1,midi_note_1,1,midi_note_2])

            print(f"case 1: delta: {delta}")
            
            # Increase the index on both
            i_1 = i_1 + 1
            i_2 = i_2 + 1
        
        # Check if track 1 is closer than track 2 
        elif song_list[0][i_1][POS_TIMELINE] < song_list[1][i_2][POS_TIMELINE]:
            
            current_timeline = song_list[0][i_1][POS_TIMELINE]
            # Select the midi note of both (making sure if is on or off.) 
            midi_note_1 = 0
            if song_list[0][i_1][POS_ONOFF] == "ON":
                midi_note_1 = song_list[0][i_1][POS_NOTE]
            
            # Review delta
            if song_list[0][i_1 + 1][POS_TIMELINE] < song_list[1][i_2 + 1][POS_TIMELINE]:
                delta = song_list[0][i_1 + 1][POS_TIMELINE] - current_timeline
            else:
                delta = song_list[1][i_2 + 1][POS_TIMELINE] - current_timeline # The comparison is between the current time.
            
            
            mixed_song.append(  [ round(delta*seg_per_ticks,2),1,midi_note_1,0,0])
            
            print(f"case 2: delta: {delta}")
        
            # Increase the index on track 1
            i_1 = i_1 + 1
            
            # track 2 is the one.
        else:
            current_timeline = song_list[1][i_2][POS_TIMELINE]
            # Select the midi note of both (making sure if is on or off.) 
            midi_note_2 = 0
            if song_list[1][i_2][POS_ONOFF] == "ON":
                midi_note_2 = song_list[1][i_2][POS_NOTE]
            
            # Review delta
            if song_list[0][i_1 + 1][POS_TIMELINE] > song_list[1][i_2 + 1][POS_TIMELINE]:
                delta = song_list[0][i_1 + 1][POS_TIMELINE] - current_timeline
            else:
                delta = song_list[1][i_2 + 1][POS_TIMELINE] - current_timeline # The comparison is between the current time.
            
            
            mixed_song.append(  [ round(delta*seg_per_ticks,2),1,midi_note_2,0,0])
            
            print(f"case 3: delta: {delta}")
        
            # Increase the index on track 1
            i_2 = i_2 + 1

    print("------------")
    print(mixed_song)
           


# parse("basic.mid")

generate_sound_list("basic.mid")
