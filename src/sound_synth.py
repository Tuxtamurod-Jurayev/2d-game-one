"""
Procedural 8-bit Sound Effects Generator for Pixel Runner.
Generates retro sound waves in-memory using standard library wave + pygame.mixer.Sound.
Zero external asset files needed.
"""
import io
import math
import struct
import wave
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self.enabled = True
            self.sound_jump = self._gen_jump()
            self.sound_coin = self._gen_coin()
            self.sound_hit = self._gen_hit()
            self.sound_checkpoint = self._gen_checkpoint()
        except Exception as e:
            print(f"[SoundManager] Audio initialization skipped or muted: {e}")
            self.enabled = False

    def _create_sound(self, generator, duration, sample_rate=22050):
        n_samples = int(sample_rate * duration)
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            frames = bytearray()
            for i in range(n_samples):
                t = i / sample_rate
                val = generator(t, duration)
                # Clamp to 16-bit signed
                val = max(-32767, min(32767, int(val * 32767)))
                frames.extend(struct.pack('<h', val))
            wf.writeframes(frames)
        buf.seek(0)
        return pygame.mixer.Sound(buf)

    def _gen_jump(self):
        # Pitch sweeps up 300Hz -> 750Hz
        def wave_func(t, dur):
            freq = 320 + (t / dur) * 450
            amp = 0.35 * (1.0 - t / dur)
            return amp * math.sin(2 * math.pi * freq * t)
        return self._create_sound(wave_func, duration=0.15)

    def _gen_coin(self):
        # Two-tone chime 980Hz and 1318Hz (B5 -> E6)
        def wave_func(t, dur):
            half = dur / 2.0
            freq = 980 if t < half else 1318
            amp = 0.35 * (1.0 - (t % half) / half)
            return amp * math.sin(2 * math.pi * freq * t)
        return self._create_sound(wave_func, duration=0.18)

    def _gen_hit(self):
        # Low frequency noise/crunch
        import random
        def wave_func(t, dur):
            freq = 140 * (1.0 - t / dur)
            noise = (random.random() * 2.0 - 1.0) * 0.4
            tone = math.sin(2 * math.pi * freq * t) * 0.6
            amp = 0.5 * (1.0 - t / dur)
            return amp * (tone + noise)
        return self._create_sound(wave_func, duration=0.3)

    def _gen_checkpoint(self):
        # Arpeggio chime
        def wave_func(t, dur):
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            idx = min(int((t / dur) * 4), 3)
            freq = notes[idx]
            amp = 0.3 * (1.0 - (t % (dur / 4)) / (dur / 4))
            return amp * math.sin(2 * math.pi * freq * t)
        return self._create_sound(wave_func, duration=0.32)

    def play_jump(self):
        if self.enabled:
            self.sound_jump.play()

    def play_coin(self):
        if self.enabled:
            self.sound_coin.play()

    def play_hit(self):
        if self.enabled:
            self.sound_hit.play()

    def play_checkpoint(self):
        if self.enabled:
            self.sound_checkpoint.play()
