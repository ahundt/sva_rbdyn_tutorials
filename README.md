# SpaceVecAlg and RBDyn tutorials

This repository contains IPython notebook tutorial for the SpaceVecAlg and the RBDyn library:
 * [SpaceVecAlg tutorial](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/SpaceVecAlg.ipynb)
 * [MultiBody tutorial](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/MultiBody.ipynb)
 * [Rigid Body Algorithm tutorial](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/SomeAlgorithm.ipynb)
 * [Jacobian tutorial](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/Jacobian.ipynb)
 * [My First Inverse Kinematic](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/MyFirstIK.ipynb)
 * [Inverse Kinematic with the REEM-C humanoid robot](http://nbviewer.ipython.org/github/jorisv/sva_rbdyn_tutorials/blob/master/ReemCIK.ipynb)

## Ubuntu 16.04 Install/Run Instructions

```
# install the software
sudo add-apt-repository ppa:pierre-gergondet+ppa/multi-contact-unstable
sudo apt-get update
sudo apt-get install python-tasks python3-tasks

python2 -c 'import sva; import tasks'
python3 -c 'import sva; import tasks'

# install the python packages
pip3 install jupyter vtk mayavi PyQt5 --user --upgrade

# wxPython install from https://wiki.wxpython.org/How%20to%20install%20wxPython
pip3 install --user --upgrade -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-16.04 wxPython

# enable mayavi visualization in jupyter lab
jupyter nbextension install --py mayavi --user
jupyter nbextension enable --py mayavi --user

# get the code
mkdir -p ~/src/jrl-umi3218
cd ~/src/jrl-umi3218
git clone https://github.com/jrl-umi3218/sva_rbdyn_tutorials.git
cd sva_rbdyn_tutorials

# start running the code server
jupyter lab
```

Once you run `jupyter lab` it will open in your web browser, from there select one of the tutorial files and you are good to go!

### Dependencies

To execute those IPython notebook you must have:

 * [IPython]() (test with the version 3)
 * [Eigen3ToPython](https://github.com/jorisv/Eigen3ToPython)
 * [SpaceVecAlg](https://github.com/jorisv/SpaceVecAlg)
 * [RBDyn](https://github.com/jorisv/RBDyn)
 * [mayavi2]()
