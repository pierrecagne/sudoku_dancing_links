class Cell:
  def __init__(self, idrow):
    self.up, self.down, self.left, self.right = self, self, self, self
    self.colhead = None
    self.idrow = idrow
    return None

  def __vcover(self):
    self.up.down, self.down.up = self.down, self.up
    self.colhead.size -= 1
    return None

  def __hcover(self):
    self.left.right, self.right.left = self.right, self.left
    return None

  def cover(self, direction):
    if direction not in ['vertical', 'horizontal']:
      raise ValueError
    if direction == 'vertical': self.__vcover()
    elif direction == 'horizontal': self.__hcover()
    return None

  def __vuncover(self):
    self.up.down, self.down.up = self, self
    self.colhead.size += 1   
    return None
  
  def __huncover(self):
    self.left.right, self.right.left = self, self
    return None

  def uncover(self, direction):
    if direction not in ['vertical', 'horizontal']:
      raise ValueError
    if direction == 'vertical': self.__vuncover()
    elif direction == 'horizontal': self.__huncover()
    return None

  def __vinsert(self, after):
    self.up, self.down = after, after.down
    self.colhead = after.colhead
    self.__vuncover()
    return None
    
  def __hinsert(self, after):
    self.left, self.right = after, after.right
    self.__huncover()
    return None

  def insert(self, after, direction):
    if direction not in ['vertical', 'horizontal']:
      raise ValueError
    if direction == 'vertical': self.__vinsert(after)
    elif direction == 'horizontal': self.__hinsert(after)
    return None

  # def iter(self, start=None, stop=None, direction='down'):
  #   if start != None: nondef_start = True
  #   curr = start if start != None else self
  #   stop = stop if stop != None else self
  #   if nondef_start and curr == stop: return
  #   while True:
  #     yield curr
  #     curr = curr.__getattribute__(direction)
  #     if curr == stop: break
        
