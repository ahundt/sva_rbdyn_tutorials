from tvtk.api import tvtk
from tvtk.common import configure_input_data

import eigen as e
import sva

from . import transform

class Vector6dViz(object):
  def __init__(self, linear, angular, frame, linColor, angColor):
    """
    Create the visualization of a 6D vector with a linear and angular part.
    Parameter:
      linear: 3d linear component (e.Vector3d)
      angular: 3d angular component (e.Vector3d)
      frame: vector frame (sva.PTransformd)
      linColor: linear component color (float, float, float)
      angColor: angular component color (float, float, float)
    """
    self.linearActor, X_l = self._createVector(linear, frame, linColor)
    self.angularActor, X_a = self._createVector(angular, frame, angColor)

    # create a Arc around the angular axis
    # The arc must turn around the X axis (Arrow default axis)
    angNorm = angular.norm()
    angNormW = angNorm*0.3
    arcSource = tvtk.ArcSource(point1=(angNorm/2., -angNormW, -angNormW),
                               point2=(angNorm/2., -angNormW, angNormW),
                               center=(angNorm/2., 0., 0.), negative=True,
                               resolution=20)

    # arcPdm = tvtk.PolyDataMapper(input=arcSource.output)
    arcPdm = tvtk.PolyDataMapper()

    # https://stackoverflow.com/questions/35089379/how-to-fix-traiterror-the-input-trait-of-a-instance-is-read-only
    # configure_input_data(textPdm, textSource)# https://github.com/enthought/mayavi/issues/521
    arcPdm.input_connection = arcPdm.output_port

    prop = tvtk.Property(color=angColor)
    # https://github.com/enthought/mayavi/issues/521
    # arcPdm.input_connection = arcSource.output_port
    self.arcActor = tvtk.Actor(mapper=arcPdm, property=prop)

    # commented due to api change, new lines are above Actor creation
    # self.arcActor.property.color = angColor
    # https://github.com/enthought/mayavi/blob/5c2694b72b329b8d5c469bc459a211378e2c8581/tvtk/pyface/actors.py#L112
    self.arcActor.user_transform = tvtk.Transform()
    # apply the angular transform
    transform.setActorTransform(self.arcActor, X_a)


  def _createVector(self, vector, frame, color):
    source = tvtk.ArrowSource()
    # pdm = tvtk.PolyDataMapper(input=source.output)
    pdm = tvtk.PolyDataMapper()
    # https://github.com/enthought/mayavi/issues/521
    pdm.input_connection = source.output_port
    # configure_input_data(pdm, source)
    prop = tvtk.Property(color=color)
    actor = tvtk.Actor(mapper=pdm, property=prop)
    actor.user_transform = tvtk.Transform()
    # commented due to api change, new lines are above Actor creation
    # actor.property.color = color
    norm = vector.norm()
    actor.scale = (norm,)*3
    quat = e.Quaterniond()
    # arrow are define on X axis
    quat.setFromTwoVectors(vector, e.Vector3d.UnitX())
    X = sva.PTransformd(quat)*frame
    transform.setActorTransform(actor, X)
    return actor, X


  def addActors(self, scene):
    """
    Add actors to the scene.
    """
    scene.renderer.add_actor(self.linearActor)
    scene.renderer.add_actor(self.angularActor)
    scene.renderer.add_actor(self.arcActor)


  def removeActors(self, scene):
    """
    Remove actors from the scene.
    """
    scene.renderer.remove_actor(self.linearActor)
    scene.renderer.remove_actor(self.angularActor)
    scene.renderer.remove_actor(self.arcActor)



class ForceVecViz(Vector6dViz):
  def __init__(self, F, frame):
    """
    Helper class to display a sva.ForceVecd.
    """
    super(ForceVecViz, self).__init__(F.force(), F.couple(), frame,
                                      (1., 0., 0.), (1., 1., 0.))



class MotionVecViz(Vector6dViz):
  def __init__(self, M, frame):
    """
    Helper class to display a sva.MotionVecd.
    """
    super(MotionVecViz, self).__init__(M.linear(), M.angular(), frame,
                                       (0., 0., 1.), (1., 0., 1.))
