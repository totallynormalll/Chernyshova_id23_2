import pygame
import pygame_gui
import json
import math
import os

pygame.init()

shirina, visota = 800, 600
screen = pygame.display.set_mode((shirina, visota))
pygame.display.set_caption("Wave Simulation")

white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)

class Wave:
    def __init__(self, amplitude, period, speed, base_visota):
        self.amplitude = amplitude
        self.period = period
        self.speed = speed
        self.base_visota = base_visota
        self.is_selected = False

    def draw(self, screen, time):
        color = red if self.is_selected else blue
        points = [
            (x, self.base_visota + self.amplitude * math.sin(2 * math.pi / self.period * (x - self.speed * time)))
            for x in range(shirina)
        ]
        pygame.draw.aalines(screen, color, False, points)

    def visota_at(self, x, time):
        return self.base_visota + self.amplitude * math.sin(2 * math.pi / self.period * (x - self.speed * time))

class Float:
    def __init__(self, x, wave_index, mass=1.0, volume=1.0):
        self.x = x
        self.wave_index = wave_index
        self.mass = mass
        self.volume = volume

    def update_and_draw(self, screen, waves, time):
        wave = waves[self.wave_index]
        water_visota = wave.visota_at(self.x, time)

        sila_vitalkivania = self.volume
        g = self.mass
        submerged_depth = g / sila_vitalkivania #d=Fg/Fвыталкивания=V/m

        y = water_visota + submerged_depth * 10
        radius = int(self.volume * 10)

        pygame.draw.circle(screen, red, (int(self.x), int(y)), radius)

def load_state(filename):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump({
                "waves": [
                    {"amplitude": 50, "period": 100, "speed": 2},
                    {"amplitude": 30, "period": 80, "speed": 1.5},
                    {"amplitude": 40, "period": 60, "speed": 2.5},
                    {"amplitude": 20, "period": 50, "speed": 3}
                ],
                "floats": [{"x": 100, "mass": 1.0, "volume": 1.0} for _ in range(4)]
            }, f, indent=4)

    with open(filename) as f:
        data = json.load(f)
        waves = [Wave(**w, base_visota=100 + i * 100) for i, w in enumerate(data["waves"])]
        floats = [Float(f["x"], i, f.get("mass", 1.0), f.get("volume", 1.0)) for i, f in enumerate(data["floats"])]
        return waves, floats

def main():
    running = True
    clock = pygame.time.Clock()
    time = 0
    paused = False

    waves, floats = load_state("waves.json")
    selected_wave_index = 0

    manager = pygame_gui.UIManager((shirina, visota))

    amplitude_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((50, 520), (150, 20)),
        start_value=waves[selected_wave_index].amplitude,
        value_range=(10, 200),
        manager=manager
    )

    period_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((210, 520), (150, 20)),
        start_value=waves[selected_wave_index].period,
        value_range=(10, 300),
        manager=manager
    )

    mass_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((370, 520), (150, 20)),
        start_value=floats[selected_wave_index].mass,
        value_range=(0.1, 50.0),
        manager=manager
    )

    volume_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((530, 520), (150, 20)),
        start_value=floats[selected_wave_index].volume,
        value_range=(0.1, 10.0),
        manager=manager
    )

    amplitude_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((50, 490), (150, 20)),
        text=f'Amplitude: {waves[selected_wave_index].amplitude}',
        manager=manager
    )

    period_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((210, 490), (150, 20)),
        text=f'Period: {waves[selected_wave_index].period}',
        manager=manager
    )

    mass_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((370, 490), (150, 20)),
        text=f'Mass: {floats[selected_wave_index].mass}',
        manager=manager
    )

    volume_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((530, 490), (150, 20)),
        text=f'Volume: {floats[selected_wave_index].volume}',
        manager=manager
    )

    add_wave_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 560), (100, 30)),
        text='Add Wave',
        manager=manager
    )

    remove_wave_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((160, 560), (100, 30)),
        text='Remove Wave',
        manager=manager
    )

    pause_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((270, 560), (100, 30)),
        text='Pause/Resume',
        manager=manager
    )

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for i, float_obj in enumerate(floats):
                    float_x = float_obj.x
                    wave = waves[float_obj.wave_index]
                    float_y = wave.visota_at(float_x, time) + (float_obj.mass / float_obj.volume) * 10
                    radius = int(float_obj.volume * 10)
                    if (pos[0] - float_x) ** 2 + (pos[1] - float_y) ** 2 <= radius ** 2:
                        selected_wave_index = i
                        for wave in waves:
                            wave.is_selected = False
                        waves[selected_wave_index].is_selected = True
                        amplitude_slider.set_current_value(waves[selected_wave_index].amplitude)
                        period_slider.set_current_value(waves[selected_wave_index].period)
                        mass_slider.set_current_value(floats[selected_wave_index].mass)
                        volume_slider.set_current_value(floats[selected_wave_index].volume)
                        break

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == add_wave_button:
                        base_visota = 100 + len(waves) * 100
                        waves.append(Wave(30, 100, 2, base_visota))
                        floats.append(Float(100, len(waves) - 1))
                    if event.ui_element == remove_wave_button and waves:
                        waves.pop()
                        floats.pop()
                        selected_wave_index = max(0, len(waves) - 1)
                    if event.ui_element == pause_button:
                        paused = not paused

            manager.process_events(event)

        manager.update(time_delta)

        if waves:
            waves[selected_wave_index].amplitude = amplitude_slider.get_current_value()
            waves[selected_wave_index].period = period_slider.get_current_value()

            amplitude_label.set_text(f'Amplitude: {int(waves[selected_wave_index].amplitude)}')
            period_label.set_text(f'Period: {int(waves[selected_wave_index].period)}')

            floats[selected_wave_index].mass = mass_slider.get_current_value()
            floats[selected_wave_index].volume = volume_slider.get_current_value()

            mass_label.set_text(f'Mass: {floats[selected_wave_index].mass:.1f}')
            volume_label.set_text(f'Volume: {floats[selected_wave_index].volume:.1f}')

        for wave in waves:
            wave.draw(screen, time)
        for float_obj in floats:
            float_obj.update_and_draw(screen, waves, time)

        if not paused:
            time += 0.1

        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
