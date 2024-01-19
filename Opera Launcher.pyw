import pygame as pg
import subprocess,json
pg.init()



baseCommand = r'"C:\Users\User\AppData\Local\Programs\Opera GX\launcher.exe"  --side-profile-name=PLACEHOLDER --with-feature:side-profiles --no-default-browser-check --disable-usage-statistics-question'
scale = round(pg.display.Info().current_h*(1/1080),3)
print(f"scale: {scale}")






def runAndQuit(user):
    userKey = user.key
    runnable = baseCommand.replace("PLACEHOLDER",userKey)
    subprocess.run(runnable)
    pg.quit()
    quit()


def crop_to_circle(original_image):
    image_width, image_height = original_image.get_size()
    mask_surface = pg.Surface((image_width, image_height), pg.SRCALPHA)
    
    # Create a circular mask
    pg.draw.circle(mask_surface, (255, 255, 255, 255), (image_width // 2, image_height // 2), image_width // 2)
    
    # Create a new surface with alpha transparency
    cropped_surface = pg.Surface((image_width, image_height), pg.SRCALPHA)
    
    # Blit the circular mask onto the new surface
    cropped_surface.blit(mask_surface, (0, 0))
    
    # Blit the original image onto the circular surface using the circular mask
    cropped_surface.blit(original_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    
    return cropped_surface




class User:
    def __init__(self,name,key,image_path):
        self.OG_image = pg.transform.scale(pg.image.load(image_path),(tile_width*0.8,tile_width*0.8))
        self.image = self.OG_image
        self.image = crop_to_circle(self.OG_image)
        self.key = key
        self.name = name
        self.rect = None


def draw_UI(display, users, font, font2, displaysize):
    display.fill((100, 100, 100))
    welcome_text = font2.render("Welcome!", True, (255, 255, 255))
    text_x = (displaysize[0] - welcome_text.get_width()) // 2
    text_y = 50 * scale
    display.blit(welcome_text, (text_x, text_y))

    tiles_per_row = 4
    total_tiles = len(users)
    total_rows = (total_tiles + tiles_per_row - 1) // tiles_per_row

    row_height = spacer_height + tile_height
    col_width = spacer_width + tile_width

    total_height = row_height * total_rows

    top_border = (displaysize[1] - total_height) // 2
    left_border = (displaysize[0] - col_width * min(tiles_per_row, total_tiles)) // 2

    for idx, user in enumerate(users):
        row = idx // tiles_per_row
        col = idx % tiles_per_row

        tlx, tlr = left_border + col * col_width, top_border + row * row_height

        pg.draw.rect(display, (255, 255, 255), (tlx, tlr, tile_width, tile_height), border_radius=int(10 * scale))
        display.blit(user.image, (tlx + tile_width * 0.1, tlr + tile_width * 0.1))
        user.rect = pg.Rect(tlx, tlr, tile_width, tile_height)


        user_name_text = font.render(user.name, True, (0, 0, 0))
        text_x = tlx + (tile_width - user_name_text.get_width()) // 2
        text_y = tlr + tile_width
        display.blit(user_name_text, (text_x, text_y))



        
        
left_border = 70*scale
top_border = 150*scale
tile_width= 200*scale
tile_height = 280*scale
spacer_width = 20*scale
spacer_height = 20*scale


def main():
    with open("data/users.json") as file:   
        userData = json.load(file)
    #print(userData)
    users = [User(key,value["key"],value["image_path"]) for key,value in userData.items()]

    displaysize = (1000*scale,800*scale)
    display = pg.display.set_mode(displaysize)
    pg.display.set_caption("Opera Launcher 0.1")
    font = pg.font.Font("data/MinecraftRegular-Bmg3.otf",int(scale*30))
    font2 = pg.font.Font("data/MinecraftRegular-Bmg3.otf",int(scale*100))
    draw_UI(display,users,font,font2,displaysize)
    dead = False
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True
                elif event.unicode in "12345678":
                    try:
                        n = int(event.unicode)
                        print(n)
                        runAndQuit(users[n-1])
                    except Exception as e:
                        print(e)
            elif event.type == pg.MOUSEBUTTONDOWN:
                
                if event.button == 1:
                    mousepos = pg.mouse.get_pos()
                    for idx,user in enumerate(users):
                        if user.rect.collidepoint(mousepos):
                            runAndQuit(users[idx])
            

            
        draw_UI(display,users,font,font2,displaysize)
        pg.display.flip()


if __name__ == "__main__":
    main()
    pg.quit()
    quit()





