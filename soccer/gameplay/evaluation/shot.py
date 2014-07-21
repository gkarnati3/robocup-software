import constants
import evaluation.window_evaluator
import robocup
import math


# returns a tuple (chance of shot success, best window)
# the chance of shot success is a value from 0 to 1
# @param windowing_excludes - A list of robots to exclude from the window evaluator
# if debug is True, it draws some stuff on the field - TODO: which stuff?
def eval_shot(pos, target=constants.Field.TheirGoalSegment, windowing_excludes=[], debug=False):
    win_eval = evaluation.window_evaluator.WindowEvaluator()
    win_eval.excluded_robots = windowing_excludes
    windows, best = win_eval.eval_pt_to_seg(pos, target)

    if best != None:
        shot_vector = best.segment.center() - pos
        shot_dist = shot_vector.mag()

        angle_between_shot_and_window = abs(shot_vector.angle() - best.segment.delta().angle())
        if angle_between_shot_and_window > math.pi / 2.0:
            angle_between_shot_and_window -= math.pi / 2.0

        # we don't care about the segment length, we care about the width of the corresponding segment perpendicular to the shot line
        perp_seg_length = math.sin(angle_between_shot_and_window) * best.segment.length()

        # the 'width' of the shot in radians
        angle = abs(math.atan2(perp_seg_length, shot_dist))

        # the wider available angle the shot has, the more likely it will make it
        # the farther the shot has to travel, the more likely that defenders can block it in time
        ShotAngleBaseline = (math.pi / 16.0)    # note: this angle choice is fairly arbitrary - feel free to tune it
        angle_score = min(angle / ShotAngleBaseline, 1.0)
        longest_possible_shot = math.sqrt(constants.Field.Length**2 + constants.Field.Width)
        dist_score = 1.0 - (shot_dist / longest_possible_shot)
        shot_chance = 0.6*angle_score + 0.4*dist_score  # note: the weights are fairly arbitrary and can be tuned

        # print('angle_score=' + str(int(angle_score * 100)) + "; distscore='" + str(dist_score*100))

        if debug:
            # raise NotImplementedError("Draw the shot chance on the line")
            # raise NotImplementedError("draw the shot line and window")
            pass

        return shot_chance, best
    else:
        return 0.0, None
