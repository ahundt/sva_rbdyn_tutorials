from tvtk.api import tvtk
from tvtk.common import configure_input_data

import eigen as e
import sva

from . import transform

class Axis(object):
  def __init__(self, X=sva.PTransformd.Identity(), length=0.1, text=''):
    """
    Create a 3D axis.
    """
    self._X = X
    self.axesActor = tvtk.AxesActor(total_length=(length,)*3,
                                    axis_labels=False)
    self.axesActor.user_transform = tvtk.Transform()

    textSource = tvtk.TextSource(text=text, backing=False)
    # textPdm = tvtk.PolyDataMapper(input=textSource.output)
    textPdm = tvtk.PolyDataMapper()

    # https://stackoverflow.com/questions/35089379/how-to-fix-traiterror-the-input-trait-of-a-instance-is-read-only
    # configure_input_data(textPdm, textSource.output_port)

    # https://github.com/enthought/mayavi/issues/521
    textPdm.input_connection = textSource.output_port

    #self.textActor = tvtk.Actor(mapper=textPdm)
    self.textActor = tvtk.Follower(mapper=textPdm)
    # take the maximum component of the bound and use it to scale it
    m = max(self.textActor.bounds)
    scale = length/m
    self.textActor.scale = (scale,)*3
    # TODO compute the origin well...
    self.textActor.origin = (
      -(self.textActor.bounds[0] + self.textActor.bounds[1])/2.,
      -(self.textActor.bounds[2] + self.textActor.bounds[3])/2.,
      -(self.textActor.bounds[4] + self.textActor.bounds[5])/2.,
    )
    ySize = self.textActor.bounds[3]*1.2
    self.X_text = sva.PTransformd(e.Vector3d(0., -ySize, 0.))
    self._transform()


  def _transform(self):
    transform.setActorTransform(self.axesActor, self._X)
    # user_transform is not take into account by Follower
    self.textActor.position = tuple((self.X_text*self._X).translation())


  @property
  def X(self):
    return self._X


  @X.setter
  def X(self, X):
    self._X = X
    self._transform()


  def addActors(self, scene):
    """
    Add actors to the scene.
    """
    scene.renderer.add_actor(self.axesActor)
    scene.renderer.add_actor(self.textActor)
    self.textActor.camera = scene.camera


  def removeActors(self, scene):
    """
    Remove actors from the scene.
    """
    scene.renderer.remove_actor(self.axesActor)
    scene.renderer.remove_actor(self.textActor)
