import json


class Packet:
    timeStamp = 0
    coordinates = [None] * 4

    def __init__(self, msg):
        dict = json.loads(msg)
        self.timeStamp = dict['timeStamp']
        src = dict['src']
        for i in range(0, 4):
            self.coordinates[i] = Coor(src[i])

    def max_coordinate(self):
        max_activity = 0.0
        _max_coordinate = None
        for temp_coordinate in self.coordinates:
            if max_activity <= temp_coordinate.activity:
                max_activity = temp_coordinate.activity
                _max_coordinate = temp_coordinate

        return _max_coordinate

    # def __trim_msg(self, msg):
    #     global remainingTrack
    #     remainingTrack += msg
    #     strings = remainingTrack.split('}\n{')
    #     if len(strings) < 2:
    #         remainingTrack = strings[0]
    #         return
    #     ans = {}
    #     for string, index in enumerate(strings):
    #         if index == len(strings) - 2:
    #             ans = string
    #         if index == len(strings) - 1:
    #             remainingTrack = string
    #             return ans


class Coor:
    id = 0
    tag = ''
    x = 0.0
    y = 0.0
    z = 0.0
    activity = 0.0

    def __init__(self, src):
        self.id = src['id']
        self.tag = src['tag']
        self.x = src['x']
        self.y = src['y']
        self.z = src['z']
        self.activity = src['activity']

    def __str__(self):
        return "id: {}, tag: {}, x: {}, y: {}, z: {}, activity: {}".format(
            self.id, self.tag, self.x, self.y, self.z, self.activity)
