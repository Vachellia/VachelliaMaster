class Shops(object):

    def __init__(self):
        super().__init__()

    def test(self, parameters):
        print("[Shops][test][parameters] -> ", parameters)
        if parameters[0] == "result":
            print("[Shops][test][result] -> ", self.result)