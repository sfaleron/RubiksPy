
# keystrokes:
# u,d,f,b,l,r to rotate that face clockwise; hold shift to rotate counter-
# clockwise; ctrl to rotate twice. h to keep the face stationary while ro-
# tating the rest of the cube the opposite way on the next move. alt for
# the current move (where supported). to rotate the whole cube, rotate a
# face and then reverse the rotation, but hold the face and rotate the rest.
# left/right to undo or replay moves;
# m to set (or remove) a marker in the move stack, ctrl-left/right to undo/
# replay to the next marker. use a pretty gui interface to name markers and
# target them by name.
# s to save the state of the cube to a file, o (open) to read it back in.
# 0 to reset the cube to its initial (solved) state; a to toggle animation;
# p to toggle presentation mode
# escape exits; standard visual python behavior


import random
import time

from itertools import permutations

from visual import display

from cube import Cube

# pass 0 <= n <= 35
def decode_rotate(n, order):
   d = {}

   a, k, f = order[0]
   n, r = divmod(n, a)
   d[k] = f(r)

   a, k, f = order[1]
   n, r = divmod(n, a)
   d[k] = f(r)

   a, k, f = order[2]
   d[k] = f(n)

   return d


# glitches, but they seem to cancel w/ undos.. find view w/ interface and read parameters from program?

# iterating through all moves works fine. the funny business is cancelled somehow.

# more than one of these three true will work, but be chaotic!
ALLROTS  = False
RANDROTS = True
EACHTURN = False

UNDO     = True
VALIDATE = True


random.seed(99)

N = 20


# the six orderings of the three parameters aren't all the possible encodings,
# of course. each parameter can be similarly reordered, for 3! * 2!*3!*6! = 51840.
# this still isn't the same as arbitrarily ordering all 36 moves, not by a long shot!
# 36! = 371993326789901217467999448150835200000000.

# we'll be content with simply reordering the parameters. after all, reordering
# the order of a parameter doesn't change the appearance of the sequence much.
ENCODING = (
   (2, 'holdface', bool),
   (3, 'turns',    lambda x:x+1),
   (6, 'face',     lambda x:FACES[x])
)

FACES = ('l','r','d','u','b','f')

def demo(cube):

   time.sleep(2)

   yield

   while True:
      if ALLROTS:
         for order, guide in zip(permutations(ENCODING), permutations(map(str, range(3)))):
            #if ''.join(guide) in ('201','210'):
            #   continue

            print ' '.join(guide)
            print '-----'
            for n in range(36):
               d = decode_rotate(n, order)
               cube.rotate_face(**d)
               print n,d

               if VALIDATE:
                  if not cube.validate():
                     print 'rotation failed!'

               time.sleep(.666)
               yield

            #print

            cube.visible = False
            time.sleep(.1)
            cube.visible = True
            time.sleep(2)

      if RANDROTS:
         n = 0
         lastface = None

         while n<N:
            d = decode_rotate(random.randint(0, 35), ENCODING)

            if d['face'] != lastface:
               lastface = d['face']
               cube.rotate_face(**d)
               print d
               n += 1

               if VALIDATE:
                  if not cube.validate():
                     print 'rotation failed!'

               time.sleep(.666)
               yield

            #print

         cube.visible = False
         time.sleep(.1)
         cube.visible = True
         time.sleep(2)

      if UNDO and RANDROTS:
         for i in range(N):
            cube.undo()

            if VALIDATE:
               if not cube.validate():
                  print 'undo failed!'

            time.sleep(.666)
            yield

         cube.visible = False
         time.sleep(.1)
         cube.visible = True
         time.sleep(2)


      if EACHTURN:
         for n in range(36):
            d = decode_rotate(n, ENCODING)
            cube.rotate_face(**d)
            print n, d
            #raw_input()

            if VALIDATE:
               if not cube.validate():
                  print 'rotation failed!'

            time.sleep(.666)
            yield


            cube.undo()

            if VALIDATE:
               if not cube.validate():
                  print 'undo failed!'

            time.sleep(.666)
            yield

         #print

         cube.visible = False
         time.sleep(.1)
         cube.visible = True
         time.sleep(2)

# alt doesn't seem to work on windoze
def accept_kb_input(scene, cube):
   dodemo = False
   hold = False

   demo_g = demo(cube)

   while True:
      if not scene.kb.keys and dodemo:
         demo_g.next()
         continue

      key = scene.kb.getkey()

      d = {}
      if len(key) == 1:
         if key in FACES:
            d[ 'face'] = key
            d['turns'] = 1
         else:
            key = key.lower()
            if key in FACES:
               d[ 'face'] = key
               d['turns'] = -1

            if key == 'a':
               cube.animation = not cube.animation
               continue

            if key == 'p':
               dodemo = not dodemo
               continue

            if key == 'h':
               hold = True
               continue
      else:
         keys = key.split('+')
         key  = keys.pop(-1)

         if key in FACES:
            d = {'face':key}
            if 'shift' in keys and 'ctrl' in keys:
               continue
            if 'shift' in keys:
               d['turns'] = -1
            if 'ctrl' in keys:
               d['turns'] = 2

      if d:
         d['holdface'] = hold
         cube.rotate_face(**d)
         hold = False

         if VALIDATE:
            if not cube.validate():
               print 'rotation failed!'

if __name__ == '__main__':
   scene0 = display(title="Rubik's Cube Simulator", width=600, height=600,
      scale=(.2,.2,.2), forward=(-0.4,-0.3,-1), up=(-0.1,1,0), exit=True)

   cube = Cube(size=1.0)

   cube.validate()

   accept_kb_input(scene0, cube)
