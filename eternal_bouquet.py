"""Eternal Rose Code — scrolling code and an everlasting 3D rose bouquet.

Controls: F11 fullscreen, Space palette, R bloom again, Esc quit.
Requires pygame-ce and numpy (installed with the Windows Python on this PC).
"""

from __future__ import annotations

import math
import os
import random
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import numpy as np
import pygame


WIDTH, HEIGHT = 1280, 720
FPS = 30
BOUQUET_SCALE = 0.925

PETAL = 0
LEAF = 1
STEM = 2
BABY = 3
WRAP = 4
RIBBON = 5
BUNDLE = 6


PALETTES = (
    {
        "name": "BLUSH ROSE",
        "petal": ((238, 55, 98), (255, 133, 164), (255, 238, 240)),
        "leaf": ((63, 82, 74), (209, 219, 210)),
        "stem": ((44, 69, 56), (132, 154, 132)),
        "baby": ((255, 246, 236), (255, 221, 231)),
        "wrap": ((57, 15, 35), (168, 58, 94)),
        "ribbon": ((218, 198, 209), (255, 249, 242)),
        "bundle": ((72, 20, 42), (174, 72, 91)),
    },
    {
        "name": "CRIMSON GOLD",
        "petal": ((151, 13, 46), (235, 61, 84), (255, 220, 177)),
        "leaf": ((66, 72, 55), (200, 204, 176)),
        "stem": ((49, 67, 45), (133, 148, 106)),
        "baby": ((255, 244, 211), (255, 210, 153)),
        "wrap": ((44, 12, 22), (135, 37, 53)),
        "ribbon": ((222, 192, 151), (255, 246, 216)),
        "bundle": ((71, 16, 28), (183, 58, 64)),
    },
    {
        "name": "MOONLIT LILAC",
        "petal": ((112, 55, 162), (194, 138, 232), (248, 232, 255)),
        "leaf": ((59, 78, 82), (194, 211, 214)),
        "stem": ((43, 67, 68), (121, 151, 151)),
        "baby": ((244, 243, 255), (215, 220, 255)),
        "wrap": ((39, 18, 57), (118, 57, 136)),
        "ribbon": ((211, 201, 230), (253, 248, 255)),
        "bundle": ((55, 27, 75), (143, 70, 130)),
    },
)


CODE_TEXT = r'''
from math import sin, cos, pi, sqrt
from eternity import Light, Promise, Rose

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 720
ROSE_COUNT = "AS_MANY_AS_BEAUTY_NEEDS"
PETAL_LAYERS = 5
FOREVER = True

BLUSH_PINK = (255, 133, 164)
PEARL_WHITE = (255, 238, 240)
STEM_GREEN = (52, 102, 72)

class EternalRose:
    """A rose that blooms once and lives forever."""

    def __init__(self, center, radius, seed):
        self.center = center
        self.radius = radius
        self.seed = seed
        self.petals = []
        self.light = Light(color=PEARL_WHITE)

    def petal_surface(self, u, v, layer, angle):
        ring = self.radius * (0.04 + layer * 0.085)
        length = self.radius * (0.22 + layer * 0.035)
        r = ring + length * u
        twist = (0.45 - layer * 0.05) * (1.0 - u)
        theta = angle + twist
        width = self.radius * (0.10 + layer * 0.017)
        width *= sin(pi * u) ** 0.75

        x = r * cos(theta) - v * width * sin(theta)
        y = r * sin(theta) + v * width * cos(theta)
        z = self.radius * (0.48 - layer * 0.06)
        z *= 1.0 - u
        z += self.radius * 0.08 * (1.0 - v * v) * sin(pi * u)
        return x, y * 0.92, z

    def grow_layer(self, layer):
        petal_count = 3 + layer * 2
        for index in range(petal_count):
            angle = 2 * pi * index / petal_count
            angle += layer * 0.73
            for u in sample(0.0, 1.0, 5):
                for v in (-1.0, -0.33, 0.33, 1.0):
                    point = self.petal_surface(u, v, layer, angle)
                    self.petals.append(point)

    def bloom(self, now):
        for layer in range(PETAL_LAYERS):
            if now >= self.birth_time + layer * 0.22:
                self.grow_layer(layer)
        self.light.breathe(now, strength=0.18)

class EverlastingBouquet:
    def __init__(self):
        self.roses = []
        self.rotation = 0.0
        self.promise = Promise("NEVER WITHER")

    def arrange(self):
        centers = [
            (-145, 165, -10), (0, 205, 48),
            (145, 170, 0), (-215, 82, 32),
            (-100, 78, 88), (18, 92, 116),
            (132, 82, 82), (225, 90, 28),
            (-120, 274, -8), (0, 294, 35),
            (118, 276, -18),
        ]
        for index, center in enumerate(centers):
            radius = 68 + 14 * sin(index * 1.7) ** 2
            self.roses.append(EternalRose(center, radius, index))

    def rotate(self, seconds):
        self.rotation = seconds * 0.16
        return matrix_y(self.rotation)

    def render(self, screen, seconds):
        matrix = self.rotate(seconds)
        for rose in self.roses:
            rose.bloom(seconds)
            for point in rose.petals:
                world = matrix @ point
                screen.add_glow(world, BLUSH_PINK)

def bloom_forever():
    bouquet = EverlastingBouquet()
    bouquet.arrange()

    while FOREVER:
        seconds = clock.now()
        screen.clear(color=(4, 5, 12))
        code.scroll(speed=28)
        bouquet.render(screen, seconds)
        screen.write("∞  NEVER WITHER")
        screen.present()

if __name__ == "__main__":
    bloom_forever()

# The bouquet does not restart.
# It does not fade.
# It only keeps blooming, glowing and turning.
#
#                    for you, always.
'''.strip("\n").splitlines()


KEYWORD_RE = re.compile(
    r"(#.*$)|(\".*?\"|'.*?')|"
    r"\b(class|def|return|for|in|while|True|False|None|self|import|from|if|else|yield|with|as|range|enumerate|append)\b|"
    r"\b(\d+(?:\.\d+)?)\b|\b([A-Z][A-Z0-9_]{2,})\b"
)


