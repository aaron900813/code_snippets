
import os
import sys
import re
import time
import uuid

import codecs
import hashlib
import base64

sys.path.append("../")
import online_tracking_results_pb2
import online_event_detection_pb2

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../src")
from utils.logging_util import Logger
mlog = Logger.get("com.aibee.mall.v3")

class common_utils():
    store_event_len = 5
    detected_event_len = 10

    @staticmethod 
    def unix2human(ts):
        return time.strftime("%Y%m%d %H:%M:%S", time.localtime(ts / 1000))

    @staticmethod
    def human2unix(ts):
        return long(time.mktime(time.strptime(ts, "%Y%m%d%H%M%S")) * 1000)

    @staticmethod
    def get_time_from_filename(filename):
        channel_timestamp = re.search("ch\d+_\d{14}", filename).group(0)
        timestamp = channel_timestamp.split("_")[1]
        return time.mktime(time.strptime(timestamp, "%Y%m%d%H%M%S")) * 1000

    @staticmethod
    def get_file_hashval(CameraEvents):
        hasher = hashlib.md5()
        hasher.update(CameraEvents.SerializeToString())
        return hasher.hexdigest()

    @staticmethod
    def sort_pb_path(fn_floder):
        pbs_files = [[common_utils.get_time_from_filename(fn) , fn] for fn in os.listdir(fn_floder)]
        pbs_files = sorted(pbs_files, key = lambda k: k[0])
        return [os.path.join(fn_floder, ts_fn[1]) for ts_fn in pbs_files]

    @staticmethod
    def output_html(user_events, store_id, html_path):
        # mlog.info("output_html %s" % (common_utils.build_msg_of_user_events(user_events)))
        with codecs.open(html_path, "w", 'utf-8') as f:
            f.write('''<meta charset="utf-8">''')
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write("</head>\n")   
            f.write("<body>\n")
            user_events_count = 0
            for uid in user_events:
                f.write("<div>")
                f.write("<HR style=\"FILTER: alpha(opacity=100,finishopacity=0,style=2)\" width=\"100%\" color=#987cb9 SIZE=10>")

                f.write('''<table width=%s border="0" cellspaceing="0" cellpadding="0" >''' % (len(user_events[uid]) * 200))
                f.write("<tr>")
                
                for event_info in user_events[uid]:
                    event = event_info["event"]
                    # paired = event_info["paired"]
                    f.write("""<td align="center" valign="middle"/><img src="data:image/jpg;base64, %s" height="300" width="200" ></td>""" % (base64.b64encode(event.box_patches)))
                
                f.write("</tr>")
                f.write("</table>")

                f.write('''<table width=%s border="0" cellspaceing="0" cellpadding="0" >'''% (len(user_events[uid]) * 200))
                f.write("<tr>")
                
                for event_info in user_events[uid]:
                    event = event_info["event"]
                    paired = event_info["paired"]
                    log_str = "%s %s %s %s %s" % (paired, store_id, event.track_id, event.event_type, common_utils.unix2human(event.timestamp))
                    f.write("""<td><p style="word-wrap: break-word; width: 100px;">%s</p></td>""" % (log_str))
                f.write("</tr>")
                f.write("</table>")
                f.write("""<pre>%s %s</pre>""" % (user_events_count, uid))
                f.write("</div>")
                user_events_count += 1
            f.write("</body>\n")
