# ADR: Silent Laptop Audio Recording Script

## Context
The user needs a script to record system audio output on a KDE Ubuntu laptop for 6.5 hours, even when the physical volume is turned down or muted.

## Decision
We implemented a bash script `record_laptop_audio.sh` that:
1. Dynamically detects the default audio sink.
2. Creates a virtual null sink (`record_null_sink`) and sets it as the default sink.
3. Creates a loopback from the virtual sink's monitor to the original physical sink so the user can still hear audio if they turn up their physical volume.
4. Moves all active audio streams (sink-inputs) to the virtual sink.
5. Records from the virtual sink's monitor using `ffmpeg` with on-the-fly MP3 compression (192 kbps) to save disk space.
6. Uses a robust signal trap (`trap cleanup EXIT INT TERM`) to restore the original audio configuration and unload virtual modules when finished or interrupted.

## Consequences
- The user can safely mute or turn down their laptop volume, and the recording will still capture everything at full volume.
- The recording is compressed on-the-fly, resulting in a file size of ~560 MB for 6.5 hours instead of ~4.1 GB for uncompressed WAV.
- The system's audio configuration is fully restored to its original state upon completion or interruption.
