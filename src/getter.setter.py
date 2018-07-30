    @property                           # getter/setter # "prop" property
    def prop(self):
        return self.__prop
    @prop.setter
    def prop(self, value):
        if isinstance(value, (str)):
            self.__prop = value
