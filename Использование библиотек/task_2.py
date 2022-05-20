from random import uniform, seed, random
from math import sqrt
from time import sleep
from tkinter import *
from PIL import ImageTk, Image 

class Simulation(Canvas):
    state = 0;
    plotPos = (560, 490);
    population = []
    on_plot_population = []
    speed = 5
    limit_person = 0
    def draw_env(self):
        self.create_rectangle(0, 500, 1799, 999, fill="blue")
        self.create_rectangle(0, 480, 200, 999, fill="black")
        self.create_rectangle(1500, 480, 1799, 999, fill="black")

    def draw_plot(self):
        self.create_rectangle(self.plotPos[0] - 60, self.plotPos[1] - 10, self.plotPos[0] + 60, self.plotPos[1] + 10, fill="grey")

    def draw_person(self, pos):
        self.create_line(pos[0], pos[1] - 10, pos[0], pos[1] + 10)
        self.create_line(pos[0], pos[1] + 10, pos[0] - 8, pos[1] + 20)
        self.create_line(pos[0], pos[1] + 10, pos[0] + 8, pos[1] + 20)
        self.create_line(pos[0], pos[1] - 10, pos[0] - 7, pos[1] + 5)
        self.create_line(pos[0], pos[1] - 10, pos[0] + 7, pos[1] + 5)
        self.create_oval(pos[0] - 5, pos[1] - 20, pos[0] + 5, pos[1] - 10)

    def updateSimulation(self):
        self.delete("all")

        if self.state == 0:
            self.plotPos = (self.plotPos[0] + self.speed, self.plotPos[1])
            if(self.plotPos[0] >= 1440):
                self.state = 1
                self.limit_person = round(abs(uniform(1, 4)))
        elif self.state == 1:
            if len(self.population) < self.limit_person:
                if len(self.population) == 0:
                    self.population.append((1530, 460))
                else:
                    self.population.append((self.population[-1][0] + 30, self.population[-1][1]))
            else:
                if self.population[0][0] >= 1400:
                    self.population = [(i[0] - self.speed, i[1]) for i in self.population]
                else:
                    self.state = 2
        elif self.state == 2:
            self.plotPos = (self.plotPos[0] - self.speed, self.plotPos[1])
            self.population = [(i[0] - self.speed, i[1]) for i in self.population]
            if self.plotPos[0] <= 260:
                self.state = 3
        elif self.state == 3:
            if len(self.population) > 0:
                self.population = [(i[0] - self.speed, i[1]) for i in self.population]
                if self.population[0][0] < 10:
                    self.population.remove(self.population[0])
            else: 
                self.state = 0

        for i in self.population: self.draw_person(i)
        self.draw_env()
        self.draw_plot()
        self.update()


root = Tk()
root.geometry('1800x1000')
canvas = Simulation(root,width=1799,height=999)
canvas.pack()
while(True):
    canvas.updateSimulation()
    sleep(0.01)
    
root.mainloop()