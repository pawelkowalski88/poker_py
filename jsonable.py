import datetime
import decimal
import json

class Jsonable(object):
    def __iter__(self):
        for attr, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                iso = value.isoformat()
                yield attr, iso
            elif isinstance(value, decimal.Decimal):
                yield attr, str(value)
            #elif(hasattr(value, '__iter__')):
            elif hasattr(value, 'pop'):
                a = []
                for subval in value:
                    if(isinstance(subval, Jsonable)):
                        a.append(dict(subval))
                    else:
                        a.append(subval)
                yield attr, a
            elif(isinstance(value, Jsonable)):
                yield attr, dict(value)
            else:
                yield attr, value

class Identity(Jsonable):
    def __init__(self):
        self.name="abc name"
        self.first="abc first"
        self.addr=[Addr(), Addr()]

class Addr(Jsonable):
    def __init__(self):
        self.street="sesame street"
        self.zip="13000"

class Doc(Jsonable):
    def __init__(self):
        self.identity=Identity()
        self.data="all data"


def main():
    doc=Doc()
    print ("-Dictionary- \n")
    print (dict(doc))
    print ("\n-JSON- \n")
    print (json.dumps(dict(doc), sort_keys=True, indent=4))

if __name__ == '__main__':
    main()
    #defg = {}
    # abc = Doc()
    # print(isinstance(abc, Jsonable))