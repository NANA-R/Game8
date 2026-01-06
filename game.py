import pygame as pg
import time
import math
from copy import copy

def main(frameLimit, bpm, tempo, startCount):

  class Clock:
    def __init__(self, color, bpm, tempo=4):
      self.color = color
      self.speed = bpm / 60 * 6 / tempo  # 1分間に回転する角度（度）
      self.angle = 0
      self.tempAngle = 0
      self.angleCount = 0
      self.playingAngle = 0
      self.playing = False

    def draw(self, screen, frame):
      self.tempAngle = copy(self.angle)
      center = screen.get_rect().center
      scrW, scrH = screen.get_size()
      radius = min(scrW, scrH) // 3
      pg.draw.circle(screen, pg.Color(self.color), center, radius)
      pg.draw.circle(screen, pg.Color("BLACK"), center, radius // 1.05)
      angle = (frame * self.speed) % 360 - 90
      end_x = center[0] + radius * 0.9 * math.cos(math.radians(angle))
      end_y = center[1] + radius * 0.9 * math.sin(math.radians(angle))
      pg.draw.line(screen, pg.Color(self.color), center, (end_x, end_y), 3)
      self.angle = int(angle)
      if self.playing:
        if self.tempAngle > self.angle:
          self.angleCount += 1
        self.playingAngle = 90 + self.angle + self.angleCount * 360
      return angle % 90 < self.speed

    def start(self):
      self.playing = True

  class Notes:
    def __init__(self, color, angle):
      self.color = color
      self.angle = angle

    def draw(self):
      pass

    def hit(self):
      pass

  # テキスト描画関数
  def draw_texts(counter, angle):
    cnt_str = f'tempo counter:{counter:05}'
    angle_str = f'angle:{angle:05}'
    screen.blit(font.render(cnt_str, True, 'WHITE'), (10, 10))
    screen.blit(font.render(angle_str, True, 'WHITE'), (10, 30))
    screen.blit(font.render("test", True, 'WHITE'), (10, 600))
    screen.blit(font.render("test", True, 'WHITE'), (10, 620))

  # 初期化処理
  pg.init()
  pg.mixer.pre_init(44100, -16, 2, 1024)
  pg.display.set_caption('RedArchibe')
  disp_w = 640
  disp_h = 640
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 20)
  frame = 0
  counter = 0
  exit_flag = False
  exit_code = '000'

  try:
    pg.mixer.music.load("Polygons.mp3")
  except Exception as e:
    print(f'音声ファイルの読み込みに失敗しました: {e}')
    exit_flag = True
    exit_code = '101'
  GameClock = Clock("RED", bpm, tempo)
  while not exit_flag:
    # カウントダウン処理
    while counter < startCount + 1 and not exit_flag:

      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'

      # 画面のクリア
      screen.fill(pg.Color('BLACK'))

      # 描画処理
      if GameClock.draw(screen, frame):
        if startCount - counter <= tempo and startCount != counter:
          pg.mixer.Sound('pip.mp3').play()
        counter += 1
      # フレームカウンタの表示
      frame += 1
      draw_texts(counter, GameClock.playingAngle)

      # 画面の更新とフレームレートの設定
      pg.display.update()
      clock.tick(60)

    # 音楽の再生開始
    if not exit_flag:
      GameClock.start()
      pg.mixer.music.play()

    while counter < frameLimit and not exit_flag:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'
      screen.fill(pg.Color('BLACK'))
      if GameClock.draw(screen, frame):
        counter += 1
        pg.mixer.Sound('pip.mp3').play()

      frame += 1
      draw_texts(counter, GameClock.playingAngle)
      pg.display.update()
      clock.tick(60)

    pg.quit()
    return exit_code

  pg.quit()
  return "109"


if __name__ == "__main__":
  code = main(300, 130, 4, 7.5)
  print(f'プログラムを「コード{code}」で終了しました。')
