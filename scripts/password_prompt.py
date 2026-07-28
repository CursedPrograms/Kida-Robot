# password_prompt.py — small on-screen numeric password overlay for KIDA
#
# Pure pygame — no hardware, no network calls. The caller supplies a
# submit callback that does the actual work (motor_lock.try_unlock()
# in-process on the robot, or remote.send_action("motor_lock_off", ...)
# over the network on the controller) so this same overlay drives both
# HUDs identically.

import pygame


class PasswordPrompt:
    def __init__(self, title: str, length: int = 4):
        self.title     = title
        self.length    = length
        self.active    = False
        self.buffer    = ""
        self.error     = False
        self.on_submit = None   # callback(password: str) -> bool

    def open(self, on_submit) -> None:
        self.active    = True
        self.buffer    = ""
        self.error     = False
        self.on_submit = on_submit

    def cancel(self) -> None:
        self.active    = False
        self.buffer    = ""
        self.error     = False
        self.on_submit = None

    def handle_key(self, event) -> None:
        if not self.active:
            return
        if event.key == pygame.K_ESCAPE:
            self.cancel()
            return
        if event.key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
            self.error  = False
            return
        if event.key == pygame.K_RETURN:
            self._submit()
            return
        ch = event.unicode
        if ch and ch.isdigit() and len(self.buffer) < self.length:
            self.buffer += ch
            self.error   = False
            if len(self.buffer) == self.length:
                self._submit()

    def _submit(self) -> None:
        ok = bool(self.on_submit and self.on_submit(self.buffer))
        if ok:
            self.cancel()
        else:
            self.error  = True
            self.buffer = ""

    def draw(self, surface, fonts) -> None:
        if not self.active:
            return
        sw, sh = surface.get_size()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 380, 150)
        box.center = (sw // 2, sh // 2)
        pygame.draw.rect(surface, (20, 24, 36), box, border_radius=10)
        pygame.draw.rect(surface, (200, 80, 80), box, width=2, border_radius=10)

        title_surf = fonts["hd"].render(self.title, True, (255, 200, 200))
        surface.blit(title_surf, title_surf.get_rect(center=(box.centerx, box.top + 30)))

        dots = ("* " * len(self.buffer) + "- " * (self.length - len(self.buffer))).strip()
        dots_surf = fonts["hd"].render(dots, True, (255, 255, 255))
        surface.blit(dots_surf, dots_surf.get_rect(center=(box.centerx, box.centery + 12)))

        if self.error:
            msg = fonts["xs"].render("Wrong password - try again (Esc to cancel)", True, (255, 120, 120))
        else:
            msg = fonts["xs"].render("Type 4 digits, Enter to confirm, Esc to cancel", True, (150, 160, 190))
        surface.blit(msg, msg.get_rect(center=(box.centerx, box.bottom - 22)))
