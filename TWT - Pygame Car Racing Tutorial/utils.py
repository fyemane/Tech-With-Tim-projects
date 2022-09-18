import pygame
pygame.font.init()

# scaling function
def scale_image(img, factor):
    # tuple must have rounded width and height
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

# input image, outputs rotated image
def blit_rotate_center(win, image, top_left, angle):
    # rotate image around top left corner
    rotated_image = pygame.transform.rotate(image, angle)
    # remove the offset without changing x,y position
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft = top_left).center)
    # find correct x,y position for new rotated image
    win.blit(rotated_image, new_rect.topleft)

# blit text at center of screen
def blit_text_center(win, font, text):
    # text we want to render
    render = font.render(text, 1, (0, 255, 255))
    # put text on window
    win.blit(render, (win.get_width()/2 - render.get_width()/2,
                     win.get_height()/2 - render.get_height()/2))