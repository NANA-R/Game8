from codes import game

if __name__ == "__main__":
  code = game.game(245, 130, 4, 8, 60)
  if type(code) == tuple:
    exit_code, hit, miss = code
    print(f'プログラムを「コード{exit_code}」で終了しました。')
    print(f'Hit: {hit}, Miss: {miss}')
  else:
    print(f'プログラムを「コード{code}」で終了しました。')
