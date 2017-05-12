import numpy as np

def recover(cover_data, emb_msg_len): # cover_data is a string list of binary numbers
    msg = ''
    cover_len = len(cover_data)
    lsb_lvl = emb_msg_len // cover_len
    data = np.array([list(x) for x in cover_data])

    for i in range(lsb_lvl):
        msg = msg + ''.join(data[:,31 - i]) 

    rem = emb_msg_len % (cover_len)
    msg = msg + ''.join(data[:rem ,31 - lsb_lvl])

    chunk = 32
    msg_split = [msg[i : i + chunk] for i in range(0, len(msg), chunk)]
    f = open("emb_msg_rec.txt", 'w')
    for i in msg_split:
        f.write(i + '\n')
    return msg_split

