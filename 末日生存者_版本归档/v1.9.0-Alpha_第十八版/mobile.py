# -*- coding: utf-8 -*-

import math
import sys


class MobileLayout:
    CORE_TABS = ['explore', 'backpack', 'map', 'quest', 'more']

    def __init__(self, width, height, platform=None):
        self.width = int(width or 0)
        self.height = int(height or 0)
        raw = (platform if platform is not None else sys.platform) or 'linux'
        self.platform = str(raw).lower()
        shortest = min(self.width, self.height)
        longest = max(self.width, self.height)
        phone_screen = shortest <= 600 or longest <= 960
        self.is_mobile = self.platform in ('android', 'ios') or phone_screen
        if self.platform == 'ios':
            self.safe_top = 47
            self.safe_bottom = 34
        elif self.platform == 'android':
            self.safe_top = 44
            self.safe_bottom = 34
        else:
            self.safe_top = 44 if self.is_mobile else 0
            self.safe_bottom = 34 if self.is_mobile else 0
        self.bottom_bar_height = 72 if self.is_mobile else 0
        self.min_tap_size = 44 if self.is_mobile else 32
        self.one_hand_top = int(self.height * 0.5)

    def core_action_ys(self):
        y = self.height - self.safe_bottom - self.bottom_bar_height / 2.0
        return [y] * len(self.CORE_TABS)

    def bottom_tabs(self):
        return list(self.CORE_TABS)


class MobileTheme:
    PALETTES = {
        'wasteland_dark': {
            'bg': '#2D2419',
            'bg2': '#1A1A1A',
            'text': '#E8DFD0',
            'text2': '#A09888',
            'danger': '#FF6B35',
            'safe': '#4ECDC4',
            'warn': '#FFE66D',
            'info': '#45B7D1',
        },
        'wasteland_brown': {
            'bg': '#3B2A1A',
            'bg2': '#2A1C12',
            'text': '#E8DFD0',
            'text2': '#B5A48C',
            'danger': '#FF6B35',
            'safe': '#4ECDC4',
            'warn': '#FFE66D',
            'info': '#45B7D1',
        },
        'daylight': {
            'bg': '#F5F0E6',
            'bg2': '#E8DFD0',
            'text': '#2D2419',
            'text2': '#5A5044',
            'danger': '#FF6B35',
            'safe': '#4ECDC4',
            'warn': '#C9A227',
            'info': '#45B7D1',
        },
    }

    def __init__(self, name='wasteland_dark'):
        key = str(name or 'wasteland_dark')
        if key not in self.PALETTES:
            key = 'wasteland_dark'
        self.name = key
        self.colors = dict(self.PALETTES[key])


class FontScale:
    _BODY = {'small': 14, 'medium': 16, 'large': 18, 'xlarge': 22}

    def presets(self):
        return ['small', 'medium', 'large', 'xlarge']

    def body_px(self, preset='medium'):
        return self._BODY.get(preset, self._BODY['medium'])

    def line_height_ratio(self):
        return 1.6


class GestureHandler:
    TAP_SLOP = 24
    LONG_PRESS_MS = 500

    def classify(self, x1, y1, x2, y2, duration_ms):
        dx = float(x2) - float(x1)
        dy = float(y2) - float(y1)
        dist = math.hypot(dx, dy)
        if dist <= self.TAP_SLOP:
            if duration_ms >= self.LONG_PRESS_MS:
                return 'long_press'
            return 'tap'
        if abs(dx) >= abs(dy):
            return 'swipe_left' if dx < 0 else 'swipe_right'
        return 'swipe_up' if dy < 0 else 'swipe_down'

    def pinch(self, start_scale, end_scale):
        if float(end_scale) > float(start_scale):
            return 'zoom_in'
        if float(end_scale) < float(start_scale):
            return 'zoom_out'
        return 'none'


class MobileCombatBar:
    def __init__(self):
        self.has_auto_combat = True

    def actions(self):
        return ['attack', 'defend', 'skill', 'item']
