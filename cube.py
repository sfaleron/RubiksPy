
# idea about building by position:
# define the faces (colors) by their -1,1 axes values;
# from that, getting positions is straightforward.

# the numpy array stuff and the visual stuff should be separated, but how
# to correlate the pieces? probably a dictionary rather than a list, eh?
# the visual part would register each location with the numpy part by location,
# then the numpy part would return a set of these when its done the rotation.

# ahh, three square classes; one for each orthogonal plane!

# to reorient, can do the face/holdface thing, but also rotate along
# (-1,-1,-1)-(1,1,1) to keep the same three faces showing. although,
# this is the correct axis only if the user has not rotated the scene
# too much. the numpy array will need some updating, too.. which implies
# it can be done with straightforward already supported rotations.. eh,
# not really. could do it with a 3D rotation of the coordinate triples,
# then fill in the rotated triples with the piece from the original. the
# swap method used in 2D rotation would work, but would be really hairy
# in 3D!

# have a reflection method to make a mirror image cube. needs to have
# piece-by-position stuff though.

from visual import frame, convex, color, rate, pi

import numpy

# reminder of coordinate system: plus z is towards viewer; plus xy is up and right.
# right hand rule says x is horizontal axis

# takes a 3x3 numpy array
# convert to 1D, swap values as appropriate, back to 2D
def rotate_cw(a, n):
   aa = a.copy().reshape(9)
   for i in range(n):
      e0,e1,e2,e3,e4,e5,e6,e7,e8 = aa
      aa = (e6,e3,e0,e7,e4,e1,e8,e5,e2)
   return numpy.array(aa).reshape(3,3)

def mkslice(a, i):
   l = [slice(None)] * 3
   l[a] = i
   return l

# this is the fundamental element
# always in the xy plane, rotate as needed
class Square(frame):
   def __init__(self, parent, pos, size, color1):
      frame.__init__(self, frame=parent, pos=pos)
      convex(frame=self, pos = (
         (-size/2, -size/2, 0),
         ( size/2, -size/2, 0),
         (-size/2,  size/2, 0),
         ( size/2,  size/2, 0) ),
         color=color1)

class Center(frame):
   def __init__(self, parent, pos, size, color1):
      frame.__init__(self, frame=parent, pos=pos)
      self.children = (
         Square(self, (0, 0, size/2), size, color1) )

class Edge(frame):
   def __init__(self, parent, pos, size, color1, color2):
      frame.__init__(self, frame=parent, pos=pos)
      self.children = (
         Square(self, (0, 0, -size/2), size, color1),
         Square(self, (0, 0, -size/2), size, color2) )

      self.children[-1].rotate(angle=pi/2, origin=(0,0,0), axis=(1,0,0))

class Corner(frame):
   def __init__(self, parent, pos, size, color1, color2, color3):
      frame.__init__(self, frame=parent, pos=pos)
      self.children = (
         Square(self, (0, 0, -size/2), size, color1),
         Square(self, (0, 0, -size/2), size, color2),
         Square(self, (0, 0, -size/2), size, color3) )

      self.children[-1].rotate(angle=pi/2, origin=(0,0,0), axis=(1,0,0))
      self.children[-2].rotate(angle=pi/2, origin=(0,0,0), axis=(0,1,0))

