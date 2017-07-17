### Rough Strategy

The snake starts by building a grid of the board based on the data. Note that if any snakes are larger than us we consider any spaces it could move next turn as dangerous, but if we're larger than them we count those spaces as safe because we would just kill them if a collision were to happen. We then make a priority list of the goals starting with the gold, then the food, sorted by distance to the center. We chose distance from the center rather than from ourselves because the gold always spawns in the center. So we wanted to have the best chance of being near the gold when it spawned (Winning by getting 5 gold coins was OP). We skip all goals that any other snake is closer to.
Once a goal is selected, we update what the board would look like if we took our intended path to get there, if after getting to the goal there is no clear path to our tail, then we skip that goal.

If no goals are suitable (i.e. we're not closest to them, and the are not safe), then we just take the shortest path to our own tail, allowing us to loop "forever" until a goal spawns that satisfies our conditions. If we can't get to our tail, I think we just make a random move that isn't into a wall (we probably ran out of time). Another solution would be to try to path to another snake's tail, and just follow them until a goal appears or our own tail becomes visible.

### Next Steps / Ideas

* Implement some sort of space filling algorithm
* Search out the largest empty spaces and try to hang out there
* Purposely position to kill other snakes - maybe make traps out of existing food if healthy enough?
* Identify "easy kill" scenarios (i.e. when you are in control of another snakes choke point)
* Voronoi heuristic for when snakes are really long (see https://www.a1k0n.net/2010/03/04/google-ai-postmortem.html)
* Either avoid or master endgame (Once snakes are super long, and space is slim, the optimal strategy probably changes, either kill of other snakes before this happens, or figure out a good strategy that avoids getting wrecked by RNG once walls start spawning in your face)

# battlesnake-python

A simple [BattleSnake AI](http://battlesnake.io) written in Python. 

Visit [battlesnake.io/readme](http://battlesnake.io/readme) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#### You will need...

* a working Python 2.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
* experience [deploying Python apps to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction)
* [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1) [Fork this repo](https://github.com/sendwithus/battlesnake-python/fork).

2) Clone repo to your development environment:
```
git clone git@github.com:username/battlesnake-python.git
```

3) Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):
```
pip install -r requirements.txt
```

4) Run local server:
```
python app/main.py
```

5) Test client in your browser: [http://localhost:8080](http://localhost:8080).

## Deploying to Heroku

1) Create a new Heroku app:
```
heroku create [APP_NAME]
```

2) Deploy code to Heroku servers:
```
git push heroku master
```

3) Open Heroku app in browser:
```
heroku open
```
or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4) View server logs with the `heroku logs` command:
```
heroku logs --tail
```

## Questions?

Email [battlesnake@sendwithus.com](mailto:battlesnake@sendwithus.com), or tweet [@send_with_us](http://twitter.com/send_with_us).
