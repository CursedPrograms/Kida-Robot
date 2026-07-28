# camera_actions.py — remote-controller stand-in for the robot's
# camera_actions module (which imports picamera2 and talks to real hardware).
#
# hud_draw.draw_button_panel() only reads active_cam_id to label the
# "Cam: N" button; server.py's /status route reports the robot's real
# active_cam_id and remote_client.py mirrors it here each poll.

active_cam_id = 0
