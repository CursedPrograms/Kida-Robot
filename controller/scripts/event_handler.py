# event_handler.py — remote-controller keyboard/mouse dispatch
#
# Mirrors the key bindings in scripts/event_handler.py, but every action
# is a RemoteClient.send_action() POST to the robot's /action route
# instead of a direct hardware call — nothing here touches GPIO, serial,
# or Picamera2.

import pygame
import mode_manager
import state


def handle_events(events, buttons: list, pressed_keys: set, remote,
                  lock_prompt=None) -> dict:
    """lock_prompt is main.py's PasswordPrompt, so the 'U' key can open the
    same on-screen prompt the "Lock Motors" button uses (optional; 'U' is a
    no-op without it)."""
    signals = {"quit": False}

    for event in events:

        if event.type == pygame.QUIT:
            signals["quit"] = True
            continue

        # ── Keyboard ─────────────────────────────────────────────────────
        if event.type == pygame.KEYDOWN:
            k = event.key

            if k == pygame.K_1:
                remote.send_action("mode_1")
            elif k == pygame.K_2:
                remote.send_action("mode_2")
            elif k == pygame.K_3:
                remote.send_action("mode_3")
            elif k == pygame.K_4:
                remote.send_action("mode_4")
            elif k == pygame.K_5:
                remote.send_action("mode_5")
            elif k == pygame.K_6:
                remote.send_action("mode_6")

            # Quit — Q and ESC both just close this window. There's no
            # run.sh restart loop on this side to distinguish them; that
            # split (see scripts/event_handler.py) is robot-specific.
            elif k in (pygame.K_q, pygame.K_ESCAPE):
                signals["quit"] = True

            elif k == pygame.K_i:
                remote.send_action("inference_toggle")

            elif k == pygame.K_x:
                remote.send_action("speed_cycle")

            elif k == pygame.K_SPACE:
                remote.send_action("hard_stop")

            elif k == pygame.K_m:
                if remote.status.get("music_on"):
                    remote.send_action("music_skip")
                else:
                    remote.send_action("music_play")

            elif k == pygame.K_l:
                remote.send_action("leds_toggle")
            elif k == pygame.K_k:
                remote.send_action("leds_effects_toggle")

            # Motor lock — mirrors the "Lock Motors" button: locking is
            # instant, unlocking opens the password prompt (checked
            # server-side, never locally).
            elif k == pygame.K_u:
                if state.motor_lock:
                    if lock_prompt is not None:
                        lock_prompt.open(lambda pw: remote.send_action("motor_lock_off", password=pw))
                else:
                    remote.send_action("motor_lock_on")

            elif k == pygame.K_c:
                remote.send_action("photo")
            elif k == pygame.K_v:
                remote.send_action("video_start")

            # Drive scheme toggle — ,/< = WASD (differential), ./> = QAWS
            # (tank, independent per-motor). Mirrors scripts/event_handler.py.
            elif event.unicode in ('<', ','):
                remote.send_action("scheme_wasd")
            elif event.unicode in ('>', '.'):
                remote.send_action("scheme_qaws")

            # Movement — KEYBOARD mode only, mirroring the robot's own guard.
            # Which keys do what depends on state.drive_scheme (synced from
            # /status by remote_client.py).
            elif state.drive_scheme == "QAWS" and k in (pygame.K_q, pygame.K_a, pygame.K_w, pygame.K_s):
                if mode_manager.is_keyboard():
                    command = {
                        pygame.K_q: "left_forward",
                        pygame.K_a: "left_backward",
                        pygame.K_w: "right_forward",
                        pygame.K_s: "right_backward",
                    }[k]
                    remote.send_action(command)
                    pressed_keys.add(k)
            elif state.drive_scheme == "WASD" and k in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d):
                if mode_manager.is_keyboard():
                    command = {
                        pygame.K_w: "move_forward",
                        pygame.K_s: "move_backward",
                        pygame.K_a: "move_left",
                        pygame.K_d: "move_right",
                    }[k]
                    remote.send_action(command)
                    pressed_keys.add(k)

        elif event.type == pygame.KEYUP:
            if event.key in pressed_keys:
                if state.drive_scheme == "QAWS" and event.key in (pygame.K_q, pygame.K_a):
                    remote.send_action("left_stop")
                elif state.drive_scheme == "QAWS" and event.key in (pygame.K_w, pygame.K_s):
                    remote.send_action("right_stop")
                else:
                    remote.send_action("move_stop")
                pressed_keys.discard(event.key)

        # ── Mouse ────────────────────────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for button in buttons:
                if button.is_clicked(pos):
                    button.action()

    return signals
