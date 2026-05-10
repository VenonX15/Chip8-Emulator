# 🎮 Émulateur CHIP-8

> Un interpréteur CHIP-8 écrit en Python, permettant de jouer aux jeux classiques des années 70 comme Pong, Breakout ou Space Invaders directement sur votre machine.

---

## 📋 Table des matières

- [C'est quoi CHIP-8 ?](#️-cest-quoi-chip-8-)
- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Lancer un jeu](#-lancer-un-jeu)
- [Spécifications techniques](#️-spécifications-techniques)

---

## 🕹️ C'est quoi CHIP-8 ?

CHIP-8 est un langage de programmation intermédiaire créé dans les années 1970 par Joseph Weisbecker, conçu pour simplifier le développement de jeux vidéo sur les micro-ordinateurs de l'époque. Ce n'est pas une vraie console physique, mais une machine virtuelle (un environnement logiciel standardisé sur lequel les jeux pouvaient tourner.)

Ce projet émule fidèlement ce système, vous permettant de faire tourner les jeux d'origine sur votre ordinateur moderne.

---

## ✨ Fonctionnalités

- **Jeu d'instructions complet** - Les 35 opcodes CHIP-8 sont entièrement implémentés.
- **Affichage graphique** - Rendu via Pygame à la résolution d'origine 64×32 pixels.
- **Son** - Buzzer intégré déclenché par le timer sonore (ST).
- **Menu de jeu** - Interface pour naviguer, importer et sélectionner vos ROMs.
- **Clavier complet** - Support des touches directionnelles, Entrée, Échap et du pavé hexadécimal.

---

## 🔧 Prérequis

- **Python 3.8+** — [Télécharger Python](https://www.python.org/downloads/)
- Les dépendances listées dans `requirements.txt`

Pour vérifier votre version de Python, ouvrez un terminal et tapez :
```bash
python --version
```

---

## 📦 Installation

Ce projet peut être utilisé directement depuis l'archive fournie, ou cloné depuis GitHub.

---

### Option A — Depuis l'archive ZIP

**1. Extraire le dossier**

Faites un clic droit sur le fichier `.zip` reçu et choisissez **"Extraire tout"** (Windows) ou double-cliquez dessus (macOS/Linux). Placez le dossier extrait où vous le souhaitez.

**2. Ouvrir un terminal dans le dossier du projet**

- **Windows** : clic droit → *Ouvrir dans un terminal*.
- **macOS** : clic droit sur le dossier → *Nouveau terminal au dossier*.
- **Linux** : clic droit → *Ouvrir dans un terminal*.

**3. (Recommandé) Créer un environnement virtuel**

Un environnement virtuel permet d'installer les dépendances sans toucher à votre installation Python globale.

```bash
python -m venv venv

# Sur Windows :
venv\Scripts\activate

# Sur macOS / Linux :
source venv/bin/activate
```

**4. Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

### Option B — Depuis GitHub

**1. Cloner le dépôt**

```bash
git clone https://github.com/VenonX15/chip8-emulator.git
cd chip8-emulator
```

**2. (Recommandé) Créer un environnement virtuel**

```bash
python -m venv venv

# Sur Windows :
venv\Scripts\activate

# Sur macOS / Linux :
source venv/bin/activate
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

---

## 🚀 Lancer un jeu

Une fois les dépendances installées, lancez l'émulateur avec :

```bash
python main.py
```

L'émulateur s'ouvre sur un **menu principal**. Depuis ce menu, vous pouvez **importer n'importe quelle ROM** présente sur votre machine et lancer le jeu de votre choix directement dans l'interface.

> ⚠️ Les ROMs ne sont pas incluses dans ce projet. 

---

## 🛠️ Spécifications techniques

L'émulateur reproduit fidèlement le matériel CHIP-8 d'origine :

| Composant | Spécification |
|-----------|--------------|
| **Mémoire** | 4 Ko (4096 octets) de RAM |
| **Registres** | 16 registres 8 bits (`V0` à `VF`) |
| **Pile (Stack)** | Stockage des adresses de retour pour les sous-routines |
| **Timers** | Delay Timer et Sound Timer à 60 Hz |
| **Affichage** | 64×32 pixels |
| **Opcodes** | 35 instructions implémentées |

---

*Projet réalisé par Deodat A, Thomas B, Lucas H, Kylian M, Brianna M, Mouhamed S*
