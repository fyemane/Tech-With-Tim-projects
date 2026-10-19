# Tech With Tim — Python Projects

[Project portfolio](https://fyemane.github.io/projects.html) · [About me, experience & qualifications](https://fyemane.github.io/)


My collection of Python projects completed while following [Tech With Tim's tutorials](https://www.techwithtim.net/). These exercises helped me practise object-oriented programming, game loops, graphics, search algorithms, and introductory machine learning.

The repository brings together Pygame games, a NEAT-based Flappy Bird experiment, Sudoku and checkers exercises, and NumPy/OpenCV examples. Each folder is a separate project with its own entry point and assets.

## Project guide

| Folder | Project and concepts |
| --- | --- |
| [AI Plays Flappy Bird - NEAT Python](AI%20Plays%20Flappy%20Bird%20-%20NEAT%20Python) | Flappy Bird simulation with neural networks evolved using NEAT; fitness rewards, population evaluation, and collision handling |
| [Pygame Checkers Tutorial](Pygame%20Checkers%20Tutorial) | Board and piece classes, valid moves, captures, king promotion, and turn handling |
| [Pygame Checkers AI Tutorial](Pygame%20Checkers%20AI%20Tutorial) | Extension of the checkers game with recursive minimax search and board evaluation |
| [Pygame Tetris Tutorial](Pygame%20Tetris%20Tutorial) | Falling blocks, rotation, collision checks, line clearing, and a saved score |
| [Python Hangman Tutorial](Python%20Hangman%20Tutorial) | Word guessing with clickable letters and staged Hangman images |
| [Python Sudoku Solver Tutorial](Python%20Sudoku%20Solver%20Tutorial) | Backtracking solver and a Pygame grid interface |
| [TWT - SudokuPy](TWT%20-%20SudokuPy) | Another saved version of the Sudoku GUI and solver |
| [Space Shooting Tutorial](Space%20Shooting%20Tutorial) | Player/enemy ships, projectiles, collision checks, waves, and health |
| [TWT - Jump Jive Wail](TWT%20-%20Jump%20Jive%20Wail) | Animated player/enemy sprites, movement, jumping, projectiles, and audio |
| [TWT - Pygame Car Racing Tutorial](TWT%20-%20Pygame%20Car%20Racing%20Tutorial) | Car motion and rotation, mask-based track collisions, and finish-line logic |
| [Python Firework Animation Tutorial](Python%20Firework%20Animation%20Tutorial) | Particle motion, randomised explosions, gravity, and transparency-based fading |
| [TWT - Numpy Tutorial](TWT%20-%20Numpy%20Tutorial) | Array creation and numerical operations |
| [TWT - OpenCV Python Tutorial](TWT%20-%20OpenCV%20Python%20Tutorial) | Eight modules covering images, video, drawing, colour filtering, corners, template matching, and face/eye detection |

## Algorithms and learning experiments

### Flappy Bird with NEAT

The Flappy Bird project uses `neat-python` to evaluate a population of neural networks in the game. Birds receive fitness for surviving and passing pipes, and lose fitness when they collide. The network configuration is stored in `AI.txt`; the project also includes a saved `best.pickle` artifact.

This is an evolutionary learning exercise rather than a conventional labelled-data training pipeline. The simulation and rendering use Pygame, with game objects defined in `classes.py`.

### Checkers and Sudoku

The checkers exercises separate the board, pieces, game state, and search algorithm into modules. The AI entry point requests a minimax search depth of three. The checked-in algorithm does **not** implement alpha-beta pruning.

The Sudoku projects use recursive backtracking to search for a valid solution. Their GUI versions support selecting a cell, entering a candidate, confirming it, and deleting a pencilled entry.

### OpenCV and NumPy

The OpenCV modules progress from loading and manipulating image pixels to webcam input, drawing, colour masks, corner detection, template matching, and Haar-cascade face/eye detection. Webcam modules use camera index `0`; image examples use the assets stored beside the scripts. NumPy provides array operations used in these exercises.

## Running a project

Use a Python 3 environment and install the packages needed by the selected exercise. There is no shared requirements file or pinned environment in this repository.

| Projects | External packages |
| --- | --- |
| Games, Sudoku GUI, fireworks | `pygame` |
| Flappy Bird AI | `pygame`, `neat-python` |
| OpenCV modules | `opencv-python`, `numpy` |
| NumPy exercises | `numpy` |

For example, to run checkers:

```bash
python -m pip install pygame
cd "Pygame Checkers Tutorial"
python main.py
```

For the Sudoku GUI:

```bash
cd "Python Sudoku Solver Tutorial"
python GUI.py
```

For the Flappy Bird experiment, install `neat-python` as well, enter its folder, and run `main.py`. For OpenCV, enter its folder and choose a module such as `python module8.py` for face/eye detection.

Run scripts **from their own project folder** so relative image, audio, configuration, and score-file paths resolve. The games need a graphical desktop; webcam exercises also need camera access.

## Controls

| Project | Main controls |
| --- | --- |
| Checkers | Mouse selection of pieces and destination squares |
| Tetris | `A`/`D` move, `S` descend, `W` rotate |
| Space Shooting | `WASD` movement, Space to shoot |
| Jump Jive Wail | `A`/`D` movement, `W` jump, Space to shoot |
| Car Racing | `W`/`S` accelerate/reverse, `A`/`D` turn |
| Sudoku GUI | Click a cell, number keys to pencil an entry, Enter to confirm, Delete to clear |

The NEAT experiment controls the birds through neural-network outputs rather than manual play.

## Notes on this archive

These are saved tutorial implementations, not a single maintained application. A fresh run of every project has not been verified. Some folders contain generated bytecode, and the Sudoku work appears in two saved versions.

The checkers AI's minimizing branch currently uses `max()` when updating its minimum evaluation; that logic needs review before relying on its move choices. Older NEAT configurations may also need adaptation to the installed `neat-python` version. These notes describe the existing source; this README update doesn't change the programs.

## Samples

<img src="https://user-images.githubusercontent.com/93152842/190885847-4e9de84c-89ce-4b03-803c-ff02dd114ecf.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190885298-2a6cd1bd-7eb3-4ec6-9883-ad6886ad415a.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190885345-8e8d80a7-9f42-47a1-8c65-7a455d64d1f7.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190885390-53eae668-ec54-4cdd-adc2-7a6f9e120865.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884411-55e49339-f5de-4b73-85f0-24404b1abecc.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884478-3bb485af-c441-401e-b39d-f11d8b468518.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884545-d8b38ac8-510d-4e39-bdac-47b1186c543c.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884760-fa2e5a53-4f82-43c3-b497-a52e555e4e44.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884848-9e9935b3-cafe-49f3-84e2-b81ae61e895a.png" height=200> <img src="https://user-images.githubusercontent.com/93152842/190884945-3d109ed8-0b0b-49d4-ae6b-7b18e329862e.png" height=200>

## Credits

These projects follow Tech With Tim's tutorials. The tutorial structure, example assets, and underlying teaching material remain credited to their original creators. This repository records my implementations and learning exercises; it isn't a claim that the tutorial games or algorithms were independently designed by me.
