from channels import Group
import json
from ui_channel.upstream import Upstream
from ui_channel.delete_files import delete_logs, delete_raw, delete_reduced
from ui_channel.alerts import Alerts
import datetime
from ui_channel.qlf_state import QLFState

qlf_state = QLFState()
us = Upstream(qlf_state)
alerts = Alerts()


# Connected to websocket.connect
def ws_add(message):
    us.start_uptream()
    # Accept the connection
    message.reply_channel.send({"accept": True})
    message.reply_channel.send({
        "text": json.dumps({
            "status": "connected"
        })
    })
    # Add to the monitor group
    Group("monitor").add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "status": "connected monitor",
            "notification": alerts.available_space()
        })
    })
    Group("monitor").send({
        "text": qlf_state.get_current_state()
    })


# Connected to websocket.receive
def ws_message(message):
    if message.content['text'] == "startPipeline":
        us.start_daemon()
        Group("monitor").send({
            "text": qlf_state.get_current_state()
        })
        return
    if message.content['text'] == "stopPipeline":
        if qlf_state.pipeline_running is not 1:
            us.pipeline_message('Process {} aborted.'.format(
                qlf_state.current_process_id))
        us.stop_daemon()
        qlf_state.update_pipeline_log()
        Group("monitor").send({
            "text": qlf_state.get_current_state()
        })
        return
    if message.content['text'] == "resetPipeline":
        delete_logs()
        us.stop_daemon()
        qlf_state.reset_state()
        us.pipeline_message('Monitor reset.')
        qlf_state.update_pipeline_log()
        message.reply_channel.send({
            "text": qlf_state.get_current_state()
        })
        return
    if message.content['text'] == "deleteAll":
        delete_logs()
        delete_raw()
        delete_reduced()
        return
    if message.content['text'] == "deleteRaw":
        delete_raw()
        us.pipeline_message('Raw files deleted.')
        qlf_state.update_pipeline_log()
        message.reply_channel.send({
            "text": qlf_state.get_current_state()
        })
        return
    if message.content['text'] == "deleteReduced":
        delete_reduced()
        us.pipeline_message('Reduced files deleted.')
        qlf_state.update_pipeline_log()
        message.reply_channel.send({
            "text": qlf_state.get_current_state()
        })
        return
    if message.content['text'] == "deleteLog":
        delete_logs()
        us.pipeline_message('Log files deleted.')
        qlf_state.update_pipeline_log()
        message.reply_channel.send({
            "text": qlf_state.get_current_state()
        })
        return
    # Get Single Camera
    if "camera" in message.content['text']:
        camera = str(message.content['text'].split(":")[1])
        if camera in us.qlf_state.camera_logs.keys():
            message.reply_channel.send({
                "text": json.dumps({
                    "cameralog": us.qlf_state.camera_logs[
                        camera
                    ]
                })
            })
            Group(camera).add(message.reply_channel)

    # User Channel
    if "uuid" in message.content['text']:
        Group(str(message.content['text'].split("uuid=")[1])).add(
            message.reply_channel
        )

        Group(str(message.content['text'].split("uuid=")[1])).send({
            "text": json.dumps({
                "text": "Test single channel"
            })
        })

    Group("monitor").send({
        "text": json.dumps({
            "text": "%s" % message.content['text']
        })
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("monitor").discard(message.reply_channel)
    for cam in us.qlf_state.camera_logs.keys():
        Group(cam).discard(message.reply_channel)
