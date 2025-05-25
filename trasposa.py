#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# =============================================================================
#  Trasposa - Pitch and Speed Modifier for Audio Files
# =============================================================================
#
#  Author:     Valerio Poggi (with some help from Luna!)
#  Created:    2025-05-25
#  License:    GNU General Public License v3.0
#
#  Description:
#    Trasposa is a command-line and Python utility to modify the pitch
#    and/or speed of an audio file. It also normalizes output volume and
#    can play the result directly if no output file is specified.
#
# =============================================================================

import argparse
import platform
import threading
import numpy as np
import librosa
import soundfile as sf
import sounddevice as sd
from pynput import keyboard


def load_audio(file_path):
    """
    Load an audio file.

    Parameters
    ----------
    file_path : str
        Path to the input audio file.

    Returns
    -------
    tuple
        (y, sr) where y is the audio array and sr is the sample rate.
    """
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


def change_pitch(y, sr, semitones):
    """
    Shift the pitch of an audio signal.

    Parameters
    ----------
    y : np.ndarray
        Audio signal.
    sr : int
        Sample rate.
    semitones : int
        Pitch shift in semitones.

    Returns
    -------
    np.ndarray
        Pitch-shifted audio.
    """
    return librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)


def change_speed(y, rate):
    """
    Time-stretch an audio signal.

    Parameters
    ----------
    y : np.ndarray
        Audio signal.
    rate : float
        Stretch factor (<1 = slower, >1 = faster).

    Returns
    -------
    np.ndarray
        Time-stretched audio.
    """
    return librosa.effects.time_stretch(y, rate=rate)


def normalize_audio(y, peak_db=-1.0):
    """
    Normalize an audio signal to a given peak level in decibels.

    Parameters
    ----------
    y : np.ndarray
        Audio signal.
    peak_db : float
        Target peak in dBFS (e.g., -1.0 for -1 dBFS).

    Returns
    -------
    np.ndarray
        Normalized audio.
    """
    peak = np.max(np.abs(y))
    if peak == 0:
        return y
    target = 10 ** (peak_db / 20)
    return y * (target / peak)


def save_audio(y, sr, file_path):
    """
    Save an audio signal to a file.

    Parameters
    ----------
    y : np.ndarray
        Audio signal.
    sr : int
        Sample rate.
    file_path : str
        Output path.
    """
    sf.write(file_path, y, sr)


def play_audio(y, sr):
    """
    Play an audio signal and allow stopping with the 'Q' key.

    Parameters
    ----------
    y : np.ndarray
        Audio signal.
    sr : int
        Sample rate.
    """
    def on_press(key):
        try:
            if key.char and key.char.lower() == 'q':
                sd.stop()
                return False
        except AttributeError:
            pass

    def listen_for_q():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    if platform.system() == "Darwin":
        print("NOTE: On macOS, enable Accessibility for your terminal in:")
        print("      System Settings → Privacy & Security → Accessibility")

    print("Playing audio... Press 'Q' to stop.")
    thread = threading.Thread(target=listen_for_q, daemon=True)
    thread.start()
    sd.play(y, sr)
    sd.wait()


def trasposa(
    input_path,
    semitones=0,
    speed=1.0,
    normalize=True,
    output_path=None
):
    """
    Apply pitch shift and/or time stretch to an audio file.

    Parameters
    ----------
    input_path : str
        Path to input audio file.
    semitones : int, default 0
        Number of semitones to shift.
    speed : float, default 1.0
        Speed factor (1.0 = no change).
    normalize : bool, default True
        Whether to normalize the output volume.
    output_path : str or None
        If None, play the output instead of saving.

    Returns
    -------
    tuple
        (y, sr) of the processed audio.
    """
    y, sr = load_audio(input_path)

    if speed != 1.0:
        y = change_speed(y, speed)

    if semitones != 0:
        y = change_pitch(y, sr, semitones)

    if normalize:
        y = normalize_audio(y)

    if output_path:
        save_audio(y, sr, output_path)
    else:
        play_audio(y, sr)

    return y, sr


def main():
    parser = argparse.ArgumentParser(
        description="Transpose and/or stretch an audio file."
    )
    parser.add_argument(
        "input",
        help="Input audio file (e.g., WAV, MP3)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output audio file. If omitted, play the audio instead."
    )
    parser.add_argument(
        "-s", "--semitones", type=int, default=0,
        help="Number of semitones to transpose (e.g., -2)"
    )
    parser.add_argument(
        "-v", "--speed", type=float, default=1.0,
        help="Speed factor (e.g., 0.9 = slower, 1.1 = faster)"
    )
    parser.add_argument(
        "--no-normalize", action="store_true",
        help="Disable volume normalization"
    )

    args = parser.parse_args()

    trasposa(
        input_path=args.input,
        semitones=args.semitones,
        speed=args.speed,
        normalize=not args.no_normalize,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
