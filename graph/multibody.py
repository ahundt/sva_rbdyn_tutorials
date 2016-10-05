import rbdyn as rbd

from body import linesBody, meshBody, endEffectorBody
from joint import revoluteJoint, prismaticJoint, sphericalJoint
from transform import setActorTransform

JOINT_FROM_TYPE = {
  rbd.Joint.Rev: revoluteJoint,
  rbd.Joint.Prism: prismaticJoint,
  rbd.Joint.Spherical: sphericalJoint
}


class MultiBodyViz(object):
  def __init__(self, mbg, mb, meshDict={}, endEffectorDict={}):
    """
    MutiBody visualisation.
    Params:
      - meshDict : {bodyName: (fileName, X_s, scale)}
      - endEffectorDict : {bodyName, X_to_end_effector, size, color}
    """
    self.aBodies = [] # (body index, actor, X_s)
    self.aJoints = [] # (joint index, actor, X_s)

    successorJointsName = dict(mbg.successorJoints(mb.body(0).name()))

    # body displayed by a line
    lineBodiesByIndex = {bi:b for bi, b in enumerate(mb.bodies()) if
                         len(list(successorJointsName[b.name()])) > 0}

    # create actor from mesh
    for bodyName, (fileName, X_sm, scale) in meshDict.items():
      bi = mb.bodyIndexByName(bodyName)
      try:
        del lineBodiesByIndex[bi] # don't create a line body if a mesh is set
      except KeyError:
        pass
      a, X_s = meshBody(fileName, scale)
      self.aBodies.append((bi, a, X_sm))

    # create actor from end effector
    for bodyName, (X_see, size, color) in endEffectorDict.items():
      bi = mb.bodyIndexByName(bodyName)
      a, X_s = endEffectorBody(X_see, size, color)
      self.aBodies.append((bi, a, X_s))

    for bi, b in lineBodiesByIndex.items():
      a, X_s = linesBody(mb, b.name(), successorJointsName)
      self.aBodies.append((bi, a, X_s))

    for ji, j in enumerate(mb.joints()):
      try:
        a, X_s = JOINT_FROM_TYPE[j.type()](j)
        self.aJoints.append((ji, a, X_s))
      except KeyError:
        pass


  def display(self, mb, mbc, displayBodies=True, displayJoints=True):
    """
    Display the MultiBody.
    """
    bodyPosW = list(mbc.bodyPosW)

    if displayBodies:
      for bi, actor, X_s in self.aBodies:
        X_a = X_s*bodyPosW[bi]
        setActorTransform(actor, X_a)

    if displayJoints:
      for ji, actor, X_s in self.aJoints:
        X_a = X_s*bodyPosW[ji]
        setActorTransform(actor, X_a)


  def addActors(self, scene):
    """
    Add all actors to the scene.
    """
    actors = map(lambda ab: ab[1], self.aBodies) +\
      map(lambda aj: aj[1], self.aJoints)
    for actor in actors:
      scene.renderer.add_actor(actor)


if __name__ == '__main__':
  import sys
  sys.path += [".."]

  import numpy as np
  import eigen as e
  import sva

  from robots import TutorialTree

  mbg, mb, mbc = TutorialTree()

  q = map(list, mbc.q)
  q[1] = [np.pi/2.]
  q[2] = [-np.pi/4.]
  q[3] = [-np.pi/2.]
  q[4] = [0.5]
  mbc.q = q
  rbd.forwardKinematics(mb, mbc)

  X_s = sva.PTransformd(sva.RotY(-np.pi/2.), e.Vector3d(0.1, 0., 0.))
  mbv = MultiBodyViz(mbg, mb, endEffectorDict={'b4':(X_s, 0.1, (0., 1., 0.))})

  # test MultiBodyViz
  from tvtk.tools import ivtk
  viewer = ivtk.viewer()
  viewer.size = (640, 480)
  mbv.addActors(viewer.scene)
  mbv.display(mb, mbc)

  # test axis
  from axis import Axis
  a1 = Axis(text='test', length=0.2)
  a1.addActors(viewer.scene)
  a1.X = sva.PTransformd(sva.RotX(np.pi/2.), e.Vector3d.UnitX())

  # test vector6d
  from vector6d import ForceVecViz, MotionVecViz
  M = sva.MotionVecd(e.Vector3d(0.2, 0.1, 0.), e.Vector3d(0.1, 0., 0.2))
  F = sva.ForceVecd(e.Vector3d(-0.2, -0.1, 0.), e.Vector3d(-0.1, 0., -0.2))
  MV = MotionVecViz(M, a1.X)
  FV = ForceVecViz(F, sva.PTransformd(sva.RotX(np.pi/2.), e.Vector3d.UnitX()*1.4))
  MV.addActors(viewer.scene)
  FV.addActors(viewer.scene)
