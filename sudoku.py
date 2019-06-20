import dancingLinks as dlx

class Sudoku:
  def __init__(self, grid, pprint=True):
    self.grid = grid
    self.pprint = pprint

  def is_valid(self):
    rows = [[0 for _ in range(9)] for _ in range(9)]
    columns = [[0 for _ in range(9)] for _ in range(9)]
    blocks = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
      for j in range(9):
        n = self.grid[i][j]-1
        if not (n >= 0 and n <= 8): return False
        rows[i][n] += 1
        columns[j][n] += 1
        blocks[3*(i//3)+(j//3)][n] += 1

    for t in [rows,columns,blocks]:
      for x in t:
        for y in x:
          if y != 1 : return False

    return True

  def __str__(self):
    s = ''
    if self.pprint:
      sep_line = '----'*9+'-'
      sep = '|'
      for row in self.grid:
        s += sep_line + '\n'
        for x in row:
          s += sep + ' ' + str(x) + ' '
        s += sep + '\n'
      s += sep_line
    else:
      for row in self.grid:
        for x in row:
          s += str(x) if x != 0 else '.'
    return s


  
  def produce_dlx(self):
    # constraints on columns
    columns = [str(i*10+j) for j in range(1,10) for i in range(1,10)] + \
              [str(i)+'C'+str(j) for j in range(1,10) for i in range(1,10)] + \
              [str(i)+'L'+str(j) for j in range(1,10) for i in range(1,10)] + \
              [str(i)+'B'+str(j) for j in range(1,10) for i in range(1,10)]
    root = dlx.ColHeader('NaN')
    for idcol in columns:
      dlx.ColHeader(idcol).insert(root)

    for i in range(9):
      for j in range(9):
        ii,jj = i+1,j+1
        n = self.grid[i][j]
        if n > 0:
          root.add_row([str(ii*10+jj),
                        str(n)+'C'+str(jj),
                        str(n)+'L'+str(ii),
                        str(n)+'B'+str((3*(i//3)+(j//3))+1)],
                       str(n*100+ii*10+jj))
        else:
          for nn in range(1,10):
            root.add_row([str(ii*10+jj),
                          str(nn)+'C'+str(jj),
                          str(nn)+'L'+str(ii),
                          str(nn)+'B'+str((3*(i//3)+(j//3))+1)],
                         str(nn*100+ii*10+jj))

    return root
  
  def fill_from_dlx_sol(self,sol):
    for x in sol:
      x = int(x)
      n = x // 100
      i = (x - n*100) // 10
      j = x - n*100 - i*10
      self.grid[i-1][j-1] = n

  def solve(self,inplace=True):
    sols = self.produce_dlx().KnuthX()
    if inplace:
      if len(sols) != 1:
        raise ValueError
      self.fill_from_dlx_sol(sols[0])
    return sols
