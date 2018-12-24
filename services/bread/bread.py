#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Service (reloadable) methods for food-related operations."""

import os
import random
import re
import sys

_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(re.sub(r'/services/bread', '', _path))

SNACKS = [
    'amphora', 'apple', 'avocado', 'baby_bottle', 'bacon', 'baguette_bread',
    'banana', 'beer', 'beers', 'bento', 'birthday', 'bowl_with_spoon', 'bread',
    'broccoli', 'burrito', 'cake', 'candy', 'canned_food', 'carrot',
    'champagne', 'cheese_wedge', 'cherries', 'chestnut', 'chocolate_bar',
    'chopsticks', 'clinking_glasses', 'cocktail', 'coconut', 'coffee',
    'cookie', 'corn', 'croissant', 'cucumber', 'cup_with_straw', 'cut_of_meat',
    'curry', 'custard', 'dango', 'doughnut', 'dumpling', 'egg', 'eggplant',
    'fish_cake', 'fork_and_knife', 'fortune_cookie', 'fried_egg',
    'fried_shrimp', 'fries', 'glass_of_milk', 'grapes', 'green_apple',
    'green_salad', 'hamburger', 'hocho', 'honey_pot', 'hot_pepper', 'hotdog',
    'ice_cream', 'icecream', 'kiwifruit', 'knife_fork_plate', 'lemon',
    'lollipop', 'meat_on_bone', 'melon', 'mushroom', 'oden', 'pancakes',
    'peach', 'peanuts', 'pear', 'pie', 'pineapple', 'pizza', 'popcorn',
    'potato', 'poultry_leg', 'pretzel', 'ramen', 'rice', 'rice_ball',
    'rice_cracker', 'sake', 'sandwich', 'shallow_pan_of_food', 'shaved_ice',
    'spaghetti', 'spoon', 'stew', 'strawberry', 'stuffed_flatbread', 'sushi',
    'sweet_potato', 'taco', 'takeout_box', 'tangerine', 'tea', 'tomato',
    'tropical_drink', 'tumbler_glass', 'watermelon', 'wine_glass',
]  # yapf: disable


def snack_me():
    """Choose three snacks at random. If there are duplicates, replace the
    second snack instance with a star and the third instance with a trophy.

    Returns:
        A tuple of the three snacks.
    """
    s = [random.choice(SNACKS) for _ in range(3)]

    if s[0] == s[1]:
        if s[1] == s[2]:
            s[2] = 'trophy'
        s[1] = 'star'
    elif s[0] == s[2]:
        s[1], s[2] = 'star', s[1]
    elif s[1] == s[2]:
        s[0], s[1], s[2] = s[1], 'star', s[0]

    return tuple(s)
