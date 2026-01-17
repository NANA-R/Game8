import pygame as pg
import time
from codes import contents
Clock = contents.Clock
Note = contents.Note

def game(tempoLimit, bpm, tempo, startCount, fps, auto=False):

  # テキスト描画関数
  def draw_texts(counter, angle, hit, miss, color):
    # cnt_str = f'tempo counter:{counter:05}'
    # angle_str = f'angle:{angle:05}'
    hit_str = f'hit:{hit:05}'
    miss_str = f'miss:{miss:05}'
    # screen.blit(font.render(cnt_str, True, 'WHITE'), (10, 10))
    # screen.blit(font.render(angle_str, True, 'WHITE'), (10, 30))
    # screen.blit(font.render(color, True, color), (10, 50))
    screen.blit(font.render(hit_str, True, "WHITE"), (10, 600))
    screen.blit(font.render(miss_str, True, "WHITE"), (10, 620))

  # 初期化処理
  pg.init()
  pg.mixer.pre_init(44100, -16, 2, 1024)
  pg.display.set_caption('Rhythm Timer')
  disp_w = 640
  disp_h = 640
  screen = pg.display.set_mode((disp_w, disp_h))
  clock = pg.time.Clock()
  font = pg.font.Font(None, 20)
  frame = 0
  counter = 0
  exit_flag = False
  exit_code = '000'
  gameColor = "RED"
  notesAngle = [360, 90, 90, 90, 90, 90, 90,
                150, 30, 90, 90, 90, 90, 90,
                90, 150, 30, 90, 90, 90, 90,
                90, 90, 150, 30, 90, 90, 90,
                90, 60, 30, 60, 30, 90, 90, "BLUE",
                90, 30, 60, 60, 90, 30, 90,
                90, 90, 90, 90, 30, 60, 60,
                90, 30, 90, 90, 90, 90, 90,
                30, 60, 60, 90, 30, 90, 90,
                90, 90, 90, 30, 60, 60, 90,
                30, 90, 90, 30, 60, 30, 60,
                60, 30, "YELLOW", 90, 90, 90,
                90, 90, 60, 30, 60, 30, 90,
                90, 90, 90, 30, 60, 30, 60,
                30, 60, 90, 90, 90, 150, 30, 90, 90,
                150, 30, 90, 90, 90, 90, 60, 30, 60, 30, 90, 90, "GRAY", 0.5,
                90, 90, 90, 30, 30, 30, 90, 90, 90, 60, 30,
                90, 90, 90, 90, 90, 90, 90, 60, 30, "WHITE", 2.0,
                90, 90, 90, 90, 90, 90, 90, 30, 30, 30, 90, 90, 90, 90, 90, 30, 30, 30,
                60, 60, 60, 90, 90, 90, 90, 90, 90, 90, 30, 30, 30, 90, 90, 90, 90,
                60, 30, 60, 30, 90, 90, "GREEN",
                90, 30, 60, 60, 60, 60, 90, 90, 90, 90, 90, 30, 60, 60, 60, 60, 90, 90,
                60, 30, 60, 30, 90, 90, 90, 30, 30, 30, 90, 90, 90, 30, 30, 30, 90, 60, 120,
                90, 90, 60, 120, 90, 90, 30, 60, 60, 60, 60, 90, 90, 90, 90,
                90, 30, 60, 60, 60, 60, 90, 90, 60, 30, 60, 30, 90, 90, 90, 30, 30, 30,
                90, 90, 90, 30, 30, 30, 90, 90, 90, 90, 90, 90, 90, 90, "RED", 0.5,
                180, 30, 60, 30, 30, 30, 180, 30, 60, 30, 30, 30, 180, 30, 60, 30, 30, 30, 180, 30, 60, 30, 30, 30]
  notes = []
  changeColorTimings = []
  changeBPMTimings = []
  tempAngle = 0
  for content in notesAngle:
    if type(content) == int:
      tempAngle += content
      notes.append(tempAngle)
    elif type(content) == str:
      changeColorTimings.append([tempAngle, content])
    else:
      changeBPMTimings.append([tempAngle, content])

  mag = 1.0
  notesCount = 0
  displayNotesCount = 0
  doneNotesCount = 0
  miss = 0
  hit = 0
  key = False
  autoPlay = auto

  try:
    pg.mixer.music.load("./assets/Polygons.mp3")
    peep = "./assets/pip.mp3"
  except Exception as e:
    print(f'音声ファイルの読み込みに失敗しました: {e}')
    exit_flag = True
    exit_code = '101'
  GameClock = Clock(gameColor, bpm, screen, tempo, fps)
  for num in range(len(notes)):
    globals()[f"note{num + 1}"] = Note(gameColor, notes[num], screen)

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
      if GameClock.draw(frame):
        if startCount - counter <= tempo and startCount != counter:
          pg.mixer.Sound(peep).play()
        counter += 1
      # フレームカウンタの表示
      frame += 1
      draw_texts(counter, GameClock.playingAngle, hit, miss, gameColor)

      # 画面の更新とフレームレートの設定
      pg.display.update()
      clock.tick(fps)

    # 音楽の再生開始
    if not exit_flag:
      pg.mixer.music.play()
      GameClock.start()

    while counter < tempoLimit and not exit_flag:
      for event in pg.event.get():
        if event.type == pg.QUIT:
          exit_flag = True
          exit_code = '001'
        if event.type == pg.KEYUP:
          key = False
        if event.type == pg.KEYDOWN:
          key = True
      screen.fill(pg.Color('BLACK'))
      for timing in changeColorTimings:
        if timing[0] < GameClock.playingAngle:
          gameColor = timing[1]
          GameClock.color = gameColor
          changeColorTimings.remove(timing)
      for timing in changeBPMTimings:
        if timing[0] < GameClock.playingAngle:
          mag *= timing[1]
          changeBPMTimings.remove(timing)
      try:
        if notes[notesCount] - 360 < GameClock.playingAngle:
          globals()[f"note{notesCount + 1}"].draw(gameColor)
          displayNotesCount += 1
          notesCount += 1
      except IndexError:
        pass
      if GameClock.draw(frame):
        if counter % 5 == 0:
          time.sleep(0.001)
        counter += 1

      if not autoPlay:
        for num in range(1, displayNotesCount):
          if globals()[f"note{num + doneNotesCount}"].hitCheck(GameClock.playingAngle) and key:
            doneNotesCount += 1
            displayNotesCount -= 1
            hit += 1
            key = False
            pg.mixer.Sound(peep).play()
          elif globals()[f"note{num + doneNotesCount}"].update(GameClock.playingAngle, gameColor):
            doneNotesCount += 1
            displayNotesCount -= 1
            time.sleep(0.05)
            miss += 1

      else:
        for num in range(1, displayNotesCount):
          if globals()[f"note{num + doneNotesCount}"].angle <= GameClock.playingAngle:
            doneNotesCount += 1
            displayNotesCount -= 1
            hit += 1
            pg.mixer.Sound(peep).play()
          else:
            globals()[f"note{num + doneNotesCount}"].draw(gameColor)

      frame += 1
      draw_texts(counter, GameClock.playingAngle, hit, miss, gameColor)
      pg.display.update()
      clock.tick(fps * mag)

    pg.quit()
    return exit_code, hit, miss

  pg.quit()
  return "109"


if __name__ == "__main__":
  print("This module is not for direct execution.")
