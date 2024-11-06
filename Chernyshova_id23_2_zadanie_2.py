import tkinter as tk
import json
import math
import os

class WaveSimulation:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width=800, height=600, bg='white')
        self.canvas.pack()
        self.time = 0
        self.waves, self.floats = self.load_state("wave_config.json")
        self.animate()

    def load_state(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump({
                    "waves": [
                        {"amplitude": 50, "period": 100, "speed": 2},
                        {"amplitude": 30, "period": 80, "speed": 1.5},
                        {"amplitude": 40, "period": 60, "speed": 2.5},
                        {"amplitude": 20, "period": 50, "speed": 3}
                    ],
                    "floats": [{"x": 100} for _ in range(4)]
                }, f, indent=4)

        with open(filename) as f:
            data = json.load(f)
            return (
                [Wave(**w, base_height=100 + i * 100) for i, w in enumerate(data["waves"])],
                [Float(f["x"], i) for i, f in enumerate(data["floats"])]
            )

    def animate(self):
        self.canvas.delete("all")
        for wave in self.waves:
            wave.draw(self.canvas, self.time)
        for float_obj in self.floats:
            float_obj.update_and_draw(self.canvas, self.waves, self.time)
        self.time += 0.1
        self.canvas.after(30, self.animate)

class Wave:
    def __init__(self, amplitude, period, speed, base_height):
        self.amplitude = amplitude
        self.period = period
        self.speed = speed
        self.base_height = base_height

# y= y0 + A*sin*((2π/T)*(x−v*t))+H
# A-амплитуда, Т-период волны, v-скорость распространения по OX,
# t-текущее время (изменяется при каждом обновлении для создания движения)
# Н-базовая высота, которая задает начальное положение волны на холсте, смещая ее вертикально
    def draw(self, canvas, time):
        points = [(x, self.base_height + self.amplitude * math.sin(2 * math.pi / self.period * (x - self.speed * time))) for x in range(800)]
        canvas.create_line(points, fill='blue')

    def height_at(self, x, time):
        return self.base_height + self.amplitude * math.sin(2 * math.pi / self.period * (x - self.speed * time))

class Float:
    def __init__(self, x, wave_index):
        self.x = x
        self.wave_index = wave_index

    def update_and_draw(self, canvas, waves, time):
        y = waves[self.wave_index].height_at(self.x, time)
        canvas.create_oval(self.x - 10, y - 10, self.x + 10, y + 10, fill='red')

root = tk.Tk()
root.title("Wave Simulation")
simulation = WaveSimulation(root)
root.mainloop()
