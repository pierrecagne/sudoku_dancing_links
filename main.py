import dancingLinks as dlx
import random
import sudoku as sdk
import time
import sys

def main():
  print('avg time:', sudoku_testing()*1000, 'ms')
  
def sudoku_testing():
  total_time = 0
  with open(sys.argv[1],'r') as tests:
    nb_test = 0
    for sudoku in tests:
      nb_test += 1
      sudoku = sudoku[:81]
      sudoku = [list(map(lambda x: 0 if x == '.' else int(x),sudoku[9*i:9*(i+1)])) for i in range(9)]
      checkpoint = time.time()
      s = sdk.Sudoku(sudoku, pprint=True)
      # print(s)
      # root = s.produce_dlx()
      # print('exploring column', root.right.idcol)
      # for x in root.right.cell.iter(start=root.right.cell.down):
      #   print(x.idrow, ':', end=' ')
      #   for y in x.iter(start=x.right, direction='right'):
      #     print(y.colhead.idcol, end=' ')
      #   print()
      s.solve(inplace=True)
      # print(s, '\n')
      total_time += time.time()-checkpoint
  return total_time / float(nb_test)

def testing():
  root = dlx.ColHeader(idcol='NaN')
  for x in range(1,11):
    print('Treating column nb', x)
    new = dlx.ColHeader(idcol=x)
    print('Column created: ', id(new.cell.colhead))
    nrow = random.randrange(1,11)
    l = []
    for _ in range(nrow):
      done = False
      while not done:
        r = random.randrange(0,10)
        if r not in l:
          l.append(r)
          done = True
    print('Random list of row indices:', l)
    for r in l:
      ncell = dlx.Cell(r)
      ncell.insert(after=new.cell,direction='vertical')
    new.insert(root)
  print(root)

def add_row_testing():
  root = dlx.ColHeader(idcol='NaN')
  colids = list('ABCDEF')
  for colid in colids:
    print('Treating column ', colid)
    new = dlx.ColHeader(idcol=colid)
    new.insert(root)
  rowids = list(range(1,30))
  for rowid in rowids:
    chosencols = []
    for col in colids:
      if random.randrange(0,2) == 0:
        chosencols.append(col)
    print('Columns for row', rowid, ':', chosencols)
    root.add_row(chosencols, rowid)
  print(root.right.right)
  print(root)
  print(root.KnuthX())
  
if __name__ == '__main__' :
  main()
