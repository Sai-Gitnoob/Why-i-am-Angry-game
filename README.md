# Why-i-am-Angry-game
# Why Am I Angry Today? 🎮

*A Relationship Survival Simulator built with Python and Pygame*

---

## Overview

**Why Am I Angry Today?** is a short interactive **visual novel-style game** developed using **Python and the Pygame library**.

In this game, the player returns home after a long day only to find their girlfriend upset. The problem? She says *“Nothing.”*

The player must navigate through dialogue and guess the reason for her anger. Choose wisely — one wrong guess and you might end up sleeping on the couch.

The game demonstrates how **scene-based storytelling, dialogue animation, asset management, and background music** can be implemented using Pygame.

---

## Features

* 🎭 **Visual Novel Style Dialogue System**
* 🖱️ **Interactive Choice-Based Gameplay**
* 🎵 **Dynamic Background Music System**
* 🪟 **Scene Transitions with Fade Effects**
* 💬 **Animated Typewriter Text Effect**
* 🖼️ **Backgrounds and Character Sprites**
* 🎮 **Menu System**
* 💡 **Simple Scene Graph Architecture**

---

## Gameplay

The story progresses through **dialogue scenes** and **player choices**.

### Example Flow

1. Player arrives home.
2. Girlfriend appears angry.
3. Player asks what happened.
4. She says: **"Nothing."**
5. Player must guess why she is upset.

Possible outcomes:

* ❌ **Game Over — Sleeping on the Couch**
* ✅ **Successful Ending — Sleeping in the Bed**

---

## Project Structure

```
project-folder/
│
├── main.py
│
├── Game Images/
│   ├── icon.png
│   ├── backgroundLight.png
│   ├── backgroundDark.png
│   ├── bedroom.png
│   ├── charNeutral.png
│   ├── charAngry.png
│   ├── charHappy.png
│
├── music/
│   ├── 1. Intro Song.mp3
│   ├── 2. Normal Convo.mp3
│   ├── 3. Guessing Reasons.mp3
│   ├── 4. She angry.mp3
│   ├── 5. Couch ending.mp3
│   ├── 6. Successful Ending.mp3
│
└── README.md
```

---

## Technologies Used

* **Python 3**
* **Pygame**

Pygame handles:

* window rendering
* event handling
* audio playback
* animations
* asset loading

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/why-am-i-angry-today.git
cd why-am-i-angry-today
```

### 2. Install dependencies

```bash
pip install pygame
```

### 3. Run the game

```bash
python main.py
```

---

## Controls

| Action            | Control                     |
| ----------------- | --------------------------- |
| Continue dialogue | Left Mouse Click            |
| Select choices    | Left Mouse Click            |
| Toggle fullscreen | F                           |
| Quit game         | Close window or Quit button |

---

## Game Architecture

The game uses a **scene-based architecture**.

Each scene is defined in a dictionary containing:

* dialogue text
* background image
* character sprite
* music track
* scene type
* next scene

Example:

```python
"intro":{
"texts":[
"You come home after a long day...",
"Your girlfriend looks angry."
],
"type":"story",
"next":"ask",
"bg":"bg_livingroom",
"char":"char_angry",
"music":"music/2. Normal Convo.mp3"
}
```

Scene types include:

| Scene Type | Description               |
| ---------- | ------------------------- |
| `menu`     | Main menu with buttons    |
| `story`    | Dialogue progression      |
| `choice`   | Player decision selection |

---

## Key Systems

### 1. Dialogue Animation

The game uses a **typewriter effect** that reveals characters gradually to simulate natural dialogue.

This improves pacing and player immersion.

---

### 2. Asset Loader

All images are defined in an `asset_map` and loaded automatically when the game starts.

Benefits:

* centralized asset management
* easier debugging
* automatic fallback if files are missing

---

### 3. Music System

The game includes a **dynamic music manager** that:

* prevents unnecessary track restarts
* allows smooth transitions between scenes
* changes music based on emotional tone

---

### 4. Scene Fade Transitions

Scenes transition using a **fade-to-black animation** to create smoother story flow.

---

### 5. Choice System

Players interact through clickable UI buttons.

Choices determine which scene loads next.

---

## Learning Objectives

This project demonstrates:

* Game loops
* Event-driven programming
* Scene management
* Basic UI systems
* Animation techniques
* Asset pipelines
* Audio management in games

It is a great **beginner-to-intermediate project for learning game development with Python**.

---

## Possible Future Improvements

Potential upgrades include:

* 💾 Save / Load system
* 🎧 Sound effects for dialogue
* 📱 Responsive UI scaling
* 🎨 Multiple character expressions
* 🧠 More branching storylines
* 📜 Dialogue history log
* ⚙️ Settings menu
* 🎮 Controller support

---

## Author

**Sai Tukrul**

Bachelor of Science in **Artificial Intelligence & Machine Learning**
IIT Jodhpur

GitHub:
https://github.com/yourusername

---

## License

This project is released under the **MIT License**.

You are free to:

* use
* modify
* distribute

with proper attribution.

---

## Final Note

This project was created as a **fun experiment combining storytelling and Python game development**.

If you enjoyed it, feel free to ⭐ the repository!
