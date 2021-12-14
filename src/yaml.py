
# From PyYAML version 5.1, the yaml.load api is changed to be more explicit (https://github.com/yaml/pyyaml/blob/5.1/lib3/yaml/__init__.py#L103)
# To avoid yaml warning like this one:
# YAMLLoadWarning: calling yaml.load() without Loader=... is deprecated, as the default Loader is unsafe. Please read https://msg.pyyaml.org/load for full details.
myYAML = yaml.load(configurationFile)
# Translate it to:
myYAML = yaml.load(configurationFile, yaml.SafeLoader)
# Possible values: SafeLoader, FullLoader, Loader (UnsafeLoader is the same as Loader)
#    src: https://stackoverflow.com/questions/55677397/why-does-pyyaml-5-1-raise-yamlloadwarning-when-the-default-loader-has-been-made/56455769

#
