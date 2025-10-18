from __future__ import annotations

import math
from typing import List, Tuple

from src.models import CarPose, Cone, Path2D


class PathPlanning:
    PATH_STEP_SIZE = 0.5
    TOTAL_PATH_LENGTH = 10.0
    ASSUMED_TRACK_WIDTH = 3.0
    ALIGNMENT_DISTANCE = 0.5

    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        blue_cones = []
        yellow_cones = []
        for cone in self.cones:
            if cone.color == 1:
                blue_cones.append(cone)
            else:
                yellow_cones.append(cone)

        start_point = (self.car_pose.x, self.car_pose.y)

        turn_point_x = start_point[0] + self.ALIGNMENT_DISTANCE * math.cos(self.car_pose.yaw)
        turn_point_y = start_point[1] + self.ALIGNMENT_DISTANCE * math.sin(self.car_pose.yaw)
        turn_point = (turn_point_x, turn_point_y)

        end_target = self._calculate_target_point(blue_cones, yellow_cones)

        path = self._create_zigzag_path(start_point, turn_point, end_target)
        return path

    def _get_centroid(self, cones: List[Cone]) -> Tuple[float, float] | None:
        if len(cones) == 0:
            return None
        
        sum_x = 0.0
        sum_y = 0.0
        for cone in cones:
            sum_x = sum_x + cone.x
            sum_y = sum_y + cone.y
        
        num_cones = len(cones)
        return (sum_x / num_cones, sum_y / num_cones)

    def _calculate_target_point(
        self, blue_cones: List[Cone], yellow_cones: List[Cone]
    ) -> Tuple[float, float]:
        blue_centroid = self._get_centroid(blue_cones)
        yellow_centroid = self._get_centroid(yellow_cones)
        
        target_x = 0.0
        target_y = 0.0

        if blue_centroid is not None and yellow_centroid is not None:
            target_x = (blue_centroid[0] + yellow_centroid[0]) / 2.0
            target_y = (blue_centroid[1] + yellow_centroid[1]) / 2.0
        
        elif blue_centroid is not None:
            dir_to_centroid_x = blue_centroid[0] - self.car_pose.x
            dir_to_centroid_y = blue_centroid[1] - self.car_pose.y
            offset_x = dir_to_centroid_y
            offset_y = -dir_to_centroid_x
            magnitude = math.sqrt(offset_x**2 + offset_y**2)
            if magnitude > 0:
                offset_x = (offset_x / magnitude) * (self.ASSUMED_TRACK_WIDTH / 2.0)
                offset_y = (offset_y / magnitude) * (self.ASSUMED_TRACK_WIDTH / 2.0)
            target_x = blue_centroid[0] + offset_x
            target_y = blue_centroid[1] + offset_y

        elif yellow_centroid is not None:
            dir_to_centroid_x = yellow_centroid[0] - self.car_pose.x
            dir_to_centroid_y = yellow_centroid[1] - self.car_pose.y
            offset_x = -dir_to_centroid_y
            offset_y = dir_to_centroid_x
            magnitude = math.sqrt(offset_x**2 + offset_y**2)
            if magnitude > 0:
                offset_x = (offset_x / magnitude) * (self.ASSUMED_TRACK_WIDTH / 2.0)
                offset_y = (offset_y / magnitude) * (self.ASSUMED_TRACK_WIDTH / 2.0)
            target_x = yellow_centroid[0] + offset_x
            target_y = yellow_centroid[1] + offset_y
            
        else:
            target_x = self.car_pose.x + math.cos(self.car_pose.yaw) * self.TOTAL_PATH_LENGTH
            target_y = self.car_pose.y + math.sin(self.car_pose.yaw) * self.TOTAL_PATH_LENGTH
        
        return (target_x, target_y)

    def _create_zigzag_path(self, start, turn, end) -> Path2D:
        path: Path2D = [start]
        current_pos = start
        total_dist_traveled = 0.0

        dist_1 = math.sqrt((turn[0] - start[0])**2 + (turn[1] - start[1])**2)
        if dist_1 > 0:
            dir_x_1 = (turn[0] - start[0]) / dist_1
            dir_y_1 = (turn[1] - start[1]) / dist_1
            
            num_steps = int(dist_1 / self.PATH_STEP_SIZE)
            for i in range(num_steps):
                current_pos = (current_pos[0] + dir_x_1 * self.PATH_STEP_SIZE,
                               current_pos[1] + dir_y_1 * self.PATH_STEP_SIZE)
                path.append(current_pos)
                total_dist_traveled += self.PATH_STEP_SIZE
        
        current_pos = turn
        if path[-1] != turn:
            path.append(turn)

        dist_2 = math.sqrt((end[0] - turn[0])**2 + (end[1] - turn[1])**2)
        if dist_2 > 0:
            dir_x_2 = (end[0] - turn[0]) / dist_2
            dir_y_2 = (end[1] - turn[1]) / dist_2

            while total_dist_traveled < self.TOTAL_PATH_LENGTH:
                current_pos = (current_pos[0] + dir_x_2 * self.PATH_STEP_SIZE,
                               current_pos[1] + dir_y_2 * self.PATH_STEP_SIZE)
                path.append(current_pos)
                total_dist_traveled += self.PATH_STEP_SIZE
                
        return path