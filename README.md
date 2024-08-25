# FlappyBirdAI
Pure python implementation of NEAT algorithm for FlappyBird game. (graphics in pygame).

https://github.com/user-attachments/assets/d0628bd3-a902-46c0-9474-92f8636bc0ce

> [!WARNING]
> Due to random nature of this algorithm it is possible there are bugs that I haven't encountered

# Downloading and running
### Clone this repository
    git clone https://github.com/hubertStanowski/FlappyBirdAI.git

### Go to its directory
    cd FlappyBirdAI

### Install packages (pygame)
    pip install -r requirements.txt

### Run the program
    python main.py
  
# Usage
### Default settings
You can modify these settings in user_config.py file

- Population size = 100
- Population staleness limit = 10
- Draw limit = 200
- Human playing = False

### Sensor view
- You can toggle sensor view by pressing **SPACE** button
- In sensor view you can see how the current best bird's neural network looks
- Each bird will also have red lines from its center to the closest bottom and top pipe
- Sensor view will also show you how many bird out of the current generation are still alive
- Sensor view displays actual FPS which may differ from set FPS depending on population size
- To turn off the sensor view press **SPACE** button again
### Resetting
- There is a population staleness limit for preventing unlucky mutations from running forever and when it's reached the population will automatically reset.
- If you want to reset the population manually press **BACKSPACE** or **DELETE** button.
### Game speed (FPS)
- You can speed up the game by pressing **PLUS** button
- You can slow down the game by pressing **MINUS** button
- FPS range is capped between 30 and 160 for best experience
- There is a draw limit, which allows to run big populations with less lag by simply not drawing all the birds, but depending on your computer you might want to lower it if lagging with <200 population size
### Additional information
- You can enable dying animations for the birds (falling to the ground) by pressing any **SHIFT** button and disable them by pressing it again
- If you want to see the population evolving keep the size <100, as with big population it is likely that there will be no need for evolution due to how uncomplicated FlappyBird is
- Too small population is more likely to get unlucky with all mutations, which will result in automatic reset after several generations of no improvement
# Resources
- https://youtu.be/WSW-5m8lRMs?si=Z0EUQAviZq7y31PR - inspiration (CodeBullet)

- https://flappybird.io/ - the original game

- https://youtu.be/0mKHcnQlVi0 - my demo video on YouTube (same as embeded above)
## NEAT
- https://neat-python.readthedocs.io/en/latest/neat_overview.html - overview

- https://www.youtube.com/watch?v=yVtdp1kF0I4 - great visual explanation

- https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf - original paper

- https://stackoverflow.com/questions/45463821/neat-what-is-a-good-compatability-threshold - compatibility threshold help

## Graphics
- https://www.spriters-resource.com/fullview/59894/ - full sprite sheet

- https://www.pixilart.com/draw - pixelart editor
