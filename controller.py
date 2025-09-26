#!/usr/bin/env python2

from periodic_turn import PeriodicTurn
from auto_drive import AutoDrive
from bumper_halter import BumperHalter
from avoid_obstacles import ObstacleAvoider

if __name__ == "__main__":
    AutoDrive = AutoDrive()
    PeriodicTurn = PeriodicTurn()
    BumperHalter = BumperHalter()
    ObstacleAvoider = ObstacleAvoider()
