

def test(string, *args):
    print(string.format(*args))


x = "Josh"
y = "Alex"

test("My name is {0}", x)


"My naame is %s" % "Josh"