class ColHeader:
  def __init__(self, idcol, size = 0):
    self.left, self.right = self, self
    self.cell = Cell('NaN')
    self.cell.colhead = self
    self.idcol = idcol
    self.size = size
    return None

  def cover(self):
    self.left.right, self.right.left = self.right, self.left
    return None

  def uncover(self):
    self.left.right, self.right.left = self, self
    return None
        
  def insert(self, after):
    self.left, self.right = after, after.right
    self.uncover()
    return None

  # def iter(self, start=None, stop=None, direction='right'):
  #   if start != None: nondef_start = True
  #   curr = start if start != None else self
  #   stop = stop if stop != None else self
  #   if nondef_start and curr == stop: return
  #   while True:
  #     yield curr
  #     curr = curr.__getattribute__(direction)
  #     if curr == stop: break
  
  def Knuth_cover(self):
    self.cover()
    curr = self.cell.down
    while curr != self.cell:
      hcurr = curr.right
      while hcurr != curr:
        hcurr.cover(direction='vertical')
        hcurr = hcurr.right
      curr = curr.down
    return None

  # def Knuth_cover(self):
  #   self.cover()
  #   for v in self.cell.iter(start=self.cell.down):
  #     for h in v.iter(start=v.right, direction='right'):
  #       h.cover(direction='vertical')
  #   return
  
  def Knuth_uncover(self):
    curr = self.cell.up
    while curr != self.cell:
      hcurr = curr.left
      while hcurr != curr:
        hcurr.uncover(direction='vertical')
        hcurr = hcurr.left
      curr = curr.up
    self.uncover()
    return None

  # def Knuth_uncover(self):
  #   for v in self.cell.iter(start=self.cell.up, direction='up'):
  #     for h in v.iter(start=v.left, direction='left'):
  #       h.uncover(direction='vertical')
  #   self.uncover()
  #   return

  # def get_idrows(self):
  #   indices = []
  #   curr = self.cell.down
  #   while curr != self.cell:
  #     indices.append(curr.idrow)
  #     curr = curr.down
  #   return indices

  def get_idrows(self):
    indices = []
    curr = self.cell.down
    while curr != self.cell:
      indices.append(curr.idrow)
      curr = curr.down
    return indices

  
  def is_root(self):
    return (self.idcol == 'NaN')
  
  def __str__(self):
    if not self.is_root():
      return str((self.idcol, self.get_idrows()))
    else:
      idrows = set()
      colids = {}
      cur = self.right
      while cur != self:
        colidrows = cur.get_idrows()
        idrows = idrows.union(colidrows)
        colids[cur.idcol] = colidrows
        cur = cur.right
      s = 'col ids   \t'
      for colid in colids.keys():
        s += str(colid) + '\t'
      s += '\n\n'
      for row in list(idrows):
        s += 'row ' + str(row) + '   \t'
        for colid in colids.keys():
          if row in colids[colid]:
            s += '1\t'
          else: s += 'O\t'
        s += '\n'
      return s

  def add_row(self, ones, idrow):
    if not self.is_root(): raise ValueError
    dummy = Cell(idrow)
    col = self.right
    while col != self:
      if col.idcol in ones:
        new = Cell(idrow)
        new.insert(col.cell, direction='vertical')
        new.insert(dummy, direction='horizontal')
        #print('new cell: idrow', new.idrow, 'colhead id', new.colhead.idcol,
        #      'colhead.size', new.colhead.size)
      col = col.right
    dummy.cover(direction='horizontal')
    del dummy

  # def add_row(self, ones, idrow):
  #   if not self.is_root(): raise ValueError
  #   dummy = Cell(idrow)
  #   for col in self.iter(start=self.right):
  #     if col.idcol in ones:
  #       new = Cell(idrow)
  #       new.insert(col.cell, direction='vertical')
  #       new.insert(dummy, direction='horizontal')
  #   dummy.cover(direction='horizontal')
  #   del dummy
    
  def KnuthX(self):
    sols = []
    def rec_search(partialSol):
      if self.right == self:
        #print('Solution found!', partialSol)
        sols.append(partialSol)
      else:
        # find column with minimal number of cells
        curr = self.right
        min_ones, min_col = curr.size, curr
        while curr != self:
          if curr.size < min_ones:
            min_ones, min_col = curr.size, curr
          curr = curr.right
        # cover the column just found
        #print('min_col found:', min_col.idcol, 'has', min_ones, 'cells')
        min_col.Knuth_cover()
        # for each cells in that column, try it for solution
        cell = min_col.cell.down
        while cell != min_col.cell:
          hcurr = cell.right
          while hcurr != cell:
            hcurr.colhead.Knuth_cover()
            hcurr = hcurr.right
          rec_search([cell.idrow] + partialSol)
          hcurr = cell.left
          while hcurr != cell:
            hcurr.colhead.Knuth_uncover()
            hcurr = hcurr.left
          cell = cell.down
        # finally uncover the column 
        min_col.Knuth_uncover()
    rec_search([])
    return sols

  # def KnuthX(self):
  #   sols = []
  #   def rec_search(partialSol):
  #     if self.right == self:
  #       sols.append(partialSol)
  #     else:
  #       # find column with minimal number of cells
  #       min_ones, min_col = None, None
  #       for curr in self.iter(start=self.right):
  #         if (min_ones == None and min_col == None) or curr.size < min_ones:
  #           min_ones, min_col = curr.size, curr
  #       # cover the column just found
  #       min_col.Knuth_cover()
  #       # for each cells in that column, try it for solution
  #       for cell in min_col.cell.iter(start=min_col.cell.down):
  #         for hcurr in cell.iter(start=cell.right, direction='right'):
  #           hcurr.colhead.Knuth_cover()
  #         rec_search([cell.idrow] + partialSol)
  #         for hcurr in cell.iter(start=cell.left, direction='left'):
  #           hcurr.colhead.Knuth_uncover()
  #       # finally uncover the column 
  #       min_col.Knuth_uncover()
  #   rec_search([])
  #   return sols
