import json

class UserNotInFile(Exception):
    pass

class JF():
    def __init__(self, jsonfile):
        self.file = jsonfile

    def __write(self, data):
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    def __getall(self):
        with open(self.file) as f:
            return json.load(f)
        
    def __user_in_file(self, userid):
        all = self.__getall()
        if all.get(str(userid)) == None:
            return False
        return True

    def get_points(self, userid):
        all = self.__getall()
        try:
           points = all[str(userid)]
        except KeyError:
            return 0
        else:
            return points

    def order(self):
        all = self.__getall()
        return sorted(all.items() , reverse=True, key=lambda x: x[1])
            

    def change_points(self, userid, points):
        all = self.__getall()
        if self.__user_in_file(str(userid)):
            if self.get_points(str(userid)) + points <= 0:
                all[str(userid)] = 0
            else:
                current_points = all[str(userid)] 
                all[str(userid)] = current_points + points
        else:
            if points <= 0:
                all.update({str(userid): 0})
            else:
                all.update({str(userid): points})
        self.__write(all)


if __name__ == '__main__':
    x = JF("points.json").order()
    print(x)