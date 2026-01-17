import pygame as pg
import math
from copy import copy

class Clock:
  def __init__(self, color, bpm, screen, tempo, fps):
    self.color = color
    self.tempo = tempo
    self.bpm = bpm
    self.angle = 0
    self.tempAngle = 0
    self.angleCount = 0
    self.playingAngle = 0
    self.playing = False
    self.screen = screen
    self.fps = fps

  def draw(self, frame):
    self.tempAngle = copy(self.angle)
    center = self.screen.get_rect().center
    scrW, scrH = self.screen.get_size()
    radius = min(scrW, scrH) // 3
    speed = self.bpm / self.fps * 6 / self.tempo
    pg.draw.circle(self.screen, pg.Color(self.color), center, radius)
    pg.draw.circle(self.screen, pg.Color("BLACK"), center, radius // 1.05)
    angle = (frame * speed) % 360 - 90
    end_x = center[0] + radius * 0.9 * math.cos(math.radians(angle))
    end_y = center[1] + radius * 0.9 * math.sin(math.radians(angle))
    pg.draw.line(self.screen, pg.Color(
        self.color), center, (end_x, end_y), 3)
    self.angle = int(angle)
    if self.playing:
      if self.tempAngle > self.angle:
        self.angleCount += 1
      self.playingAngle = 90 + self.angle + self.angleCount * 360
    return angle % 90 < speed

  def start(self):
    self.playing = True

class Note:
  def __init__(self, color, angle, screen, tolerance=20, size=10):
    self.screen = screen
    self.color = color
    self.angle = angle
    self.tolerance = tolerance
    self.size = size
    center = screen.get_rect().center
    scrW, scrH = self.screen.get_size()
    radius = min(scrW, scrH) // 5
    x = center[0] + radius * math.cos(math.radians(self.angle - 90))
    y = center[1] + radius * math.sin(math.radians(self.angle - 90))
    self.pos = (x, y)

  def draw(self, color):
    self.color = color
    pg.draw.circle(self.screen, pg.Color(self.color), self.pos, self.size)

  def hitCheck(self, angle):
    checkAngle = angle - self.angle
    if checkAngle > self.tolerance * -0.5 and checkAngle < self.tolerance:
      return True
    pg.draw.circle(self.screen, pg.Color(self.color), self.pos, self.size)
    return False

  def update(self, angle, color):
    self.color = color
    if angle - self.angle > self.tolerance:
      return True
    pg.draw.circle(self.screen, pg.Color(self.color), self.pos, self.size)
    return False

if __name__ == "__main__":
  print("This module is not for direct execution.")