def mix_color(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> np.ndarray:
    t = max(0.0, min(1.0, t))
    return np.array([a[i] + (b[i] - a[i]) * t for i in range(3)], dtype=np.float32)


def smooth(values: np.ndarray) -> np.ndarray:
    values = np.clip(values, 0.0, 1.0)
    return values * values * (3.0 - 2.0 * values)


class ParticleBuilder:
    def __init__(self, seed: int = 20260811) -> None:
        self.rng = random.Random(seed)
        self.final: list[tuple[float, float, float]] = []
        self.start: list[tuple[float, float, float]] = []
        self.role: list[int] = []
        self.tone: list[float] = []
        self.birth: list[float] = []
        self.power: list[float] = []
        self.size: list[float] = []
        self.phase: list[float] = []
        self.anchor: list[tuple[float, float, float]] = []

    def add(
        self,
        final: tuple[float, float, float],
        start: tuple[float, float, float],
        role: int,
        tone: float,
        birth: float,
        power: float = 1.0,
        size: float = 1.0,
        anchor: tuple[float, float, float] | None = None,
    ) -> None:
        self.final.append(final)
        self.start.append(start)
        self.role.append(role)
        self.tone.append(max(0.0, min(1.0, tone)))
        self.birth.append(birth)
        self.power.append(power)
        self.size.append(size)
        self.phase.append(self.rng.random() * math.tau)
        self.anchor.append(anchor if anchor is not None else (0.0, 0.0, 0.0))

    def add_rose(
        self,
        center: tuple[float, float, float],
        radius: float,
        bloom_index: int,
    ) -> None:
        cx, cy, cz = center
        for layer in range(5):
            petal_count = 3 + layer * 2
            for petal in range(petal_count):
                angle = math.tau * petal / petal_count + layer * 0.73
                angle += self.rng.uniform(-0.035, 0.035)
                for iu in range(4):
                    u = (iu + 0.35 + self.rng.random() * 0.3) / 4.0
                    for v0 in (-1.0, -0.34, 0.34, 1.0):
                        v = v0 + self.rng.uniform(-0.045, 0.045)
                        ring = radius * (0.04 + layer * 0.085)
                        length = radius * (0.22 + layer * 0.035)
                        radial = ring + length * u
                        twist = (0.48 - layer * 0.052) * (1.0 - u)
                        theta = angle + twist
                        width = radius * (0.10 + layer * 0.017)
                        width *= max(0.05, math.sin(math.pi * u)) ** 0.75
                        across = v * width
                        local_x = radial * math.cos(theta) - across * math.sin(theta)
                        local_y = (radial * math.sin(theta) + across * math.cos(theta)) * 0.92
                        local_z = radius * (0.49 - layer * 0.06) * (1.0 - u)
                        local_z += radius * (0.078 + layer * 0.006) * (1.0 - v * v) * math.sin(math.pi * u)
                        local_z -= layer * radius * 0.024
                        local_x += self.rng.uniform(-1.2, 1.2)
                        local_y += self.rng.uniform(-1.2, 1.2)
                        local_z += self.rng.uniform(-0.8, 0.8)

                        final = (cx + local_x, cy + local_y, cz + local_z)
                        unfurl = 0.055 + layer * 0.018
                        start = (cx + local_x * unfurl, cy + local_y * unfurl, cz + local_z * 0.08)
                        is_edge = abs(v0) > 0.8
                        edge_light = 0.43 if is_edge else 0.0
                        tone = 0.05 + layer * 0.075 + u * 0.24 + edge_light
                        birth = 1.15 + bloom_index * 0.34 + layer * 0.23 + u * 0.12
                        birth += self.rng.uniform(0.0, 0.18)
                        power = (1.08 if is_edge else 0.23) + self.rng.uniform(0.0, 0.11)
                        size = (2.6 if is_edge else 0.72) + self.rng.random() * 0.48
                        self.add(final, start, PETAL, tone, birth, power, size, (cx, cy, cz))

        # A luminous spiral heart makes each bloom read unmistakably as a rose.
        for spiral_index in range(116):
            t = spiral_index / 115.0
            angle = t * math.tau * 2.35 + 0.55
            radial = radius * (0.025 + 0.285 * t)
            local_x = math.cos(angle) * radial
            local_y = math.sin(angle) * radial * 0.88
            local_z = radius * (0.46 - 0.22 * t) + math.sin(t * math.pi * 5.0) * 1.5
            final = (cx + local_x, cy + local_y, cz + local_z)
            start = (cx + local_x * 0.04, cy + local_y * 0.04, cz)
            birth = 0.95 + bloom_index * 0.34 + t * 0.44
            self.add(final, start, PETAL, 0.06 + t * 0.26, birth, 1.14, 2.7, (cx, cy, cz))

        for _ in range(96):
            angle = self.rng.random() * math.tau
            radial = radius * self.rng.uniform(0.62, 1.05)
            local_x = math.cos(angle) * radial
            local_y = math.sin(angle) * radial * 0.86
            local_z = self.rng.uniform(-radius * 0.12, radius * 0.34)
            final = (cx + local_x, cy + local_y, cz + local_z)
            start = (cx + local_x * 0.12, cy + local_y * 0.12, cz)
            birth = 2.0 + bloom_index * 0.34 + self.rng.uniform(0.0, 1.3)
            self.add(final, start, PETAL, self.rng.uniform(0.68, 1.0), birth, 0.145, 0.55, (cx, cy, cz))

    def add_stem(self, center: tuple[float, float, float], index: int) -> None:
        cx, cy, cz = center
        base_angle = index * 2.399963229728653
        base = (34.0 * math.cos(base_angle), -210.0, 26.0 * math.sin(base_angle))
        control = (cx * 0.32, -70.0 + (index % 3) * 12, cz * 0.25)
        top = (cx, cy - 24.0, cz)
        for step in range(58):
            t = step / 57.0
            inv = 1.0 - t
            point = (
                inv * inv * base[0] + 2 * inv * t * control[0] + t * t * top[0],
                inv * inv * base[1] + 2 * inv * t * control[1] + t * t * top[1],
                inv * inv * base[2] + 2 * inv * t * control[2] + t * t * top[2],
            )
            start = (base[0], base[1], base[2])
            role = BUNDLE if t < 0.37 else STEM
            power = 0.74 if role == BUNDLE else 0.58
            size = 1.15 if role == BUNDLE else 0.95
            self.add(point, start, role, self.rng.random(), 0.18 + t * 1.35, power, size)

    def add_leaves(self, count: int = 18) -> None:
        for leaf_index in range(count):
            side = -1 if leaf_index % 2 == 0 else 1
            center_x = side * self.rng.uniform(78.0, 230.0)
            center_y = self.rng.uniform(-65.0, 130.0)
            center_z = self.rng.uniform(-75.0, 85.0)
            direction = (0.20 if side > 0 else math.pi - 0.20) + self.rng.uniform(-0.34, 0.34)
            length = self.rng.uniform(46.0, 76.0)
            width = self.rng.uniform(14.0, 24.0)
            for along_index in range(8):
                along = -1.0 + 2.0 * along_index / 7.0
                half_width = math.sqrt(max(0.0, 1.0 - along * along))
                for across_index in range(4):
                    across = -half_width + 2.0 * half_width * across_index / 3.0
                    across += self.rng.uniform(-0.05, 0.05)
                    lx = along * length * 0.5
                    ly = across * width
                    x = center_x + lx * math.cos(direction) - ly * math.sin(direction)
                    y = center_y + lx * math.sin(direction) + ly * math.cos(direction)
                    z = center_z + across * 8.0
                    start = (0.0, -235.0, 0.0)
                    tone = 0.20 + (along + 1.0) * 0.27 + self.rng.uniform(0.0, 0.2)
                    self.add((x, y, z), start, LEAF, tone, 0.9 + self.rng.random() * 2.4, 0.82, 1.05)

    def add_baby_breath(self, count: int = 42) -> None:
        for cluster in range(count):
            angle = self.rng.random() * math.tau
            ring_x = self.rng.uniform(246.0, 312.0)
            ring_y = self.rng.uniform(164.0, 226.0)
            cx = math.cos(angle) * ring_x
            cy = 125.0 + math.sin(angle) * ring_y
            if cy < -20.0:
                cy += 95.0
            cz = self.rng.uniform(-110.0, 110.0)
            for point in range(15):
                a = self.rng.random() * math.tau
                r = self.rng.uniform(3.0, 21.0)
                x = cx + math.cos(a) * r
                y = cy + math.sin(a) * r
                z = cz + self.rng.uniform(-13.0, 13.0)
                start = (cx * 0.2, -150.0, cz * 0.1)
                power = 0.42 if point % 5 else 1.15
                size = 0.8 if point % 5 else 2.8
                self.add((x, y, z), start, BABY, self.rng.random(), 2.0 + self.rng.random() * 4.2, power, size)

    def add_foliage_cloud(self, count: int = 3000) -> None:
        """Dense sage-and-pearl skirt beneath the rose dome."""
        for index in range(count):
            angle = self.rng.random() * math.tau
            radial = 282.0 * math.sqrt(self.rng.random())
            x = math.cos(angle) * radial
            z = math.sin(angle) * radial
            y = 27.0 - max(0.0, radial - 105.0) * 0.10 + self.rng.gauss(0.0, 29.0)
            y = max(-86.0, min(96.0, y))
            start = (x * 0.08, -103.0, z * 0.08)
            if index % 4 == 0:
                role = BABY
                power = self.rng.uniform(0.72, 1.08)
                tone = self.rng.uniform(0.48, 1.0)
            else:
                role = LEAF
                power = self.rng.uniform(0.60, 0.94)
                tone = self.rng.uniform(0.68, 1.0)
            self.add(
                (x, y, z),
                start,
                role,
                tone,
                1.5 + self.rng.random() * 4.4,
                power,
                self.rng.uniform(0.5, 1.05),
            )

    def add_wrapper(self) -> None:
        # A short, wine-red stem bundle below the knot.
        for filament in range(76):
            top_x = self.rng.uniform(-38.0, 38.0)
            top_z = self.rng.uniform(-30.0, 30.0)
            bottom_x = self.rng.uniform(-31.0, 31.0)
            bottom_z = self.rng.uniform(-24.0, 24.0)
            for step in range(25):
                t = step / 24.0
                x = top_x * (1.0 - t) + bottom_x * t
                x += math.sin(t * math.pi * 2.0 + filament * 0.37) * 2.2
                y = -104.0 - 111.0 * t
                z = top_z * (1.0 - t) + bottom_z * t
                self.add(
                    (x, y, z),
                    (top_x, -104.0, top_z),
                    BUNDLE,
                    self.rng.random(),
                    0.45 + t * 1.15 + self.rng.random() * 0.25,
                    0.48 + self.rng.random() * 0.28,
                    0.72 + self.rng.random() * 0.5,
                )

        tie_y = -103.0
        # Fine pearl-sage sprays bridge the flower skirt into the narrow tie.
        golden_angle = math.pi * (3.0 - math.sqrt(5.0))
        for spray in range(38):
            phi = spray * golden_angle + 0.31
            radius = self.rng.uniform(148.0, 246.0)
            end = (
                math.cos(phi) * radius,
                self.rng.uniform(-12.0, 78.0),
                math.sin(phi) * radius * 0.72,
            )
            start = (math.cos(phi) * 18.0, tie_y, math.sin(phi) * 15.0)
            control = (
                math.cos(phi) * radius * 0.32,
                -62.0 + self.rng.uniform(-10.0, 10.0),
                math.sin(phi) * radius * 0.22,
            )
            for step in range(24):
                t = step / 23.0
                inv = 1.0 - t
                point = (
                    inv * inv * start[0] + 2.0 * inv * t * control[0] + t * t * end[0],
                    inv * inv * start[1] + 2.0 * inv * t * control[1] + t * t * end[1],
                    inv * inv * start[2] + 2.0 * inv * t * control[2] + t * t * end[2],
                )
                is_pearl = spray % 5 == 0 or step % 9 == 0
                role = BABY if is_pearl else LEAF
                power = self.rng.uniform(0.58, 0.90) if is_pearl else self.rng.uniform(0.38, 0.62)
                self.add(
                    point,
                    start,
                    role,
                    self.rng.uniform(0.68, 1.0),
                    0.55 + t * 1.75 + self.rng.random() * 0.24,
                    power,
                    1.35 if is_pearl else 0.72,
                )

        # A real 3D burgundy tie cylinder, replacing the old flat paper triangles.
        for index in range(420):
            theta = self.rng.random() * math.tau
            height_ratio = self.rng.uniform(-1.0, 1.0)
            radius = 28.0 + (1.0 - height_ratio) * 2.0 + self.rng.uniform(-2.2, 2.2)
            x = math.cos(theta) * radius
            y = tie_y + height_ratio * 20.0
            z = math.sin(theta) * radius
            self.add(
                (x, y, z),
                (0.0, tie_y, 0.0),
                WRAP,
                self.rng.random(),
                0.8 + self.rng.random() * 1.2,
                self.rng.uniform(0.28, 0.58),
                self.rng.uniform(0.58, 1.0),
            )
        for index in range(96):
            t = index / 95.0
            theta = t * math.pi * 5.0
            radius = 32.0
            self.add(
                (math.cos(theta) * radius, tie_y - 20.0 + 40.0 * t, math.sin(theta) * radius),
                (0.0, tie_y, 0.0),
                WRAP,
                t,
                1.0 + t * 0.75,
                0.88,
                1.2,
            )

        # Six organza lobes around the stem axis stay full from every angle.
        for lobe in range(6):
            phi = lobe * math.tau / 6.0 + 0.15
            ex, ez = math.cos(phi), math.sin(phi)
            sx, sz = -ez, ex
            amplitude = 90.0 + (lobe % 3) * 12.0
            for index in range(220):
                s = self.rng.random()
                lift = math.sin(math.pi * s)
                edge = index % 5 == 0
                across = self.rng.choice((-1.0, 1.0)) if edge else self.rng.uniform(-1.0, 1.0)
                width = 7.0 + 14.0 * lift
                center_r = amplitude * lift
                center_y = tie_y + 9.0 * lift + math.sin(math.tau * s) * (25.0 + lobe % 2 * 6.0)
                side_wave = math.sin(math.pi * s + lobe) * 11.0 * lift
                x = ex * center_r + sx * (side_wave + across * width)
                z = ez * center_r + sz * (side_wave + across * width)
                y = center_y + across * width * 0.42 * math.cos(math.pi * s)
                power = self.rng.uniform(0.58, 0.86) if edge else self.rng.uniform(0.42, 0.68)
                self.add(
                    (x, y, z),
                    (0.0, tie_y, 0.0),
                    RIBBON,
                    self.rng.uniform(0.48, 1.0),
                    1.25 + s * 0.9 + lobe * 0.035,
                    power,
                    1.18 if edge else 0.68,
                )

        # A translucent organza mist breaks the loops into a feathery couture bow.
        for index in range(720):
            theta = self.rng.random() * math.tau
            radial = 118.0 * math.sqrt(self.rng.random())
            x = math.cos(theta) * radial
            z = math.sin(theta) * radial * 0.72
            y = tie_y + self.rng.gauss(0.0, 29.0) + math.cos(theta * 2.0) * 5.0
            self.add(
                (x, y, z),
                (0.0, tie_y, 0.0),
                RIBBON,
                self.rng.uniform(0.58, 1.0),
                1.35 + self.rng.random() * 1.2,
                self.rng.uniform(0.24, 0.56),
                self.rng.uniform(0.55, 1.25),
            )

        # Pearl knot at the center of the bow.
        for index in range(260):
            azimuth = self.rng.random() * math.tau
            vertical = self.rng.uniform(-1.0, 1.0)
            radial = self.rng.random() ** (1.0 / 3.0)
            horizontal = math.sqrt(max(0.0, 1.0 - vertical * vertical))
            x = math.cos(azimuth) * horizontal * radial * 29.0
            y = tie_y + vertical * radial * 22.0
            z = math.sin(azimuth) * horizontal * radial * 25.0
            self.add(
                (x, y, z),
                (0.0, tie_y, 0.0),
                RIBBON,
                self.rng.uniform(0.58, 1.0),
                0.75 + self.rng.random() * 1.3,
                self.rng.uniform(0.18, 0.54),
                self.rng.uniform(0.8, 2.0),
            )

        # Four translucent tails around the axis, with bright woven edges.
        for tail in range(4):
            phi = tail * math.tau / 4.0 + 0.34
            ex, ez = math.cos(phi), math.sin(phi)
            sx, sz = -ez, ex
            for index in range(160):
                t = self.rng.random()
                edge = index % 5 == 0
                across = self.rng.choice((-1.0, 1.0)) if edge else self.rng.uniform(-1.0, 1.0)
                width = 21.0 * (1.0 - t) + 7.0
                center_r = 13.0 + 36.0 * t + math.sin(t * math.tau * 1.5) * 5.0
                x = ex * center_r + sx * across * width
                y = tie_y - 12.0 - 94.0 * t
                z = ez * center_r + sz * across * width
                z += math.sin(t * math.pi) * 8.0 + self.rng.uniform(-3.0, 3.0)
                power = self.rng.uniform(0.80, 1.10) if edge else self.rng.uniform(0.36, 0.60)
                self.add(
                    (x, y, z),
                    (0.0, tie_y, 0.0),
                    RIBBON,
                    0.42 + t * 0.58,
                    1.0 + t * 1.15 + self.rng.random() * 0.35,
                    power,
                    1.35 if edge else 0.72,
                )

        # Loose luminous fibers around the knot, like the reference's feathery bow.
        for curl in range(6):
            phi = curl * math.tau / 6.0 + 0.2
            ex, ez = math.cos(phi), math.sin(phi)
            sx, sz = -ez, ex
            for step in range(60):
                t = step / 59.0
                angle = t * math.pi * (1.35 + curl * 0.16) + curl * 0.7
                radius = 25.0 + t * (58.0 + curl * 6.0)
                radial = math.cos(angle) * radius + 12.0
                sideways = math.sin(angle) * radius * 0.24
                x = ex * radial + sx * sideways
                y = tie_y + math.sin(angle) * radius * 0.50 - t * 22.0
                z = ez * radial + sz * sideways
                self.add(
                    (x, y, z),
                    (0.0, tie_y, 0.0),
                    RIBBON,
                    0.72 + 0.28 * t,
                    1.05 + t * 0.7,
                    0.92,
                    1.35,
                )

    def arrays(self) -> dict[str, np.ndarray]:
        return {
            "final": np.asarray(self.final, dtype=np.float32),
            "start": np.asarray(self.start, dtype=np.float32),
            "role": np.asarray(self.role, dtype=np.int8),
            "tone": np.asarray(self.tone, dtype=np.float32),
            "birth": np.asarray(self.birth, dtype=np.float32),
            "power": np.asarray(self.power, dtype=np.float32),
            "size": np.asarray(self.size, dtype=np.float32),
            "phase": np.asarray(self.phase, dtype=np.float32),
            "anchor": np.asarray(self.anchor, dtype=np.float32),
        }


@dataclass(slots=True)
class ClickSpark:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    color: tuple[int, int, int]


class EternalRoseCode:
    def __init__(self, preview_path: str | None = None) -> None:
        pygame.init()
        pygame.display.set_caption("Eternal Rose Code · 永不凋零")
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        try:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags, vsync=1)
        except TypeError:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        self.clock = pygame.time.Clock()
        self.preview_path = preview_path
        self.preview_saved = False
        self.running = True
        self.fullscreen = False
        self.palette_index = 0
        self.started = time.perf_counter()
        self.bloom_started = self.started
        self.rng = random.Random(314159)
        self.mouse_parallax = 0.0
        self.target_parallax = 0.0
        self.click_sparks: list[ClickSpark] = []

        builder = ParticleBuilder()
        self.rose_centers = self._make_rose_centers()
        for index, (x, y, z, radius) in enumerate(self.rose_centers):
            builder.add_stem((x, y, z), index)
            builder.add_rose((x, y, z), radius, index)
        builder.add_leaves(30)
        builder.add_foliage_cloud()
        builder.add_baby_breath(64)
        builder.add_wrapper()
        self.data = builder.arrays()
        self.count = len(self.data["final"])
        self.preview_ready_at = max(18.0, float(self.data["birth"].max()) + 1.15)
        self.colors = np.empty((self.count, 3), dtype=np.float32)
        (
            self.outline_points,
            self.outline_anchors,
            self.outline_slices,
            self.outline_tones,
            self.outline_births,
        ) = self._build_rose_outlines()
        self._set_palette(0)

        self.glow_offsets = (
            (0, 0, 1.00),
        )
        self.star_field = [
            (self.rng.random(), self.rng.random(), self.rng.uniform(0.4, 1.5), self.rng.random() * math.tau)
            for _ in range(95)
        ]
        self.scene_buffer: np.ndarray | None = None
        self.scene_buffer_size = (0, 0)
        self.glow_near: pygame.Surface | None = None
        self.glow_wide: pygame.Surface | None = None
        self.ambient_glow: pygame.Surface | None = None
        self._make_fonts(HEIGHT)

    def _make_fonts(self, height: int) -> None:
        scale = max(0.82, min(1.35, height / 720.0))
        self.code_font = pygame.font.SysFont("Consolas", max(12, round(14 * scale)))
        self.code_bold = pygame.font.SysFont("Consolas", max(12, round(14 * scale)), bold=True)
        self.small_font = pygame.font.SysFont("Microsoft YaHei UI", max(11, round(12 * scale)))
        self.label_font = pygame.font.SysFont("Segoe UI", max(13, round(15 * scale)), bold=True)
        self.hero_font = pygame.font.SysFont("segoeuisemilight", max(22, round(29 * scale)))

    @staticmethod
    def _make_rose_centers() -> tuple[tuple[float, float, float, float], ...]:
        """Build a dense, rotation-safe spherical flower crown."""
        rng = random.Random(20260812)
        centers: list[tuple[float, float, float, float]] = []
        count = 26
        golden_angle = math.pi * (3.0 - math.sqrt(5.0))
        for index in range(count):
            progress = (index + 0.45) / count
            y = 304.0 - progress * 302.0 + rng.uniform(-9.0, 9.0)
            normalized_y = (y - 153.0) / 166.0
            ring = 246.0 * math.sqrt(max(0.13, 1.0 - normalized_y * normalized_y))
            angle = index * golden_angle + 0.38
            x = math.cos(angle) * ring
            z = math.sin(angle) * ring
            radius = rng.uniform(74.0, 89.0) + (1.0 - abs(normalized_y)) * 5.0
            centers.append((x, y, z, radius))

        for y, radius, z in (
            (292.0, 91.0, 0.0),
            (230.0, 102.0, 12.0),
            (166.0, 111.0, -8.0),
            (98.0, 108.0, 10.0),
            (30.0, 99.0, -6.0),
        ):
            centers.append((0.0, y, z, radius))
        return tuple(centers)

    def _build_rose_outlines(
        self,
    ) -> tuple[np.ndarray, np.ndarray, list[tuple[int, int]], np.ndarray, np.ndarray]:
        all_points: list[tuple[float, float, float]] = []
        all_anchors: list[tuple[float, float, float]] = []
        slices: list[tuple[int, int]] = []
        tones: list[float] = []
        births: list[float] = []
        for bloom_index, (cx, cy, cz, radius) in enumerate(self.rose_centers):
            if bloom_index < 26 and bloom_index % 2 == 1:
                continue
            for layer in (0, 2, 4):
                petal_count = 3 + layer * 2
                for petal in range(petal_count):
                    angle = math.tau * petal / petal_count + layer * 0.73
                    contour: list[tuple[float, float, float]] = []
                    for v, order in ((-1.0, range(10)), (1.0, range(9, -1, -1))):
                        for step in order:
                            u = 0.055 + step / 9.0 * 0.92
                            ring = radius * (0.04 + layer * 0.085)
                            length = radius * (0.22 + layer * 0.035)
                            radial = ring + length * u
                            twist = (0.48 - layer * 0.052) * (1.0 - u)
                            theta = angle + twist
                            width = radius * (0.10 + layer * 0.017)
                            width *= max(0.05, math.sin(math.pi * u)) ** 0.75
                            across = v * width
                            x = radial * math.cos(theta) - across * math.sin(theta)
                            y = (radial * math.sin(theta) + across * math.cos(theta)) * 0.92
                            z = radius * (0.49 - layer * 0.06) * (1.0 - u)
                            z += radius * (0.078 + layer * 0.006) * (1.0 - v * v) * math.sin(math.pi * u)
                            z -= layer * radius * 0.024
                            contour.append((cx + x, cy + y, cz + z))
                    start = len(all_points)
                    all_points.extend(contour)
                    all_anchors.extend([(cx, cy, cz)] * len(contour))
                    slices.append((start, len(all_points)))
                    tones.append(0.12 + layer * 0.12)
                    births.append(1.12 + bloom_index * 0.34 + layer * 0.23)
        return (
            np.asarray(all_points, dtype=np.float32),
            np.asarray(all_anchors, dtype=np.float32),
            slices,
            np.asarray(tones, dtype=np.float32),
            np.asarray(births, dtype=np.float32),
        )

    def _rotation(self, elapsed: float) -> float:
        # A calm full turn: long enough to admire, short enough to see it complete.
        return (elapsed * math.tau / 36.0) % math.tau

    @staticmethod
    def _billboard(
        points: np.ndarray,
        anchors: np.ndarray,
        mask: np.ndarray,
        angle: float,
    ) -> None:
        """Keep rose faces toward the viewer while their centers orbit in 3D."""
        local_x = points[mask, 0] - anchors[mask, 0]
        local_z = points[mask, 2] - anchors[mask, 2]
        cosine, sine = math.cos(angle), math.sin(angle)
        points[mask, 0] = anchors[mask, 0] + local_x * cosine - local_z * sine
        points[mask, 2] = anchors[mask, 2] + local_x * sine + local_z * cosine

    def _set_palette(self, index: int) -> None:
        self.palette_index = index % len(PALETTES)
        palette = PALETTES[self.palette_index]
        for role in (PETAL, LEAF, STEM, BABY, WRAP, RIBBON, BUNDLE):
            mask = self.data["role"] == role
            tones = self.data["tone"][mask]
            if role == PETAL:
                dark, middle, light = palette["petal"]
                role_colors = np.empty((len(tones), 3), dtype=np.float32)
                lower = tones < 0.52
                low_t = np.clip(tones[lower] / 0.52, 0, 1)
                high_t = np.clip((tones[~lower] - 0.52) / 0.48, 0, 1)
                role_colors[lower] = np.array(dark) + (np.array(middle) - np.array(dark)) * low_t[:, None]
                role_colors[~lower] = np.array(middle) + (np.array(light) - np.array(middle)) * high_t[:, None]
            else:
                key = {
                    LEAF: "leaf",
                    STEM: "stem",
                    BABY: "baby",
                    WRAP: "wrap",
                    RIBBON: "ribbon",
                    BUNDLE: "bundle",
                }[role]
                first, second = palette[key]
                role_colors = np.array(first) + (np.array(second) - np.array(first)) * tones[:, None]
            self.colors[mask] = role_colors

    def _left_width(self, width: int) -> int:
        return max(400, min(570, int(width * 0.42)))

    def _background(self, width: int, height: int, left: int, elapsed: float) -> None:
        self.screen.fill((4, 5, 11))
        for index in range(36):
            t = index / 35.0
            color = (
                int(5 + 7 * t),
                int(6 + 3 * t),
                int(14 + 8 * (1.0 - abs(t - 0.5))),
            )
            y0 = int(height * index / 36)
            y1 = int(height * (index + 1) / 36) + 1
            pygame.draw.rect(self.screen, color, (left, y0, width - left, y1 - y0))
        pygame.draw.rect(self.screen, (5, 6, 12), (0, 0, left, height))

        scene_w = width - left
        for nx, ny, size, phase in self.star_field:
            pulse = 0.45 + 0.55 * math.sin(elapsed * 0.75 + phase) ** 2
            color = int(72 + pulse * 100)
            x = left + int(nx * scene_w)
            y = int(ny * height)
            radius = 1 if size * pulse < 1.25 else 2
            pygame.draw.circle(self.screen, (color, color - 5, min(255, color + 18)), (x, y), radius)
        if self.ambient_glow is not None:
            self.screen.blit(self.ambient_glow, (left, 0), special_flags=pygame.BLEND_RGB_ADD)

    def _draw_code_segment(self, line: str, x: int, y: int) -> None:
        position = 0
        cursor_x = x
        for match in KEYWORD_RE.finditer(line):
            if match.start() > position:
                text = line[position : match.start()]
                image = self.code_font.render(text, True, (184, 190, 207))
                self.screen.blit(image, (cursor_x, y))
                cursor_x += image.get_width()
            token = match.group(0)
            if match.group(1):
                color = (88, 125, 104)
                font = self.code_font
            elif match.group(2):
                color = (229, 190, 113)
                font = self.code_font
            elif match.group(3):
                color = (232, 104, 166)
                font = self.code_bold
            elif match.group(4):
                color = (87, 196, 209)
                font = self.code_font
            else:
                color = (122, 185, 241)
                font = self.code_font
            image = font.render(token, True, color)
            self.screen.blit(image, (cursor_x, y))
            cursor_x += image.get_width()
            position = match.end()
        if position < len(line):
            image = self.code_font.render(line[position:], True, (184, 190, 207))
            self.screen.blit(image, (cursor_x, y))

    def _draw_code_panel(self, width: int, height: int, left: int, elapsed: float) -> None:
        header_h = 58
        line_h = self.code_font.get_linesize() + 1
        total_h = len(CODE_TEXT) * line_h
        offset = (elapsed * 30.0) % total_h

        pygame.draw.rect(self.screen, (10, 11, 20), (0, 0, left, header_h))
        pygame.draw.line(self.screen, (35, 36, 52), (0, header_h), (left, header_h))
        for index, color in enumerate(((255, 95, 106), (255, 193, 75), (67, 202, 115))):
            pygame.draw.circle(self.screen, color, (21 + index * 21, 20), 5)
        title = self.label_font.render("eternal_rose.py", True, (214, 216, 228))
        self.screen.blit(title, (82, 10))
        run = self.small_font.render("●  RUNNING  ∞", True, (104, 216, 159))
        self.screen.blit(run, (left - run.get_width() - 18, 13))
        path = self.small_font.render("WINDOWS PORTABLE  /  NO PYTHON REQUIRED", True, (84, 87, 108))
        self.screen.blit(path, (82, 34))

        old_clip = self.screen.get_clip()
        self.screen.set_clip(pygame.Rect(0, header_h + 1, left, height - header_h - 1))
        visible_focus = header_h + int(height * 0.49)
        pygame.draw.rect(self.screen, (12, 15, 27), (0, visible_focus, left, line_h))
        pygame.draw.rect(self.screen, (169, 71, 121), (0, visible_focus, 2, line_h))

        for repeat in range(2):
            base_y = header_h + 8 - offset + repeat * total_h
            for index, line in enumerate(CODE_TEXT):
                y = int(base_y + index * line_h)
                if y < header_h - line_h or y > height:
                    continue
                number = self.code_font.render(f"{index + 1:>3}", True, (58, 61, 78))
                self.screen.blit(number, (9, y))
                leading = len(line) - len(line.lstrip(" "))
                for guide in range(1, leading // 4 + 1):
                    guide_x = 48 + guide * self.code_font.size("    ")[0]
                    pygame.draw.line(self.screen, (28, 31, 45), (guide_x, y), (guide_x, y + line_h))
                self._draw_code_segment(line, 48, y)

        if int(elapsed * 2) % 2 == 0:
            pygame.draw.rect(self.screen, (235, 137, 183), (left - 13, visible_focus + 3, 2, line_h - 6))
        self.screen.set_clip(old_clip)
        pygame.draw.line(self.screen, (104, 93, 122), (left, 0), (left, height), 1)
        pygame.draw.line(self.screen, (34, 32, 49), (left + 3, 0), (left + 3, height), 1)

    def _project_world(
        self,
        points: np.ndarray,
        scene_w: int,
        height: int,
        angle: float,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        cosine, sine = math.cos(angle), math.sin(angle)
        x = points[:, 0] * cosine + points[:, 2] * sine
        z = -points[:, 0] * sine + points[:, 2] * cosine
        # The tilt is periodic with the turn, so there is no jump at 360 degrees.
        tilt = 0.028 * math.sin(angle)
        ct, st = math.cos(tilt), math.sin(tilt)
        y = points[:, 1] * ct - z * st
        z2 = points[:, 1] * st + z * ct
        perspective = 1140.0 / (1140.0 - z2)
        scale = min(scene_w / 760.0, height / 720.0) * 1.06
        sx = scene_w * 0.52 + x * perspective * scale + self.mouse_parallax * 8.0
        sy = height * 0.59 - y * perspective * scale
        return sx, sy, perspective, z2

    def _draw_space_box(self, left: int, scene_w: int, height: int, angle: float) -> None:
        corners = np.array(
            [
                (-365, -285, 250), (365, -285, 250), (-365, 400, 250), (365, 400, 250),
                (-365, -285, -250), (365, -285, -250), (-365, 400, -250), (365, 400, -250),
            ],
            dtype=np.float32,
        )
        sx, sy, _, depth = self._project_world(corners, scene_w, height, angle)
        edges = ((0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), (0, 4), (1, 5), (2, 6), (3, 7))
        for first, second in edges:
            near = (depth[first] + depth[second]) * 0.5
            light = int(90 + max(-270, min(270, near)) / 270 * 32)
            color = (light, max(0, light - 3), min(255, light + 16))
            start = (left + int(sx[first]), int(sy[first]))
            end = (left + int(sx[second]), int(sy[second]))
            halo = tuple(max(0, channel // 4) for channel in color)
            pygame.draw.line(self.screen, halo, start, end, 3)
            pygame.draw.aaline(
                self.screen,
                color,
                start,
                end,
            )

    def _ensure_buffer(self, scene_w: int, height: int) -> None:
        if self.scene_buffer_size != (scene_w, height):
            self.scene_buffer = np.zeros((scene_w, height, 3), dtype=np.uint16)
            self.scene_buffer_size = (scene_w, height)
            self.glow_near = pygame.Surface((scene_w, height))
            self.glow_wide = pygame.Surface((scene_w, height))
            self.glow_near.set_alpha(148)
            self.glow_wide.set_alpha(96)
            self.ambient_glow = pygame.Surface((scene_w, height))
            self.ambient_glow.fill((0, 0, 0))
            center = (int(scene_w * 0.52), int(height * 0.37))
            outer = int(min(scene_w, height) * 0.45)
            for radius in range(outer, 12, -14):
                closeness = 1.0 - radius / outer
                color = (
                    int(1 + closeness * 11),
                    int(closeness * 2),
                    int(2 + closeness * 7),
                )
                pygame.draw.circle(self.ambient_glow, color, center, radius)

    def _draw_particles(self, left: int, scene_w: int, height: int, bloom_t: float, elapsed: float) -> float:
        self._ensure_buffer(scene_w, height)
        assert self.scene_buffer is not None
        self.scene_buffer.fill(0)

        growth = smooth((bloom_t - self.data["birth"]) / 1.05)
        points = self.data["start"] + (self.data["final"] - self.data["start"]) * growth[:, None]
        points[:, 1] += np.sin(elapsed * 0.72 + self.data["phase"]) * (0.75 * growth)
        angle = self._rotation(elapsed) + self.mouse_parallax * 0.055
        petal_mask = self.data["role"] == PETAL
        self._billboard(points, self.data["anchor"], petal_mask, angle)
        points *= BOUQUET_SCALE
        sx, sy, perspective, depth = self._project_world(points, scene_w, height, angle)

        active = growth > 0.002
        xs = sx[active].astype(np.int32)
        ys = sy[active].astype(np.int32)
        depth_light = np.clip(0.68 + (depth[active] + 260.0) / 840.0, 0.58, 1.18)
        shimmer = 0.90 + 0.10 * np.sin(elapsed * 1.25 + self.data["phase"][active])
        intensity = self.data["power"][active] * growth[active] * depth_light * shimmer
        values = self.colors[active] * intensity[:, None]

        for dx, dy, weight in self.glow_offsets:
            xx = xs + dx
            yy = ys + dy
            valid = (xx >= 0) & (xx < scene_w) & (yy >= 0) & (yy < height)
            if not np.any(valid):
                continue
            coords = (xx[valid], yy[valid])
            weighted = np.clip(values[valid] * weight, 0, 255).astype(np.uint16)
            for channel in range(3):
                np.add.at(self.scene_buffer[:, :, channel], coords, weighted[:, channel])

        pixels = np.minimum(self.scene_buffer.astype(np.float32) * 0.72, 255).astype(np.uint8)
        particle_surface = pygame.surfarray.make_surface(pixels)
        assert self.glow_near is not None and self.glow_wide is not None
        # Two fast soft-light layers keep the bouquet luminous without slowing its turn.
        pygame.transform.box_blur(particle_surface, 2, dest_surface=self.glow_near)
        pygame.transform.box_blur(particle_surface, 7, dest_surface=self.glow_wide)
        self.screen.blit(self.glow_wide, (left, 0), special_flags=pygame.BLEND_RGB_ADD)
        self.screen.blit(self.glow_near, (left, 0), special_flags=pygame.BLEND_RGB_ADD)
        particle_surface.set_alpha(84)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            self.screen.blit(particle_surface, (left + dx, dy), special_flags=pygame.BLEND_RGB_ADD)
        particle_surface.set_alpha(None)
        self.screen.blit(particle_surface, (left, 0), special_flags=pygame.BLEND_RGB_ADD)

        large = np.flatnonzero(active)[::53]
        for index in large:
            if self.data["size"][index] < 1.9:
                continue
            pulse = math.sin(elapsed * 2.1 + float(self.data["phase"][index]))
            if pulse < 0.34:
                continue
            x = left + int(sx[index])
            y = int(sy[index])
            radius = 2 + int(self.data["size"][index] * 0.65)
            if index % 5 == 0:
                color = (255, 224, 174)
            else:
                color = tuple(int(min(255, value * 1.12)) for value in self.colors[index])
            pygame.draw.aaline(self.screen, color, (x - radius * 2, y), (x + radius * 2, y))
            pygame.draw.aaline(self.screen, color, (x, y - radius * 2), (x, y + radius * 2))
            pygame.draw.circle(self.screen, (255, 250, 249), (x, y), 1)

        return float(np.mean(growth) * 100.0)

    def _draw_rose_outlines(self, left: int, scene_w: int, height: int, bloom_t: float, elapsed: float) -> None:
        angle = self._rotation(elapsed) + self.mouse_parallax * 0.055
        points = self.outline_points.copy()
        all_points = np.ones(len(points), dtype=bool)
        self._billboard(points, self.outline_anchors, all_points, angle)
        points *= BOUQUET_SCALE
        sx, sy, _, depth = self._project_world(points, scene_w, height, angle)
        dark, middle, light = PALETTES[self.palette_index]["petal"]
        for index, (start, end) in enumerate(self.outline_slices):
            reveal = max(0.0, min(1.0, (bloom_t - float(self.outline_births[index])) / 0.9))
            if reveal <= 0.0:
                continue
            tone = float(self.outline_tones[index])
            if tone < 0.52:
                base = mix_color(dark, middle, tone / 0.52)
            else:
                base = mix_color(middle, light, (tone - 0.52) / 0.48)
            depth_light = max(0.66, min(1.05, 0.82 + float(np.mean(depth[start:end])) / 900.0))
            color = tuple(int(max(0, min(255, channel * (0.24 + 0.27 * reveal) * depth_light))) for channel in base)
            points = [(left + int(sx[p]), int(sy[p])) for p in range(start, end)]
            if len(points) >= 3:
                pygame.draw.aalines(self.screen, color, True, points)

    def _draw_labels(self, width: int, height: int, left: int, bloom_percent: float, elapsed: float) -> None:
        scene_w = width - left
        palette = PALETTES[self.palette_index]
        if bloom_percent < 99.2:
            status_text = f"GENERATING ROSES  {bloom_percent:05.1f}%"
            status_color = (255, 154, 190)
            status = self.label_font.render(status_text, True, status_color)
            self.screen.blit(status, (width - status.get_width() - 28, 28))
            bar_w = min(245, int(scene_w * 0.32))
            bar_x, bar_y = width - bar_w - 30, 56
            pygame.draw.rect(self.screen, (42, 30, 45), (bar_x, bar_y, bar_w, 2))
            pygame.draw.rect(self.screen, (245, 112, 161), (bar_x, bar_y, int(bar_w * min(1.0, bloom_percent / 100.0)), 2))

        forever = self.label_font.render("∞  FOR YOU, ALWAYS", True, (216, 190, 207))
        self.screen.blit(forever, (left + scene_w // 2 - forever.get_width() // 2, height - 43))
        help_text = self.small_font.render("空格换色  ·  R 重新盛放  ·  F11 全屏  ·  Esc 退出", True, (91, 83, 104))
        self.screen.blit(help_text, (width - help_text.get_width() - 22, height - 23))
        palette_text = self.small_font.render(palette["name"], True, (119, 105, 124))
        self.screen.blit(palette_text, (left + 28, height - 23))

    def _burst(self, x: int, y: int) -> None:
        palette = PALETTES[self.palette_index]["petal"]
        for index in range(38):
            angle = math.tau * index / 38 + self.rng.uniform(-0.12, 0.12)
            speed = self.rng.uniform(55.0, 165.0)
            color = palette[index % 3]
            self.click_sparks.append(ClickSpark(x, y, math.cos(angle) * speed, math.sin(angle) * speed, self.rng.uniform(0.8, 1.5), color))

    def _draw_click_sparks(self, delta: float) -> None:
        live: list[ClickSpark] = []
        for spark in self.click_sparks:
            spark.life -= delta
            if spark.life <= 0:
                continue
            spark.x += spark.vx * delta
            spark.y += spark.vy * delta
            spark.vx *= 0.98
            spark.vy = spark.vy * 0.98 + 32.0 * delta
            fade = min(1.0, spark.life)
            color = tuple(int(channel * fade) for channel in spark.color)
            pygame.draw.circle(self.screen, color, (int(spark.x), int(spark.y)), 2)
            live.append(spark)
        self.click_sparks = live

    def _events(self, width: int) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
                    else:
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)
                elif event.key == pygame.K_SPACE:
                    self._set_palette(self.palette_index + 1)
                elif event.key == pygame.K_r:
                    self.bloom_started = time.perf_counter()
            elif event.type == pygame.MOUSEMOTION:
                self.target_parallax = (event.pos[0] / max(1, width) - 0.5) * 2.0
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._burst(*event.pos)

    def run(self) -> None:
        last = time.perf_counter()
        last_height = self.screen.get_height()
        while self.running:
            now = time.perf_counter()
            delta = min(0.05, now - last)
            last = now
            elapsed = now - self.started
            bloom_t = now - self.bloom_started
            width, height = self.screen.get_size()
            if height != last_height:
                self._make_fonts(height)
                last_height = height
            left = self._left_width(width)
            scene_w = width - left
            self.mouse_parallax += (self.target_parallax - self.mouse_parallax) * 0.045

            self._events(width)
            self._ensure_buffer(scene_w, height)
            self._background(width, height, left, elapsed)
            self._draw_code_panel(width, height, left, elapsed)
            angle = self._rotation(elapsed) + self.mouse_parallax * 0.055
            self._draw_space_box(left, scene_w, height, angle)
            self._draw_rose_outlines(left, scene_w, height, bloom_t, elapsed)
            bloom_percent = self._draw_particles(left, scene_w, height, bloom_t, elapsed)
            self._draw_click_sparks(delta)
            self._draw_labels(width, height, left, bloom_percent, elapsed)
            pygame.display.flip()

            if self.preview_path and not self.preview_saved and bloom_t >= self.preview_ready_at:
                pygame.image.save(self.screen, self.preview_path)
                self.preview_saved = True
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()


def preview_argument() -> str | None:
    if "--preview" not in sys.argv:
        return None
    index = sys.argv.index("--preview")
    if index + 1 >= len(sys.argv):
        return str(Path(__file__).with_name("eternal_rose_preview.png"))
    return sys.argv[index + 1]


if __name__ == "__main__":
    EternalRoseCode(preview_argument()).run()
