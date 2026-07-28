# text_prompt.py — small on-screen free-text overlay for KIDA
#
# Pure pygame — no hardware, no network calls. Same shape as
# password_prompt.py's PasswordPrompt, but accepts any typed text instead
# of a fixed-length numeric code, for ui.py's "type a message to KIDA" box
# (bypasses Whisper/wake-word entirely — see kida_chat_wakeword.submit_text).

import pygame

MAX_LENGTH = 200


class TextPrompt:
    def __init__(self, title: str):
        self.title     = title
        self.active    = False
        self.buffer    = ""
        self.on_submit = None   # callback(text: str) -> None

    def open(self, on_submit) -> None:
        self.active    = True
        self.buffer    = ""
        self.on_submit = on_submit

    def cancel(self) -> None:
        self.active    = False
        self.buffer    = ""
        self.on_submit = None

    def handle_key(self, event) -> None:
        if not self.active:
            return
        if event.key == pygame.K_ESCAPE:
            self.cancel()
            return
        if event.key == pygame.K_BACKSPACE:
            self.buffer = self.buffer[:-1]
            return
        if event.key == pygame.K_RETURN:
            self._submit()
            return
        ch = event.unicode
        if ch and ch.isprintable() and len(self.buffer) < MAX_LENGTH:
            self.buffer += ch

    def _submit(self) -> None:
        text = self.buffer.strip()
        if text and self.on_submit:
            self.on_submit(text)
        self.cancel()

    def draw(self, surface, fonts) -> None:
        if not self.active:
            return
        sw, sh = surface.get_size()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))

        box = pygame.Rect(0, 0, 520, 150)
        box.center = (sw // 2, sh // 2)
        pygame.draw.rect(surface, (20, 24, 36), box, border_radius=10)
        pygame.draw.rect(surface, (120, 160, 220), box, width=2, border_radius=10)

        title_surf = fonts["hd"].render(self.title, True, (200, 220, 255))
        surface.blit(title_surf, title_surf.get_rect(center=(box.centerx, box.top + 26)))

        input_rect = pygame.Rect(box.left + 16, box.centery - 14, box.width - 32, 32)
        pygame.draw.rect(surface, (10, 14, 22), input_rect, border_radius=6)
        pygame.draw.rect(surface, (80, 100, 140), input_rect, width=1, border_radius=6)

        shown = self.buffer[-46:] + ("|" if (pygame.time.get_ticks() // 500) % 2 == 0 else "")
        text_surf = fonts["xs"].render(shown, True, (255, 255, 255))
        surface.blit(text_surf, (input_rect.left + 8, input_rect.centery - text_surf.get_height() // 2))

        msg = fonts["xs"].render("Enter to send, Esc to cancel", True, (150, 160, 190))
        surface.blit(msg, msg.get_rect(center=(box.centerx, box.bottom - 20)))
