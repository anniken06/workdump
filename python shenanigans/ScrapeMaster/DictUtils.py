class InfiDict(dict):
    def nw(x,y): return InfiDict({x:y})

    def iget(self, *keys):
        if len(keys) > 0:
            value = self.get(keys[0])
            if issubclass(dict, type(value)):
                return InfiDict(value).iget(*keys[1: ])
            return value 
        return self

    def isetval(self, *keys, value=None):
        raise Exception('shit')
        if len(keys) > 1:
            self.isetval(*keys[ :-1], value=InfiDict({keys[-1]: value}))
        else:
            self[keys[0]] = value

    def isetval2(self, *keys, value=None):
        raise Exception('shit')
        if len(keys) > 1:
            existing_value = self.iget(keys[-1])
            existing_value[keys[-1]] = value
            self.isetval2(*keys[ :-1], value=existing_value)
        else:
            self[keys[0]] = value


if __name__ == '__main__':
    x = InfiDict()
    y = InfiDict({1:2})
    z = InfiDict({1:{2:3}})
    x.isetval2(1,2,3, value=100)
    print(x)
    x.isetval2(1,2,4, value=1001)
    print(x)
    import code; code.interact(local={**locals(), **globals()})
