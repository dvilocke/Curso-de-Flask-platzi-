

def decorador(f):
    def envoltura(*args):
        print('hola')
        print(f(*args))
    return envoltura


@decorador
def suma(a, b):
    return a+b

@decorador
def su(a,b,c):
    return a+b+c


x = decorador(su)

suma(1,2)
su(1,2,3)