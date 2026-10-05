import pygame


# ================================================================
# COLORS
# ================================================================

BUTTON_NORMAL = (25, 37, 56)
BUTTON_HOVER = (25, 76, 125)

BUTTON_BORDER = (218, 164, 73)
BUTTON_BORDER_INNER = (113, 72, 31)

TEXT = (245, 239, 218)
TEXT_DISABLED = (125, 125, 125)


# ================================================================
# BUTTON
# ================================================================

class Button:
    """Reusable pixel-RPG-style menu button."""

    def __init__(
        self,
        text,
        x,
        y,
        width,
        height,
        font,
        enabled=True,
    ):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.enabled = enabled

    def draw(self, screen):
        mouse_position = pygame.mouse.get_pos()

        hovering = (
            self.enabled
            and self.rect.collidepoint(mouse_position)
        )

        if hovering:
            color = BUTTON_HOVER
        else:
            color = BUTTON_NORMAL

        pygame.draw.rect(
            screen,
            color,
            self.rect,
        )

        # Outer gold border
        pygame.draw.rect(
            screen,
            BUTTON_BORDER,
            self.rect,
            4,
        )

        # Inner dark border
        inner_rect = self.rect.inflate(-10, -10)

        pygame.draw.rect(
            screen,
            BUTTON_BORDER_INNER,
            inner_rect,
            2,
        )

        if self.enabled:
            text_color = TEXT
        else:
            text_color = TEXT_DISABLED

        label = self.font.render(
            self.text,
            True,
            text_color,
        )

        label_rect = label.get_rect(
            center=self.rect.center
        )

        screen.blit(
            label,
            label_rect,
        )

    def clicked(self, event):
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )