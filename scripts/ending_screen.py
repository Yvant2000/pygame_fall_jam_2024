from pygame import font

from scripts import display, textures, manor


def display_end_screen():
    end = textures.end_screen
    pos_x = (display.window_top_layer.get_width() - end.get_width()) // 2
    display.window_top_layer.blit(end, (pos_x, 0))
    display.window_top_layer.blit(textures.end_message, (0, 0))

    # create pygame font
    font.init()
    tmp_font = font.Font(size=50)
    font_renderer = tmp_font.render(f"seed: {manor.seed}", True, (255, 255, 255))
    display.window_top_layer.blit(font_renderer, (70, 30 + textures.end_message.get_height()))
