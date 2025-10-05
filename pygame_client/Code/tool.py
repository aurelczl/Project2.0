import pygame

class Tool:
    
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, witdh: int, height: int):
        return spritesheet.subsurface(pygame.Rect(x, y, witdh, height))
    """
    @staticmethod
    def split_image(spritesheet: pygame.Surface, x: int, y: int, width: int, height: int, scale: tuple[int, int] = None):
        #Découpe une sous-image d'un spritesheet, avec option de redimension.
        frame = spritesheet.subsurface(pygame.Rect(x, y, width, height))
        if scale:
            frame = pygame.transform.scale(frame, scale)
        return frame
    """