# Path-planning-task
Solution Overview
The final solution is a simple, robust "zigzag" path planner. The core idea is to prioritize predictability and accuracy over complex, realistic curves. The path is generated in two distinct, straight-line segments:
1.	Alignment Segment: A short, straight line that starts at the car and travels in the exact direction of its current yaw. This fulfills the critical requirement of aligning the path with the car's orientation.
2.	Target Segment: After the alignment segment, the path makes a single, sharp turn and proceeds in another straight line towards the calculated center of the track.
This approach was chosen because it's easy to understand and simple to do
________________________________________
Core Concepts Used
The algorithm is built on two simple but powerful ideas:
1. Centroid-Based Targeting
The "brain" of the planner is its ability to find the center of the track. It does this by calculating the centroid (or the average (x, y) position) of the cone groups.
•	If it can see both blue and yellow cones, it calculates the centroid for each color group and aims for the midpoint between them.
•	This is a very robust method because it automatically handles any number of cones. If you have three or even five blue cones, the centroid simply becomes the average position of all of them, which gives a stable and accurate representation of the track's left boundary.
2. Two-Segment "Zigzag" Path
This concept directly addresses the need for the path to respect the car's initial direction.
•	By dedicating the first segment of the path (ALIGNMENT_DISTANCE) to traveling straight, we ensure the car doesn't try to turn in an unrealistic way right from the start.
•	The second segment's sharp turn is a simplifying assumption. While not perfectly realistic, it makes the path's behavior completely predictable and easy to calculate, avoiding the instabilities we saw with curved paths.
________________________________________
How the Solution Evolved (Problems & Fixes)
Our journey to this final solution involved trying different methods and learning from their limitations:
•	First Idea (Simple Sharp Turns): We then switched to a much simpler sharp-turn method.
o	Limitation: The initial logic for finding a target was too basic. It failed in scenarios with multiple cones on one side (like scenario 7 and 11), sometimes aiming the path through the track boundary instead of between the correct cones.
•	Final Solution (Tuned Zigzag): This version keeps the simplicity of the sharp-turn method but uses the robust centroid targeting logic.
o	How it Solved the Problems: The centroid logic ensures the target is always in the correct place, regardless of the cone layout. 
________________________________________
Handling Part 1 and Part 2 of the Assignment
This solution directly addresses all the requirements from the README.md file.
Part 1: Basic Path Generation
The generatePath function inside the PathPlanning class was implemented to solve the core problem. It correctly handles all the required cases:
•	Two Cones (Blue and Yellow): It calculates the midpoint between the two and aims for it.
•	One Cone (or one color group): It uses the ASSUMED_TRACK_WIDTH to calculate a target point offset from the visible cones.
•	No Cones: It generates a simple path straight ahead based on the car's current yaw.
Part 2: Handling Three or More Cones
The solution handles the case of three cones on one side of the track elegantly and without needing any special code.
•	Implementation: The use of centroid calculation is the key. By averaging the positions of all visible cones of a single color, the algorithm naturally finds the center of that boundary, whether it's defined by one cone or ten.
•	New Test Cases: Three new scenarios (24, 25, and 26) were added to the src/scenarios.py file to test this functionality with more complex track layouts, including sharper turns and immediate gates.
•	Limitations of this Solution:
1.	Non-Realistic Turns: The primary limitation is that the path contains an instantaneous, sharp turn, which is not physically possible for a real car. This is a deliberate simplification to ensure accuracy and robustness.
2.	Fixed Track Width Assumption: When only one side of the track is visible, the algorithm must rely on the hardcoded ASSUMED_TRACK_WIDTH constant. If the actual track is wider or narrower at that point, the generated path will not be perfectly centered.

