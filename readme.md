For my senior project in college I studied my mouse's maze. It was a 4 x 4 maze, with an entrance and an 
exit. In the center were slots to insert the 10 provided walls. Try as I could, I could not place all 10 
walls in the maze without sectioning off an area. My goal was to determine, is there any possible way to 
place all 10 walls without sectioning off an area?

Using Euler's Formula for Planar Graphs, you can show that the maximum number of walls in a rectangular 
m x n maze is (m-1)(n-1). Using Cayley's Theorem for Counting Forests you can count unstructured mazes. 
But I've never been able to answer the question of how many strict mazes could be built for an m x n maze.

After I graduated, I dropped my concern with mazes, but about one week ago I decided to dust off my old ideas 
and put them to practice. I wanted to know more about mazes, get into the mathematical framework of how they 
work.

I started building a program to draw out a randomized maze, a maze that I could choose the dimensions, 
and determine the qualities and characteristics of a maze, and hopefully gain a deeper insight to hopefully 
one day determine a strong proof on the number of possible mazes given certain dimensions.

Here are some ideas and difficulties I ran into:

1. You can build a maze, with the maximum number of walls, by initializing a grid of points with dimension 
(m-1)(n-1) on the interior of the perimeter, then by randomly assigning a direction, (left,up,right,down) 
to each gridpoint. It seems like you should be able to raise 4 to the power of (m-1)(n-1) to determine the 
possible outcomes:
-----a. However you run into the possibility of one wall headed right, and another wall headed left that you 
have to account for not providing a valid maze
-----b. You also run into the possibility of creating a cycle, which sections off an area of the maze.
----------i. (Algorithm) After randomly assigning your wall, you can check if traveling the path created 
from previous walls assigned leads you back to a point already visited. Move to the wall's destination --o 
record that point --o move to the next wall's destination --o ... --o you will either eventually hit the 
perimeter of your maze, validating your direction assignment or you will visit a point you have already 
visited before.

2. You can count the number of trees that sprout from the perimeter
-----a. Checking the inner perimeter gridpoints destination and counting if it hit's the perimeter 
accomplishes this

3. You can determine a tree that shows all the possible paths that you can take in the maze (and finally 
the solution path)
-----a. Assuming you start at the top left, and you finish at the bottom right, it is sufficient to check 
if at each position you can move to the right or down (except if you are in the last column or row, you 
cannot move right or down respectively).
-----b. By looping through the tree's edges, you can trim off an edge that has a unique position point, 
since that point is not part of the unbroken path from the entrance to the exit.

4. Data can be derived from these trees, such as the length of the solution path, or the number of trees 
in the walls, and not so surprisingly, the distribution seems to be normal at initial histogram inspection.
-----a. Is it even useful??? Are there any real world applications for these mazes??

It's only been a week, so I got a lot to stew on, a lot to reevaluate, and a lot to improve. Hopefully I 
continue this trend of posting progress, but I wanted to share, since I thought it was interesting. Thank 
you for reading!
