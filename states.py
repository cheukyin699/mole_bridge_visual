import pygame
import string
import mmass
mmass.init()

class Label:
    def __init__(self, surface, font, pos = (0, 0), text = ""):
        self.surface = surface
        self.text = text
        self.value = 0
        self.font = font

        self.image = font.render(self.text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def handle(self, e):
        pass

    def update(self):
        txt = self.text + ': ' + str(self.value)
        self.image = self.font.render(txt, True, (255, 255, 255))

    def draw(self):
        self.surface.blit(self.image, self.rect)

class Button(Label):
    def __init__(self, surface, font, cb, pos = (0, 0), text = ""):
        Label.__init__(self, surface, font, pos, text)
        self.cb = cb

        self.drect = pygame.Surface((self.rect.w, self.rect.h))
        self.drect.fill((50, 50, 50))
        self.drect.blit(self.image, (0, 0))

        self.isPointIn = self.rect.collidepoint

    def handle(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            # Get clicked
            self.cb()

    def draw(self):
        self.surface.blit(self.drect, self.rect)

class ClickText(Label):
    def __init__(self, surface, font, pos = (0, 0), text = ""):
        Label.__init__(self, surface, font, pos, text)
        self.focus = False

        self.isPointIn = self.rect.collidepoint

    def handle(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            # Get clicked
            self.focus = True

    def update(self):
        Label.update(self)

    def draw(self):
        Label.draw(self)

class MainState:
    def __init__(self, surface, font):
        self.focal = None
        self.font = font

        self.surface = surface

        # The buttons and labels and stuffs
        self.mass_ct = ClickText(self.surface, font, (0, 0), "Mass")
        self.particles_ct = ClickText(self.surface, font, (0, 100), "Particles")
        self.volume_ct = ClickText(self.surface, font, (0, 200), "Volume @ STP")
        self.element_ct = ClickText(self.surface, font, (150, 0), "Element")
        self.moles_lbl = Label(self.surface, font, (150, 100), "Moles")
        self.mass_lbl = Label(self.surface, font, (300, 0), "Mass")
        self.particles_lbl = Label(self.surface, font, (300, 100), "Particles")
        self.volume_lbl = Label(self.surface, font, (300, 200), "Volume @ STP")
        self.reset_bt = Button(self.surface, font, self.reset, (0, 400),
                "RESET")
        self.start_bt = Button(self.surface, font, self.start,
                (200, 400), "START")

        self.ct_map = {
                'm': self.mass_ct,
                'p': self.particles_ct,
                'v': self.volume_ct,
                'e': self.element_ct
        }

        self.inputted = ""
        self.last = None

        self.element_ct.value = ""

    def reset(self):
        self.mass_ct.value = 0
        self.particles_ct.value = 0
        self.volume_ct.value = 0
        self.moles_lbl.value = 0
        self.mass_lbl.value = 0
        self.particles_lbl.value = 0
        self.volume_lbl.value = 0

        self.update_texts()

    def update_texts(self):
        self.mass_ct.update()
        self.particles_ct.update()
        self.volume_ct.update()
        self.element_ct.update()
        self.moles_lbl.update()
        self.mass_lbl.update()
        self.particles_lbl.update()
        self.volume_lbl.update()

    def start(self):
        # Get a valid molar mass first
        molar_mass = mmass.getMolarMass(self.element_ct.value)
        if not molar_mass: return

        # Calculate moles for the last one updated
        l_up = self.ct_map[self.last]
        moles = 0
        if self.last == 'm':
            # Mass to moles
            moles = l_up.value / molar_mass
        elif self.last == 'p':
            # Particles to moles
            moles = l_up.value / 6.02e23
        elif self.last == 'v':
            # Volume to moles
            moles = l_up.value / 22.4
        self.moles_lbl.value = round(moles, 3)

        # Calculate each individually
        self.mass_lbl.value = round(moles * molar_mass, 3)
        self.particles_lbl.value = round(moles * 6.02e23, -5)
        self.volume_lbl.value = round(moles * 22.4, 3)

        # Update
        self.update_texts()

    def handle(self, e):
        mxy = pygame.mouse.get_pos()

        if e.type == pygame.MOUSEBUTTONUP:
            if self.mass_ct.isPointIn(mxy):
                self.focal = 'm'
            elif self.particles_ct.isPointIn(mxy):
                self.focal = 'p'
            elif self.volume_ct.isPointIn(mxy):
                self.focal = 'v'
            elif self.element_ct.isPointIn(mxy):
                self.focal = 'e'
            elif self.reset_bt.isPointIn(mxy):
                self.reset_bt.handle(e)
            elif self.start_bt.isPointIn(mxy):
                self.start_bt.handle(e)
            else:
                self.focal = None

        elif self.focal and e.type == pygame.KEYDOWN:
            # If there is a focal point
            # Take all keyboard input
            keys = []
            pressed = pygame.key.get_pressed()

            # If you pressed enter, well...
            if pressed[pygame.K_RETURN]:
                # Load value to CT
                if self.focal != 'e':
                    self.last = self.focal
                    try:
                        self.ct_map[self.focal].value = float(self.inputted)
                    except:
                        pass
                else:
                    self.ct_map[self.focal].value = self.inputted
                self.inputted = ""      # Input reset
                self.ct_map[self.focal].update()
                self.focal = None
                self.reset()
                return
            elif pressed[pygame.K_BACKSPACE]:
                # Backspace?
                if len(self.inputted) > 0:
                    self.inputted = self.inputted[:-1]

            for i in xrange(len(pressed)):
                if pressed[i] and i < 256 and chr(i) in string.printable:
                    keys.append(i)

            shift = pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]
            keys = ''.join(map(chr, keys))
            if shift:
                keys = keys.upper()
            self.inputted += keys

    def update(self):
        pass

    def draw(self):
        if self.focal:
            # Draw inputted text
            img = self.font.render(self.inputted, True, (255, 255, 255))
            self.surface.blit(img, (250, 250))
        else:
            self.mass_ct.draw()
            self.particles_ct.draw()
            self.volume_ct.draw()
            self.element_ct.draw()
            self.moles_lbl.draw()
            self.mass_lbl.draw()
            self.particles_lbl.draw()
            self.volume_lbl.draw()
            self.reset_bt.draw()
            self.start_bt.draw()