# each piece starts from a "prototype", which is simply the first one I built.
# the prototype is recreated with the appropriate colors, then rotated into
# position.
# it's not too tricky to automate the rotations, based on start and end
# positions: find the faces that the start and end positions belong to; centers
# belong to a single face, edges two, and corners three. find the two nearest
# faces and it isn't hard after that. but it's not worth the trouble just for
# initial setup.
# the ideal approach would be to create each piece exactly for its location, but
# this is much easier. it might be really desirable if load/save is implemented.
# or even to just undo a cube reset!
class Cube(frame):
   # the final rotated position of the piece corresponds to its placement in the
   # internal 3x3x3 array.
   def add_piece(self, piece, size):
      # segfaults if iterated over vector!
      x,y,z = [int(round(i/size, 0))+1 for i in piece.pos.astuple()]

      self.array[x,y,z] = len(self.piecelist)
      self.piecelist.append(piece)

   def centers(self, size):
      p = Center(self, (0,0,size), size, color.yellow)
      self.add_piece(p, size)

      p = Center(self, (0,0,size), size, color.white)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

      p = Center(self, (0,0,size), size, color.blue)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Center(self, (0,0,size), size, color.green)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Center(self, (0,0,size), size, color.red)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

      p = Center(self, (0,0,size), size, color.orange)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)


   # four pairs of opposite corners
   def corners(self, size):
      p = Corner(self, (-size, size, -size), size, color.white, color.red, color.blue)
      self.add_piece(p, size)

      p = Corner(self, (-size, size, -size), size, color.green, color.orange, color.yellow)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(0,1,0))
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)


      p = Corner(self, (-size, size, -size), size, color.white, color.orange, color.green)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(0,0,1))
      self.add_piece(p, size)

      p = Corner(self, (-size, size, -size), size, color.red, color.yellow, color.blue)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)


      p = Corner(self, (-size, size, -size), size, color.yellow, color.orange, color.blue)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

      p = Corner(self, (-size, size, -size), size, color.white, color.green, color.red)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,0,1))
      self.add_piece(p, size)


      p = Corner(self, (-size, size, -size), size, color.yellow, color.red, color.green)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Corner(self, (-size, size, -size), size, color.orange, color.white, color.blue)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)


   # yz plane
   def edges1(self, size):
      p = Edge(self, (0,size,-size), size, color.white, color.blue)
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.yellow, color.green)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.blue, color.yellow)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.green, color.white)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

   # xy plane
   def edges2(self, size):
      p = Edge(self, (0,size,-size), size, color.red, color.blue)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.orange, color.green)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,1,0))
      p.rotate(angle= pi,   origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.orange, color.blue)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.green, color.red)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(1,0,0))
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,1,0))
      self.add_piece(p, size)

   # xz plane
   def edges3(self, size):
      p = Edge(self, (0,size,-size), size, color.yellow, color.orange)
      p.rotate(angle= pi,   origin=(0,0,0), axis=(0,1,0))
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,0,1))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.white, color.red)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,0,1))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.white, color.orange)
      p.rotate(angle=-pi/2, origin=(0,0,0), axis=(0,0,1))
      self.add_piece(p, size)

      p = Edge(self, (0,size,-size), size, color.yellow, color.red)
      p.rotate(angle= pi/2, origin=(0,0,0), axis=(0,0,1))
      p.rotate(angle= pi,   origin=(0,0,0), axis=(1,0,0))
      self.add_piece(p, size)


   # always turns clockwise. specify -1 for counterclockwise turn
   def rotate_face(self, face, turns, holdface=False, undo=False, stackoff=False):
      if not turns%4:
         return

      if (face == 'u' or face == 'd') and turns%4 != 2 and not self.ohmy:
         # would it work to rotate the whole cube, do
         # the corrected rotation, then rotate back? :)
         return
         # oh my, epic fail!
         self.rotate(angle=pi/2, axis=( 1,0,0), origin=(0,0,0))
         self.ohmy = True
         self.rotate_face(face, turns, holdface, undo, stackoff)
         self.ohmy = False
         self.rotate(angle=pi/2, axis=(-1,0,0), origin=(0,0,0))
         # still fail, but more amusing, at least :)
         self.ohmy = (self.animation,)
         self.animation = False
         self.rotate_face('l',  1)
         self.rotate_face('l', -1, holdface=True)
         self.rotate_face({'u':'f','d':'b'}[face], turns, holdface, undo, stackoff)
         self.rotate_face('l', -1, holdface=True)
         self.rotate_face('l',  1)
         self.animation = self.ohmy[0]
         self.ohmy = None
         # also.. this demonstrates that the glitch isn't limited to the y axis rotations!
         return

      axis = {
         'r' : 1, 'l' : -1,
         'u' : 2, 'd' : -2,
         'f' : 3, 'b' : -3,
      }[face]

      d = {
         'face'     : face,
         'turns'    : turns,
         'holdface' : holdface
      }

      # two turns is its own inverse
      if turns%4 != 2:
         if undo:
            turns += 2

         if axis < 0:
            turns += 2

         if holdface:
            turns += 2

      turns %= 4

      if holdface:
         axis = -axis

      activeslices = [0 if axis<0 else 2]

      if holdface:
         activeslices.append(1)

      axis = abs(axis) - 1

      pieces = set()

      for i in activeslices:
         # equivalent to self.array[i,:,:] for the appropriate dimension
         slice_ = self.array.__getitem__(mkslice(axis, i))
         self.array.__setitem__(mkslice(axis, i), rotate_cw(slice_, turns))

         pieces.update(slice_.reshape(9).tolist())

      pieces.discard(99)

      rotaxis = [0,0,0]

      if self.ohmy:
         axis = 2
         turns = (turns + 2) % 4

      if turns == 3:
         turns = 1
         rotaxis[axis] = -1
      else:
         rotaxis[axis] =  1

      if self.animation:
         for i in range(6*turns):
            for p in pieces:
               self.piecelist[p].rotate(angle=-pi/12, origin=(0,0,0), axis=rotaxis)
            rate(8)

      else:
         for p in pieces:
            self.piecelist[p].rotate(angle=-turns*pi/2, origin=(0,0,0), axis=rotaxis)

      if not stackoff:
         self.movestack.append(d)

   def undo(self):
      if not self.movestack:
         return

      last = self.movestack.pop()

      last['stackoff'] = True
      last['undo'] = True
      self.rotate_face(**last)

   def validate(self):
      a = self.array
      size = self.size

      valid = True

      if a[1,1,1] != 99:
         print 'ouch! center moved!'
         valid = False

      for i in range(3):
         for j in range(3):
            for k in range(3):
               if i == j == k == 1:
                  continue

               idx = a[i,j,k]

               if idx == 99:
                  print 'ouch! center moved!'
                  valid = False

               piece = self.piecelist[idx]

               # segfaults if iterated over vector!
               x,y,z = [int(round(ii/size, 0))+1 for ii in piece.pos.astuple()]
               if i != x or j != y or k != z:
                  #print i,j,k,x,y,z
                  valid = False

      return valid

   def __init__(self, size=1.0, pos=(0,0,0), parent=None):
      frame.__init__(self, pos=pos, frame=parent)

      self.animation = True
      self.size = size
      self.ohmy = False

      self.movestack = []
      self.piecelist = []

      self.array = numpy.zeros((3,3,3), 'uint8')
      self.array[1,1,1] = 99

      self.corners(size)
      self.centers(size)

      # twelve edges, do em in batches (one for each orthogonal plane)
      self.edges1(size)
      self.edges2(size)
      self.edges3(size)
