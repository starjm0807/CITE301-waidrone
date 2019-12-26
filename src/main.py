from multiprocessing import Manager

import Drone
import Mic
import Packet

if __name__ == '__main__':
    # TODO: 마이크가 돌아가버릴 경우
    # TODO: 드론 고도 조정 문제

    d_coordinate = Manager().Value(Packet.Coor, None)
    # func = Drone.aud_wasdrfd
    func = Drone.aud_track_basic
    Drone.init(d_coordinate, func)
    Mic.init(d_coordinate)
