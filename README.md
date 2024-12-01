<div align="center">

  <h1>Pen-Plotting Robot</h1>
  
  <p>
    An open-source, python-based cartesian pen-plotting robot for CS education
  </p>
  

<h4>
    <a href="https://github.com/Louis3797/awesome-readme-template/">View Demo</a>
  <span> · </span>
    <a id = #documentation href="https://github.com/Louis3797/awesome-readme-template">Documentation</a>
  <span> · </span>
    <a href="https://cad.onshape.com/documents/94f0b3225bc3cee80dd6bd7f/w/86bde690ac0739bb1e270967/e/8b0488b3bb58129bb2a0aa1e">CAD Model</a>
  <span> · </span>
    <a href="https://github.com/Louis3797/awesome-readme-template/issues/">More</a>
  </h4>
</div>

<br />

<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#about-the-project)
  * [Motivation](#motivation)
  * [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  * [Prerequisites](#bangbang-prerequisites)
  * [Installation](#gear-installation)
    * [Step 1: Set up Micropython](#step-1-set-up-micropython)
    * [Step 2: Edit script.py and other files locally:](#step-2-edit-scriptpy-and-other-files-locally)
  * [Editing Code](#editing-code)
    * [How Everything Works](#how-everything-works)
    * [About `bot.py`](#about-botpy)
    * [Asyncronous Programming](#asyncronous-programming)
    * [Key Functions](#key-functions)
  * [Run Locally](#running-run-locally)
    * [Run Code](#run-code)
    * [Upload Files](#upload-files)
    * [Important: Key Tips](#key-tips)
  * [Deployment](#triangular_flag_on_post-deployment)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)

  

<!-- About the Project -->
## About the Project

### Motivation
This project was in response to a request by the EGR105L first-year computing course at Duke University. 


<div align="left"> 
  <img src="images/robotpic.jpg" width = "600px"/>
</div>


<!-- TechStack -->
### Tech Stack

- Micropython: An efficient implmentation of the Python 3 language optimized for running on microcontrollers.
  - `bot.py`: A low level library that deals with robot control and direct microcontroller communication as well as simple controls functions so you can focus on developing higher-complexity algorithms.
  - `main.py` and `boot.py`: ESP32 native files that are run upon startup.
  - `script.py`: A canvas for the user to write and test their own commands and methods.
- HTML/JS/CSS: Implementation of a socket web server for a User Interface and diagnostic dashboard.

<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### Prerequisites


Before starting this project, you should have some sort of code editor installed (VSCode highly recommended) as Thonny IDE is not a good development environment and mostly serves as a conduit to run the ESP32 microcontroller on the robot. You should also have the assembled robot (see [Documentation](https://www.google.com) for more information) and an ESP32.

Additionally, it is highly recommended that you have git installed and set up, and that you fork this repository, since you will need to make changes to `script.py`. You are welcome to play around with any files, but for the smoothest results, it is recommended that you do not modify `main.py`, `boot.py`, `bot.py`, or `interface.html`, instead using the UI and `script.py` to do any robot operations you need.

<!-- Installation -->
### Installation

#### Step 1: Set up Micropython 

If you have not installed micropython on your ESP32 or downloaded Thonny, start here. If you've already completed these two steps or are working with an already setup robot, skip to the next step.

First, go to the [Thonny IDE](https://thonny.org/) website and download the correct version according to your operating system.

Next, plug in the ESP32 microcontroller into your computer and open Thonny. Click `Run -> Configure Interpreter -> Which kind of interpreter? -> Select Micropython (ESP32)`.
<div align="left"> 
<br>
  <img src="images/step1-mp.png" alt="screenshot" width="600px"/>
</div>
<br>

Next, click `Install or Update MicroPython` and using the following options, install micropython. Usually, the correct port option will say something like "USB Serial" or "UART", but depends on your device and the ESP-32 you have. After you've selected the right port, you should click `install`. This will take a minute or two.

<br>
<div align="left"> 
  <img src="images/step1-mp-flash.png" alt="screenshot" width="600px"/>
</div>
<br>

Now, you should have both Thonny set up and installed Micropython on your ESP32. You can test this by connecting your device in Thonny In the main menu, select `Run -> Configure Interpreter -> Which kind of interpreter? -> Select Micropython (ESP32)` and select `<Try to detect port automatically>`. Once you connect by pressing `OK`, you should be able to type basic commands in the REPL (Terminal) like below. If this works, then you have successfully completed configuration. If not, start Step 1 again, and if issues persist, consult Google or contact us.

<br>

<div align="left"> 
  <img src="images/step1-mp-completed.png" alt="screenshot" width="800px"/>
</div>

<br>

#### Step 2: Edit script.py and other files locally:

First, fork this repo. You can do that at the top with the button that says `Fork`. 

Next, open your terminal (or the terminal in VS Code or other IDEs of your chosing) and clone the repo with either HTTPS or SSH (SSH recommended).

```bash
git clone git@github.com:srinath-iyer/Pen-Plotting-Bot.git
```

Additionally, if you don't want to use git, you can export the repo as a zip file and open it in any IDE.

<br>

Next, change the JSON in `network.txt`. If you are joining an open network, just change the network SSID, and set the Password parameter to `None`. If you are joining a network that requires a password, set the Password parameter as well. For example, `network.txt` should be like the following:

Open: 
```bash
{"SSID":"DukeOpen","Password":"None"}
```

Closed:
```bash
{"SSID":"ClosedNetwork","Password":"1234"}
```
You can test that your wifi setup works, and we recommend this before you start coding. Plug in the ESP-32, and open Thonny. In our experience, Thonny sometimes auto connects, and causes the ESP32 to start running the files. If that happens, wait for this in the REPL:

<div align="left"> 
  <img src="images/step2-wifi-success.png" alt="screenshot" width="800px"/>
</div>

If you don't see the ESP-32 running immediately, go to `Run -> Configure Interpreter -> Pick the right Port -> Ok` and the ESP-32 should run. If it doesn't run after connecting, press the `EN` button on the ESP-32. If it still doesn't work, try configuring the interpreter again.

Once you have successfully connected to the network of your choice, you are ready to begin editing `script.py`. 


<!-- Running Tests -->
### :test_tube: Editing Code

#### How Everything Works

Before you start to work with the code, we think it's important that you should know how everything works. As mentioned earlier, the 

#### About `bot.py`

#### Asyncronous Programming

#### Key Functions

To run tests, run the following command

```bash
  yarn test test
```

<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/Louis3797/awesome-readme-template.git
```

Go to the project directory

```bash
  cd my-project
```

Install dependencies

```bash
  yarn install
```

Start the server

```bash
  yarn start
```


<!-- Deployment -->
### :triangular_flag_on_post: Deployment

To deploy this project run

```bash
  yarn deploy
```

<!-- FAQ -->
## :grey_question: FAQ

- Question 1

  + Answer 1

- Question 2

  + Answer 2


<!-- License -->
## :warning: License

Distributed under the MIT License. See LICENSE.txt for more information.


<!-- Contact -->
## :handshake: Contact

Srinath Iyer - srinath.iyer@duke.edu
<br>
Niko Weaver - niko.weaver@duke.edu
<br>
Kelvin Zhang - kelvin.zhang@duke.edu
<br>
Jack Voelker - jack.voelker@duke.edu


<!-- Acknowledgments -->
## Acknowledgements

We would like to thank Duke University, and the Pratt School of Engineering First Year Design program for providing us financial support and mentorship.

Specifically, we would like to extend our gratitude to Dr. Delagrammatikas, Dr. Lipp, Dr. Smith, Dagan Trnka, and Rodrigo Bassi Guerreiro for their assistance on this project.
