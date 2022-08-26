# Strictly confined juju snap wrapper template 

This is a template/demo project to show how to go about creating a snap that wraps the juju client snap.

Say: 
 - you have written some code that interfaces with the juju client, either via [`python-libjuju`](https://github.com/juju/python-libjuju) or directly via the juju cli.
 - you want to make a snap for your code.
 - you want your snap to be strictly confined.

Then what you could do is use this project as a template, replace the demo `jujuwrapper` code with your own, add any interfaces your code might require to work, and you should be good to go!

How this works: this snap embeds a juju client binary (in fact, it carries its own copy of the juju snap) and enables it to act as if you had installed it directly.

## Not just Python
This template contains a simple python cli tool for demo purposes, and it uses the `python` plugin for the `jujuwrapper` part, but it should be easy to swap that out for any other payload.

If you drop the `python` plugin, you can also probably remove the `setup.py` and `requirements.txt` root files.

## Steps
How would you go about using this template for your python juju wrapper?

- Create a new repo using this one as template
- Put your code in place of `jujuwrapper/`
- Adjust the metadata and entry point in `setup.py`
- Overwrite requirements.txt with your own.
- Remove this README and add your own.
- Edit `snap/snapcraft.yaml`, filling in all templated blanks and replacing `jujuwrapper` with your tool's name. Add any extra interfaces you require.

You should be pretty much done! Your tool's runtime (when installed as a snap) will have access to the `juju` command via e.g. `Popen`, and `pylib-juju` should be able to connect to your local clouds.


# Snap interface notes

The `network` and `network-bind` interfaces are required for the embedded juju snap to be able to talk to your (local) clouds such as microk8s or lxd.
The `juju-client-observe` gives read access to `.local/share/juju`, which is where a local juju client will typically store its state (known controllers, credentials, etc...).
The juju client however also requires write access to `.local/share/juju`, to update said state, hence the `dot-local-share-juju:personal-files` interface.

So there is some manual connecting to be done to get the snap running. After you install it, you are going to need to manually run:

   sudo snap connect jujuwrapper:network snapd
   sudo snap connect jujuwrapper:network-bind snapd       
   sudo snap connect jujuwrapper:dot-local-share-juju snapd
   sudo snap connect jujuwrapper:juju-client-observe snapd

When you release, you should probably request for them to be auto-connect-enabled.

# Demo run

To run this project as a demo:

   snapcraft
   sudo snap install --dangerous ./jujuwrapper_0.1_amd64.snap

   snap connect jujuwrapper:juju-client-observe snapd:juju-client-observe
   snap connect jujuwrapper:dot-local-share-juju snapd
   
now you can:
    
    jujuwrapper status  # get juju status
    jujuwrapper filter traefik  # list traefik-k8s/* units