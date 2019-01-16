from os.path import splitext

from tvtk.api import tvtk

import eigen as e
import sva



FILE_READER = {
  '.obj': tvtk.OBJReader,
  '.stl': tvtk.STLReader,
}


def linesBody(mb, bodyName, successorJointsName):
  """
  Return a mesh represented by lines and the appropriate static transform.
  """
  apd = tvtk.AppendPolyData()
  sources = []

  # create a line from the body base to the next joint
  for s in map(mb.jointIndexByName, successorJointsName[bodyName]):
    X_s = mb.transform(s)
    sources.append(tvtk.LineSource(point1=(0., 0., 0.),
                                   point2=tuple(X_s.translation())))

  # add an empty source to avoid a warning if AppendPolyData have 0 source
  if len(sources) == 0:
    sources.append(tvtk.PointSource(radius=0.))

  map(lambda s: apd.add_input(s.output), sources)
  apd.update()

  pdm = tvtk.PolyDataMapper()
  pdm.input_connection = apd.output_port
  actor = tvtk.Actor(mapper=pdm)
  actor.property.color = (0., 0., 0.)
  actor.user_transform = tvtk.Transform()

  return actor, sva.PTransformd.Identity()


def meshBody(fileName, scale=(1., 1., 1.)):
  """
  Return a mesh actor and the appropriate static transform.
  """
  reader = FILE_READER[splitext(fileName)[1]](file_name=fileName)
  output = reader.output

  # if a scale is set we have to apply it
  if map(float, scale) != [1., 1., 1.]:
    tpdf_transform = tvtk.Transform()
    tpdf_transform.identity()
    tpdf_transform.scale(scale)
    tpdf = tvtk.TransformPolyDataFilter(input=reader.output, transform=tpdf_transform)
    tpdf.update()
    output = tpdf.output

  # compute mesh normal to have a better render and reverse mesh normal
  # if the scale flip them
  pdn = tvtk.PolyDataNormals(input=output)
  pdn.update()
  output = pdn.output

  pdm = tvtk.PolyDataMapper(input=output)
  actor = tvtk.Actor(mapper=pdm)
  actor.user_transform = tvtk.Transform()

  return actor, sva.PTransformd.Identity()


def endEffectorBody(X_s, size, color):
  """
  Return a end effector reprsented by a plane
  and the appropriate static transform.
  """
  apd = tvtk.AppendPolyData()

  ls = tvtk.LineSource(point1=(0., 0., 0.),
                       point2=tuple(X_s.translation()))

  p1 = (sva.PTransformd(e.Vector3d.UnitX()*size)*X_s).translation()
  p2 = (sva.PTransformd(e.Vector3d.UnitY()*size)*X_s).translation()
  ps = tvtk.PlaneSource(origin=tuple(X_s.translation()),
                        point1=tuple(p1),
                        point2=tuple(p2),
                        center=tuple(X_s.translation()))

  # apd.add_input(ls.output)
  # apd.add_input(ps.output)
  # https://github.com/enthought/mayavi/blob/ac5c8e316335078c25461a0bce4a724ae86f1836/tvtk/tests/test_tvtk.py#L586
  apd.add_input_data(ls.output)
  apd.add_input_data(ps.output)

  # pdm = tvtk.PolyDataMapper(input=apd.output)
  # arcPdm = tvtk.PolyDataMapper(input=arcSource.output)
  pdm = tvtk.PolyDataMapper()

  # https://stackoverflow.com/questions/35089379/how-to-fix-traiterror-the-input-trait-of-a-instance-is-read-only
  # configure_input_data(textPdm, textSource)# https://github.com/enthought/mayavi/issues/521
  pdm.input_connection = apd.output_port

  prop = tvtk.Property(color=color)
  # https://github.com/enthought/mayavi/issues/521
  # arcPdm.input_connection = arcSource.output_port
  actor = tvtk.Actor(mapper=pdm, property=prop)
  actor.property.color = color
  actor.user_transform = tvtk.Transform()

  return actor, sva.PTransformd.Identity()
