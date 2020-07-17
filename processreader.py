import json 
import glob
import subprocess
from config import HOME

get = lambda cmd: subprocess.check_output(cmd).decode("utf-8").strip()

def mozlz4_to_text(filepath):
    """ Given the path to a "mozlz4", "jsonlz4", "baklz4" etc. file, 
    return the uncompressed text."""   
    try:
        bytestream = open(filepath, "rb")
        bytestream.read(8)  # skip past the b"mozLz40\0" header
        valid_bytes = bytestream.read()
        import lz4.block
        text = lz4.block.decompress(valid_bytes)
        jdata = json.loads(text)
        return jdata
    except Exception as e:
        return 

def check_wtype(w_id):
    # check the type of window; only list "NORMAL" windows
    return "_NET_WM_WINDOW_TYPE_NORMAL" in get(["xprop", "-id", w_id])

def fetch_links_firefox():
    """ Returns a dictionary of all tabs currently opened in firefox along with their URLS.
    E.g. {'Facebook – log in or sign up': 'https://www.facebook.com/'}} """

    dic={}
    temp1 = HOME+".mozilla/firefox/*.default*" 
    temp2 = glob.glob(temp1) # generates all available sub-directories having pattern as temp1
    name = "/sessionstore-backups/recovery.jsonlz4"
    filepath = [x+name for x in temp2]
    
    for file in filepath:
        # print(file)
        jdata = mozlz4_to_text(file)
        if jdata is not None: 
            for win in jdata.get("windows"):
                for tab in win.get("tabs"):
                    # print(tab.get("entries"))
                    i = tab.get("index") - 1
                    if tab.get("entries")[i].get("title").strip() != None:
                        # print(tab.get("entries")[i].get("title"), tab.get("entries")[i].get("url"))
                        dic[tab.get("entries")[i].get("title")] = tab.get("entries")[i].get("url") # Add title corresponding to URL in dictionary
    return dic
# Make similar for vivaldi and chrome


if __name__ == "__main__":
    dic = fetch_links_firefox()
    print(dic)
